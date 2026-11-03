from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from napari.components import ViewerModel

from napari_bioformats._plugin import get_reader

if TYPE_CHECKING:
    from pathlib import Path

DIMS = "sizeX=16&sizeY=8&sizeZ=3&sizeC=2"


# Bio-Formats "fake" files are generated from the key=value pairs in the filename
@pytest.mark.parametrize(
    ("fake_params", "scale", "units"),
    [
        (
            "physicalSizeX=0.25&physicalSizeY=0.25&physicalSizeZ=2",
            (1, 2, 0.25, 0.25),
            ("pixel", "micrometer", "micrometer", "micrometer"),
        ),
        (
            "physicalSizeX=5nm&physicalSizeY=5nm&physicalSizeZ=20nm",
            (1, 20, 5, 5),
            ("pixel", "nanometer", "nanometer", "nanometer"),
        ),
        ("", (1, 1, 1, 1), ("pixel",) * 4),
    ],
)
def test_scale_and_units(
    tmp_path: Path,
    fake_params: str,
    scale: tuple[float, ...],
    units: tuple[str, ...],
) -> None:
    path = tmp_path / f"test&{DIMS}&{fake_params}.fake"
    path.touch()

    reader = get_reader(str(path))
    assert reader is not None
    layer_data = reader(str(path))

    viewer = ViewerModel()
    for data, kwargs, _ in layer_data:
        viewer.add_image(data, **kwargs)

    assert len(viewer.layers) == 2  # one per channel
    for layer in viewer.layers:
        assert layer.data.shape == (1, 3, 8, 16)
        assert layer.axis_labels == ("t", "z", "y", "x")
        assert tuple(layer.scale) == pytest.approx(scale)
        assert tuple(str(u) for u in layer.units) == units

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from bffile import BioFile

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from napari.types import LayerData

    # example_plugin.some_module
    PathOrPaths = str | Sequence[str]
    ReaderFunction = Callable[[PathOrPaths], list[LayerData]]

SUFFIXES = tuple(BioFile.list_supported_suffixes())


def get_reader(path: PathOrPaths) -> ReaderFunction | None:
    """Napari reader plugin hook"""
    if isinstance(path, str):
        if path.endswith(SUFFIXES):
            return _reader_function
    return None


def _reader_function(path: PathOrPaths) -> list[LayerData]:
    assert isinstance(path, str), "Should not have been called with multiple paths"

    bf = BioFile(path).open()
    fname = os.path.split(path)[-1].rsplit(".", 1)[0]
    if bf.series_count() == 1:
        indices = [0]
    else:
        # If there are more than one series,
        # pop up a selector dialog to choose which one(s) to load.
        from ._series_selector import get_series

        indices = get_series(bf)

    if not indices:
        return [(None,)]

    split_channels = True
    ome_meta = bf.ome_metadata
    layers = []
    for i in indices:
        series = bf[i]
        if series.resolution_count > 1:
            data: Any = [
                series.as_array(resolution=r) for r in range(series.resolution_count)
            ]
        else:
            data = series.as_array()

        # data is TCZYX (or TCZYXS for rgb); napari doesn't take a scale for the
        # rgb axis, so these always have one entry per TCZYX axis.
        axis_labels = list("tczyx")
        scale = [1.0] * 5
        units = ["pixel"] * 5
        try:
            pixels = ome_meta.images[i].pixels
            for ax, dim in enumerate("zyx", start=2):
                size = getattr(pixels, f"physical_size_{dim}", None)
                unit = getattr(pixels, f"physical_size_{dim}_unit", None)
                if size:
                    scale[ax] = size
                    # ome-types defaults the unit to µm even when size is unset,
                    # so only trust it when there is a size.
                    # "reference frame" is the one OME length unit pint rejects
                    if unit is not None and unit.value != "reference frame":
                        units[ax] = unit.value
        except (IndexError, AttributeError):
            pass

        if split_channels:
            axis_labels.pop(1)
            scale.pop(1)
            units.pop(1)
            channel_axis = 1
        else:
            channel_axis = None

        kwargs = {
            "rgb": series.is_rgb,
            "channel_axis": channel_axis,
            "name": f"{fname} (Series {i})",
            "axis_labels": axis_labels,
            "scale": scale,
            "units": units,
            "metadata": {"ome_types": ome_meta},
        }

        layers.append((data, kwargs, "image"))
    return layers

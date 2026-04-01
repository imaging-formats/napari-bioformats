# napari-bioformats: Bio-Formats plugin for napari using [bffile](https://github.com/imaging-formats/bffile)

[![License](https://img.shields.io/pypi/l/napari-bioformats.svg?color=green)](https://github.com/napari/napari-bioformats/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-bioformats.svg?color=green)](https://pypi.org/project/napari-bioformats)
[![Conda](https://img.shields.io/conda/v/conda-forge/napari-bioformats)](https://anaconda.org/conda-forge/napari-bioformats)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-bioformats.svg?color=green)](https://python.org)
[![tests](https://github.com/imaging-formats/napari-bioformats/actions/workflows/ci.yml/badge.svg)](https://github.com/imaging-formats/napari-bioformats/actions/workflows/ci.yml)
<!-- hide the unused badge right now
[![codecov](https://codecov.io/gh/imaging-formats/napari-bioformats/branch/master/graph/badge.svg)](https://codecov.io/gh/imaging-formats/napari-bioformats)
-->

Use the classic Java-based OME Bio-Formats reader you know and love from ImageJ/Fiji, QuPath, etc. in napari to open >100 different imaging file formats (for details, see the [Bio-Formats documentation](https://bio-formats.readthedocs.io/en/stable/formats/index.html)).

This plugin leverages [`bffile`](https://imaging-formats.github.io/bffile/), a modern Bio-Formats wrapper for Python: 
- "Batteries include": no special Java setup is required
- Layer data is returned as [LazyBioArray](https://imaging-formats.github.io/bffile/api/#bffile.LazyBioArray) with full lazy indexing and slicing (with no additional dependencis on dask/xarray/zarr)
- Basic OME metadata handling to identify channel axis and scale
- Automatic handling of multiple resolution levels as napari MultiScaleData

Additionally, it provides a convenient Series selection widget allowing you to choose what to load when a file contains multiple Series.

## Installation

You can install the plugin using the built-in napari Plugin manager in the Plugins menu or from either conda-forge or PyPI over a wide range of Python versions (3.10-3.14) using your favorite package manager. E.g.:

```bash
conda install napari-bioformats
```

or

```bash
pip install napari-bioformats
```

> [!TIP]
> **No manual Java installation required!**  
>
> This package automatically downloads and manages the Java runtime using
> [cjdk](https://github.com/cachedjdk/cjdk) (via [scyjava](https://github.com/scijava/scyjava)).

## Contributing

Contributions are welcome! 

To get started, fork and clone the repository. For the development environment we recommend using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Please be sure to work on contributions in a dedicated branch and then open a pull request for review.


## Releasing

Anyone with write access can create a release:

1. **Locally:**

   checkout the commit you want to release, then run:

   ```bash
   git tag -a vX.Y.Z -m vX.Y.Z
   git push upstream --follow-tags
   ```

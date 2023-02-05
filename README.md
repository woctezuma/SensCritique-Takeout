# SensCritique Takeout

[![PyPI status][pypi-image]][pypi]
[![Build status][build-image]][build]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to export your data from [SensCritique.com](https://www.senscritique.com).

## Installation

The code is packaged for [PyPI](https://pypi.org/project/senscritique/), so that the installation consists in running:

```bash
pip install senscritique
```

## Usage

### Library (« collection »)

A library can be downloaded as follows:

```python
import senscritique

# Download in JSON format the library of the given user
data = senscritique.parse_and_cache(user_name='wok', data_type='collection')
```

### Reviews (« critiques »)

Reviews can be downloaded as follows:

```python
import senscritique

# Download in JSON format the reviews of the given user
data = senscritique.parse_and_cache(user_name='wok', data_type='critiques')
```

### Rankings (« listes »)

Rankings can be downloaded as follows:

```python
import senscritique

# Download in JSON format the rankings of the given user
data = senscritique.parse_and_cache(user_name='wok', data_type='listes')
```

## References

- [Google Takeout](https://en.wikipedia.org/wiki/Google_Takeout)

<!-- Definitions for badges -->

[pypi]: <https://pypi.python.org/pypi/senscritique>
[pypi-image]: <https://badge.fury.io/py/senscritique.svg>

[build]: <https://github.com/woctezuma/SensCritique-Takeout/actions>
[build-image]: <https://github.com/woctezuma/SensCritique-Takeout/workflows/Python package/badge.svg?branch=master>
[publish-image]: <https://github.com/woctezuma/SensCritique-Takeout/workflows/Upload Python Package/badge.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/SensCritique-Takeout/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/SensCritique-Takeout/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/SensCritique-Takeout/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/SensCritique-Takeout>
[codecov-image]: <https://codecov.io/gh/woctezuma/SensCritique-Takeout/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/SensCritique-Takeout>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/5414284721184d139b48023a0467858d>

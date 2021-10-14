How to publish to PyPI
===============================

## Step I: make sure to increase version number

Version number is located in `exh/__init__.py`

## Step II: Create archive files

```bash
python setup.py sdist bdist_wheel
```

## Step III: check package

```bash
twine check dist/NAME_OF_DISTFILE
```

## Step IV : upload package

```bash
twine upload dist/FILES_TO_UPLOAD
```

**Caveat:** No reuploads are possible. One ought to make sure that the archive contains everything as desired.


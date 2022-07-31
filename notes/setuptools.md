# Setup Tools Notes

## Install
```bash
pip install setuptools wheel twine
```

## Publish
```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
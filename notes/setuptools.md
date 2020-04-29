# Setup Tools Notes

## Install

    pip install setuptools wheel

## Publish

    python3 setup.py sdist bdist_wheel
    python3 -m twine upload dist/*
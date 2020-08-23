# Setup Tools Notes

## Install

    pip install setuptools wheel twine

## Publish

    python3 setup.py sdist bdist_wheel
    python3 -m twine upload dist/*
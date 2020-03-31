Create a virtual environment in this directory
    
    pip3 -m venv env
    source env/bin/activate

Install Badwing in it so we can generate the API docs

    pip install ../

Install Sphinx

    pip install sphinx

Quick Start

    sphinx-quickstart

Install Theme

    pip install sphinx_rtd_theme

Set the theme

    html_theme = 'sphinx_rtd_theme'

Uncomment these lines at the top of conf.py
```
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
```

Generate the API docs manually

    sphinx-apidoc -o source/ ../badwing

Generate the API docs automatically

    pip install sphinxcontrib-apidoc

In conf.py
```
extensions = [
    'sphinxcontrib.apidoc',
    # ...
]
apidoc_module_dir = '../badwing'
apidoc_output_dir = 'reference'
apidoc_excluded_paths = ['tests']
apidoc_separate_modules = True
```

Generate the HTML

    make html
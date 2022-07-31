# BadWing :butterfly:

Skateboarder/Platformer/Lepidopterist Game using Arcade & Pymunk

## Quick Links

:notebook: [Documentation](https://badwing.readthedocs.io/en/latest/)

:package: [Package](https://pypi.org/project/badwing/)

## Installation

### From PyPI

#### TLDR - do this at your own risk

```bash
pip install badwing
```

#### Recommended - pipX

If you don't already have it installed go to https://pypi.org/project/pipx/ for instructions
```bash
pipx install badwing
```

#### And then run it!
```bash
badwing run
```

### From GitHub

Clone the repository
```bash
git clone https://github.com/kfields/badwing.git
```

Navigate to the new directory which contains the repository
```bash
cd badwing
```

Create a Python 3 virtual environment called `env`
```bash
python3 -m venv env
```

Activate the environment
```bash
source env/bin/activate
```
        
Install required packages
```bash
pip install -r requirements.txt
```

## Usage

Activate the virtual environment, if not already active
```bash
cd badwing
source env/bin/activate
```

Run the game
```bash
python run_game.py
```

## Controls

### Movement

WASD + cursor keys
Press down to mount/dismount
Press up to do an Ollie! :)

### Pause/Menu

Escape key

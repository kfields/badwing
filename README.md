# BadWing :butterfly:

Skateboarder/Platformer/Lepidopterist Game using Arcade & Pymunk

## Installation

### From PyPI

#### TLDR - do this at your own risk

        pip install badwing

#### Recommended - pipX

If you don't already have it installed go to https://pypi.org/project/pipx/ for instructions

        pipx install badwing

#### And then run it!

        badwing run


### From GitHub

Navigate to a directory where you keep your software projects

        cd <myprojects>

Clone the repository

        git clone https://github.com/kfields/badwing.git
        
Navigate to the new directory which contains the repository

        cd badwing

Create a Python 3 virtual environment called `env`

        python3 -m venv env
        
Activate the environment

        source env/bin/activate
        
Install required packages

        pip install -r requirements.txt


## Run

Activate the virtual environment, if not already active

        cd badwing
        source env/bin/activate
        
Run the game

        python run_game.py

## Controls

WASD + cursor keys.  Press up to do an Ollie! :)
#!/bin/bash

#run with "source init.sh"

alias activate=". venv/bin/activate"

if [[ ! -d venv ]]
then
    echo "wha hav y done!?"
    python3 -m venv ./venv
fi

# activate venv
activate

# install all the packages
echo "Installing packages from requirements"
pip install -r requirement.txt


echo "imma don"


# to save current python packages use pip freeze > requirement.txt
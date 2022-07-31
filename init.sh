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
pip install -r requirements.txt

# to save current python packages use pip freeze > requirements.txt

echo "Requirement installed in virtual environment"

docker-compose up -d

echo "docker-compose executed"

python market_producer.py &
python twitter_producer.py &

echo "waiting for data in the queue (120s)"
sleep 120

echo "executing predictive model"
python model_one.py
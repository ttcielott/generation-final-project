#! /bin/bash
set -eu

echo -n "What is your operation system? [W if Window, L if Linux]: "
read var

# create a docker container for database
cd database
docker compose up -d

# cerate a virtual environment
if [[ $var == 'W']]
    py -3.10 -m venv .venv

    # activate the virtual environment
    .venv/Scripts/Activate.bat
else
    python3.10 -m venv .venv
    source .venv/bin/activate
then
    echo "a virtural environment was created and activated"
fi
    
# install packages from requirements.txt
cd main_files
pip install -r requirements.txt


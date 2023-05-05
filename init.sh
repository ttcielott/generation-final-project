#! /bin/bash
set -eu

echo -n "What is your operation system? [W if Window, L if Linux]: "
read var

# create a docker container for database
# cd database
# docker compose up -d

if [[ $var == 'W' ]]
then
    # cerate a virtual environment
    py -3.10 -m venv .venv

    # activate the virtual environment
    .venv/Scripts/Activate.bat
elif [[ $var == 'L' ]]
then
    # cerate a virtual environment
    python3.10 -m venv .venv
    # activate the virtual environment
    current_dir=$(pwd)
    source .venv/bin/activate
fi
echo "a virtural environment was created and activated"
    
# install packages from requirements.txt
cd main_files
pip install -r requirements.txt

# virtual environment got deactivated, so activate again
if [[ $var == 'W' ]]
then
    # activate the virtual environment
    .venv/Scripts/Activate.bat
elif [[ $var == 'L' ]]
then
    # activate the virtual environment
    source .venv/bin/activate
fi

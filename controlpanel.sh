#!/bin/bash

cd /home/$USER/PycharmProjects/hackerspace-scripts-2

FILE="/home/$USER/.profile"
localdir="$(pwd)"


echo -e "export PATH=\$PATH:$localdir/" >> $FILE
echo "log out then back in, successfuly made 'controlpanel.sh' a linked command!"

if [ ! -f venv/bin/activate ]; then
    python3 -m venv
fi

source /home/$USER/PycharmProjects/hackerspace-scripts-2/venv/bin/activate
python /home/$USER/PycharmProjects/hackerspace-scripts-2/controlpanel.py
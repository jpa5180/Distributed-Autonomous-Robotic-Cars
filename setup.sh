#!/bin/sh

sudo pip install --upgrade pip
sudo pip install virtualenv

if [ ! -d "venv/" ]; then
  virtualenv venv
fi

source venv/bin/activate

sudo apt update
sudo apt install python3-opencv
sudo pip install numpy
sudo pip install pillow
sudo pip install pupil_apriltags
sudo python -m pip install "kivy[base]"

deactivate


# Ambient

Ambient soundscape player

This program looks in the current directory for .ogg files or .flac files and
plays them for five minutes each fading in between the sound files. If a sound
file is less than five minutes it will loop the sound.

## Installation

 - Requires python3
 - Requires pygame

Run `pip3 install --user -r requirements.txt` to install pygame if not already installed

Recommended: link `ambient` in a directory on your path. E.g. `ln -s ambient ~/bin/ambient`

## Usage

Run `ambient` in a directory with `.ogg` files to start listening.

Use "ctrl-c" to stop.

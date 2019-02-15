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

### Alternate install (compile pygame from source)

If you notice high CPU usage while running ambient, it may be due to [known issue 331](https://github.com/pygame/pygame/issues/331).

To install pygame from scratch instead, use the following commands (assuming linux):

```
# Clone source repo
sudo apt install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame

sudo apt install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev

python3 setup.py build
sudo python3 setup.py install
```

## Usage

Run `ambient` in a directory with `.ogg` files to start listening.

Use "ctrl-c" to stop.


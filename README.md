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

## Sound credits

Credit goes to the following for the sound files included in this package:

- Bruce Baron for [`alien-contact.ogg`](https://freesound.org/people/Sclolex/sounds/149131/)
- Vann Westfold for [`ambienttraut.ogg`](https://freesound.org/people/Vann%20Westfold/sounds/34308/)
- Ero Kia for [`ambient-wave-17.ogg`](https://freesound.org/people/deleted_user_2731495/sounds/395837/)
- Sclolex for [`cave.ogg` (Water Dripping in a Large Cave)](https://freesound.org/people/Sclolex/sounds/177958/)
- Ero Kia for [`elementary-wave-11.ogg`](https://freesound.org/people/deleted_user_2731495/sounds/183881/)
- Blair Ferrier for [`helicopter-mix.ogg`](https://freesound.org/people/nofeedbak/sounds/41171/)
- Chris Zabriskie for [`long-hallway.ogg` (excerpt from "I Am Running Down the Long Hallway of Viewmont Elementary)](http://freemusicarchive.org/music/Chris_Zabriskie/I_Am_a_Man_Who_Will_Fight_for_Your_Honor/I_Am_Running_Down_the_Long_Hallway_of_Viewmont_Elementary) Creative Commons 3.0
- György Ligeti for `lux-aeterna-excerpt.ogg`
- Sclolex for [`night-sounds.ogg` (Sounds on a quiet night)](https://freesound.org/people/Sclolex/sounds/342106/)
- Luftrum for [`ocean-waves.ogg`](https://freesound.org/people/Luftrum/sounds/48412/)
- chzmn for [`perfect-storm.ogg`](https://weather.ambient-mixer.com/the-perfect-storm)
- Hargisss Sound for [`spring-birds.ogg`](https://freesound.org/people/hargissssound/sounds/345851/)

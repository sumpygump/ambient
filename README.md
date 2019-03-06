# Ambient

Ambient soundscape player

This is a python cli program that plays audio files, looping them for a specified
duration and fading between them.

It reads a directory for `.ogg`, `.wav` or `.flac` files. The program comes
with a set of files, but can be used with any files on your computer of the
supported types by using the `--path` parameter when invoking.

## Installation

 - Requires python3
 - Requires pygame

Run `pip3 install --user -r requirements.txt` to install pygame if not already installed

Recommended: link `ambient` in a directory on your path. E.g. `ln -s ambient ~/bin/ambient`

### Alternate install for pygame (compile pygame from source)

To install pygame from scratch instead of using pip, you can use the following
commands (assuming linux):

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

To run with the default settings, simply run `ambient`. Use "ctrl-c" to stop.

```
usage: ambient [-h] [-v] [-p PATH] [-d DURATION] [-n] [paths [paths ...]]

positional arguments:
  paths                 load given sound file(s) or path(s)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version and exit
  -p PATH, --path PATH  set the path where the sound files are
  -d DURATION, --duration DURATION
                        set the duration in minutes each sound will play: default=5
  -n, --noinput         disable the stdin input capture
```

If invoked without the `-n` parameter, press 'n' to skip to next sound and 'q'
to quit.

The default sounds used are in the install directory (wherever you
cloned/downloaded this repo) in the sub-directory `sounds`.

## Sound credits

Credit goes to the following for the sound files included in this package:

- Bruce Baron for [`alien-contact.ogg`](https://freesound.org/people/Sclolex/sounds/149131/)
- Vann Westfold for [`ambienttraut.ogg`](https://freesound.org/people/Vann%20Westfold/sounds/34308/)
- Ero Kia for [`ambient-wave-17.ogg`](https://freesound.org/people/deleted_user_2731495/sounds/395837/)
- Mynoise.net for [`b25-bomber.ogg`](https://mynoise.net/NoiseMachines/propellerNoiseGenerator.php?l=32353333252532141414&m=&d=0)
- Mynoise.net for [`binaural-low-complex.ogg`](https://mynoise.net/NoiseMachines/binauralBrainwaveGenerator.php?l=61565146413633292522&m=&d=0)
- Sclolex for [`cave.ogg` (Water Dripping in a Large Cave)](https://freesound.org/people/Sclolex/sounds/177958/)
- Daniel Simion for [`crackling-fireplace`](http://soundbible.com/2178-Crackling-Fireplace.html)
- musicbrain for [`didgeridu-monk.ogg`](https://freesound.org/people/musicbrain/sounds/376577/)
- Ero Kia for [`elementary-wave-11.ogg`](https://freesound.org/people/deleted_user_2731495/sounds/183881/)
- Blair Ferrier for [`helicopter-mix.ogg`](https://freesound.org/people/nofeedbak/sounds/41171/)
- Chris Zabriskie for [`long-hallway.ogg` (excerpt from "I Am Running Down the Long Hallway of Viewmont Elementary)](http://freemusicarchive.org/music/Chris_Zabriskie/I_Am_a_Man_Who_Will_Fight_for_Your_Honor/I_Am_Running_Down_the_Long_Hallway_of_Viewmont_Elementary") Creative Commons 3.0
- György Ligeti for `lux-aeterna-excerpt.ogg`
- Sclolex for [`night-sounds.ogg` (Sounds on a quiet night)](https://freesound.org/people/Sclolex/sounds/342106/)
- Luftrum for [`ocean-waves.ogg`](https://freesound.org/people/Luftrum/sounds/48412/)
- chzmn for [`perfect-storm.ogg`](https://weather.ambient-mixer.com/the-perfect-storm)
- Hargisss Sound for [`spring-birds.ogg`](https://freesound.org/people/hargissssound/sounds/345851/)
- Trekcore.com for [`warp-core-hum.ogg`](http://www.trekcore.com/audio/)

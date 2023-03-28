# Ambience

Ambient soundscape player

This is a python cli program that plays audio files, looping them for a specified
duration and fading between them.

It reads a directory for `.ogg`, `.wav` or `.flac` files. The program comes
with a set of files, but can be used with any files on your computer of the
supported types by using the `--path` parameter when invoking.

## Installation with pip

```
pip install ambience

ambience --fetch-library
```

## Manual Installation

 - Requires python3
 - Requires pygame

Clone this repository.

Run `pip3 install --user -r requirements.txt` to install pygame if not already installed

Recommended: link `ambience` in a directory on your path. E.g. `ln -s ambience.py ~/bin/ambience`

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

To run with the default settings, simply run `ambience`. Use "ctrl-c" to stop.

```
Hello from the pygame community. https://www.pygame.org/contribute.html
usage: ambience [-h] [-d DURATION] [-f] [-i] [-n] [-p PATH] [-q] [-v] [paths ...]

positional arguments:
  paths                 load given sound file(s) or path(s)

options:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        set the duration in minutes each sound will play: default=5
  -f, --fetch-library   fetch the sound library from internet
  -i, --noinit          do not pre-initialize all sounds at start
  -n, --noinput         disable the stdin input capture
  -p PATH, --path PATH  set the path where the sound files are
  -q, --quiet           produce no output
  -v, --version         show version and exit
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
- NASA/JPL for [`mars-perseverance.ogg`](https://mars.nasa.gov/resources/25399/in-flight-perseverance-rovers-interplanetary-sound/)
- Mynoise.net for [`b17-bomber.ogg`](https://mynoise.net/NoiseMachines/propellerNoiseGenerator.php?l=46504747000046202020)
- juskiddink for [`bonfire.ogg`](https://freesound.org/people/juskiddink/sounds/65795/)
- AshFox for [`coffee-shop.ogg`](https://freesound.org/people/AshFox/sounds/172968/)
- unfa for [`fan.ogg`](https://freesound.org/people/unfa/sounds/170869/)
- inchadney for [`forest.ogg`](https://freesound.org/people/inchadney/sounds/56611/)
- juskiddink for [`leaves.ogg`](https://freesound.org/people/juskiddink/sounds/78955/)
- el mar for [`library.ogg`](https://freesound.org/people/el_mar/sounds/171008/)
- juskiddink for [`seaside.ogg`](https://freesound.org/people/juskiddink/sounds/194868/)
- SDLx for [`train.ogg`](https://freesound.org/people/SDLx/sounds/259988/)
- Greim for the [machine-planet samples](https://greim.github.io/machine-planet/)
- NASA/JPL for [`mars-ingenuity.ogg`](https://mars.nasa.gov/resources/25893/listen-to-nasas-ingenuity-mars-helicopter-in-flight/)
- AdrienPola for [`amazon-rainforest.ogg`](https://freesound.org/people/AdrienPola/sounds/413976/)
- dobroide for [`rural-spain.ogg`](https://freesound.org/people/dobroide/sounds/269218/)
- Mynoise.net for [`the-pilgrim.ogg`](https://mynoise.net/NoiseMachines/tongueDrumSoundscapeGenerator.php)
- anankalisto for [`resonance-of-the-gods.ogg`](https://freesound.org/people/anankalisto/sounds/139050/)
- Emanuele Correani for [`train-station.ogg`](https://freesound.org/people/Emanuele_Correani/sounds/332769/)
- InspectorJ for [`machine-factory.ogg`](https://freesound.org/people/InspectorJ/sounds/385943/)
- Gladkiy for [`metro-outdoors.ogg`](https://freesound.org/people/gladkiy/sounds/333361/)
- Zabuhailo for [`metro.ogg`](https://freesound.org/people/Zabuhailo/sounds/193742/)

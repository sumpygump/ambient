#!/usr/bin/env python3
"""Ambience: ambient soundscape player"""

# ----------------------------------------------------#
#       _              _     _                        #
#      / \   _ __ ___ | |__ (_) ___ _ __   ___ ___    #
#     / _ \ | '_ ` _ \| '_ \| |/ _ \ '_ \ / __/ _ \   #
#    / ___ \| | | | | | |_) | |  __/ | | | (_|  __/   #
#   /_/   \_\_| |_| |_|_.__/|_|\___|_| |_|\___\___|   #
#                                                     #
# ----------------------------------------------------#

import argparse
import fcntl
from fnmatch import fnmatch
import hashlib
import os
import pygame
import random
import sys
import termios
import tty

from pygame.locals import *  # pylint: disable=wildcard-import

AMBIENT_TICK = USEREVENT + 1


class AmbientSounds:
    """AmbientSounds class"""

    version = "1.0.12"

    # FPS: Low number is used to reduce CPU;
    # Don't really need pygame's cycle running so frequently
    fps = 2

    # How long each sound should play (by itself)
    play_duration = 600

    # Number of ambient ticks (half seconds) for a fade
    fade_duration = 120
    fade_ms = fade_duration * 1000

    # Countdown timer for playing sound
    play_timer = 0

    # Storage of sound objects
    sounds = {}
    current_sound = 0
    animate_chars = "◐◓◑◒"
    animate_position = 0

    # Path and sound files
    package_path = os.path.dirname(os.path.realpath(__file__))
    paths = [os.path.join(package_path, "sounds")]
    files = []

    # Whether to listen to stdin in cli (experimental
    noinput = False

    # Whether to silence output
    quiet = False

    # Volume
    volume = 1.0
    muted = False

    def __init__(
        self, paths=None, duration=5, noinput=False, quiet=False, initialize_sounds=True
    ):
        if paths:
            self.paths = paths
        self.noinput = bool(noinput)
        self.quiet = bool(quiet)

        # Calculate number of half seconds from minutes
        self.play_duration = float(duration) * (self.fps * 60)

        # If the duration is shorter than the standard fade, make a new fade duration
        if self.play_duration <= self.fps * 60:
            self.fade_duration = float(self.play_duration / 5.0)  # 5% of sound duration
            self.fade_ms = int(self.fade_duration * (1000.0 / self.fps))

        if not self.quiet:
            print(self.get_version())

        self.files = self.load_sound_files()
        if initialize_sounds:
            self.initialize_sounds()

    @classmethod
    def get_version(cls):
        return "Ambient version {}".format(cls.version)

    def start(self):
        if len(self.files) == 0:
            print("No sound files to load!")
            pygame.quit()
            sys.exit(1)

        if not self.quiet:
            print("\nPlaying sounds. Press Ctrl-C to exit.", flush=True)
        if not self.noinput and not self.quiet:
            print("Press '[' and ']' to change volume and press 'm' to mute.")
            print(
                "Press 'n' to go to next sound, "
                "or 'p' to go to previous sound. Press 'q' to quit.",
                flush=True,
            )
        if sys.stdout.isatty():
            print("\033[?25l")  # Hide cursor

        # Load the first sound
        self.load_sound(self.current_sound)

        # Start first sound
        self.sounds[self.get_sound_id(self.current_sound)].play(-1, fade_ms=3000)
        self.play_timer = int(
            self.play_duration - (self.fade_duration / 2) - (3 * self.fps)
        )

    def tick(self):
        self.handle_play()
        if sys.stdout.isatty() and not self.quiet:
            self.print_current_sound()

    def print_current_sound(self):
        self.animate_position += 1
        if self.animate_position >= len(self.animate_chars):
            self.animate_position = 0

        animate_char = self.animate_chars[self.animate_position]
        sound_name = os.path.basename(self.files[self.current_sound])

        volume_str = ""
        if self.volume < 1.0:
            volume_str = " vol: {}%".format(int(self.volume * 100))
        if self.muted:
            volume_str = " [mute]"

        print(
            "\r\033[K▶  Playing {} {} {}".format(sound_name, animate_char, volume_str),
            end="",
        )

    def handle_play(self):
        if self.play_timer > 0:
            self.play_timer = self.play_timer - 1
            if self.play_timer == min(10, int(self.play_duration / 2)):
                # Load the next sound a few ticks before we need to play it
                self.load_sound(self.get_next_sound())
        else:
            self.stop_sound(self.current_sound)
            self.start_next_sound()

    def start_next_sound(self, fade_override=None):
        self.current_sound = self.get_next_sound()

        self.play_sound(self.current_sound, fade_override)

    def get_next_sound(self):
        next_sound = self.current_sound + 1

        if next_sound >= len(self.files):
            next_sound = 0

        return next_sound

    def start_previous_sound(self, fade_override=None):
        self.current_sound = self.get_previous_sound()

        self.play_sound(self.current_sound, fade_override)

    def get_previous_sound(self):
        previous_sound = self.current_sound - 1

        if previous_sound < 0:
            previous_sound = len(self.files) - 1

        return previous_sound

    def next(self):
        self.load_sound(self.get_next_sound())
        self.stop_sound(self.current_sound, 2)
        self.start_next_sound(2)

    def previous(self):
        self.load_sound(self.get_previous_sound())
        self.stop_sound(self.current_sound, 2)
        self.start_previous_sound(2)

    def play_sound(self, index, fade_override=None):
        fade_duration, fade_ms = self._get_fade_duration(fade_override)

        self.load_sound(index)
        self.sounds[self.get_sound_id(index)].play(-1, fade_ms=fade_ms)
        self.play_timer = int(self.play_duration - (fade_duration / 2))

    def stop_sound(self, index, fade_override=None):
        _, fade_ms = self._get_fade_duration(fade_override)

        self.sounds[self.get_sound_id(index)].fadeout(fade_ms)

    def end_fadeout(self, duration=4000):
        if not self.quiet:
            print()
            print("Stopping sounds...", flush=True)
        pygame.mixer.fadeout(duration)
        pygame.time.wait(duration)
        print("Goodbye.", flush=True)

    def _get_fade_duration(self, fade_override=None):
        fade_duration = fade_override if fade_override else self.fade_duration
        fade_ms = int(fade_duration * (1000.0 / self.fps))
        return (fade_duration, fade_ms)

    def decrease_volume(self):
        self.volume = self.volume - 0.05
        self.volume = max(self.volume, 0.0)
        self.set_volume(self.volume)

    def increase_volume(self):
        self.volume = self.volume + 0.05
        self.volume = min(self.volume, 1.0)
        self.set_volume(self.volume)

    def set_volume(self, level):
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(level)

    def mute(self):
        self.muted = not self.muted
        if self.muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self.volume)

    def load_sound(self, file_index):
        if self.get_sound_id(file_index) not in self.sounds:
            try:
                self.sounds[self.get_sound_id(file_index)] = pygame.mixer.Sound(
                    file=self.files[file_index]
                )
            except pygame.error as e:
                # Remove this file so we skip trying to play it
                del self.files[file_index]
                print("\nERROR {} -- skipping sound.".format(str(e)))

    def get_files(self, paths):
        files = []

        for path in paths:
            try:
                if os.path.isdir(path):
                    files.extend(self.get_files_from_path(path))
                else:
                    self.add_valid_file(path, files)
            except FileNotFoundError:
                print("Path '{}' not found".format(path))

        if len(files) == 0:
            print("No sound files to load!")
            sys.exit(1)

        return files

    def get_sound_id(self, file_index):
        try:
            _ = self.files[file_index]
        except IndexError:
            print("Error: cannot reference sound {}".format(file_index))
        return hashlib.md5(str(file_index).encode("utf-8")).hexdigest()[:6]

    def get_files_from_path(self, path):
        files = []
        for f in os.listdir(path):
            full = os.path.join(path, f)
            if os.path.isdir(full):
                files.extend(self.get_files_from_path(full))  # recurse
            if len(files) > 64:
                break  # break if we have enough
            self.add_valid_file(full, files)
        return files

    def add_valid_file(self, path, files):
        patterns = ["*.ogg", "*.wav", "*.flac"]
        if any(fnmatch(path, pattern) for pattern in patterns):
            files.append(path)

    def load_sound_files(self):
        if not self.quiet:
            print("Reading sounds from paths")
            [print(" - {}".format(path)) for path in self.paths]
            print("")

        files = self.get_files(self.paths)
        random.shuffle(files)

        if len(files) == 0:
            return files

        if not self.quiet:
            print("Sounds:")
            for index, file in enumerate(files):
                # Clean up common ancestors in sound file paths
                for path in self.paths:
                    if path in file:
                        listed_sound = file.replace(path + os.sep, "")
                print("{}. {}".format(index + 1, listed_sound))

        return files

    def initialize_sounds(self):
        if not self.quiet:
            print("\nInitializing sounds ", end="", flush=True)
        for i, _ in enumerate(self.files):
            if not self.quiet:
                print(".", end="", flush=True)
            self.load_sound(i)
        if not self.quiet:
            print()

    def event_loop(self):
        while True:
            try:
                if self.noinput:
                    char = False
                else:
                    char = sys.stdin.read(1)
                self.handle_events(char)
            except KeyboardInterrupt:
                self.the_end()

    def handle_events(self, char_input=False):
        for event in pygame.event.get():
            if event.type == AMBIENT_TICK:
                self.tick()
            if event.type == pygame.KEYUP:
                # Keyboard in pygame window (macos)
                self.handle_input(event.key)
        if char_input:
            # Stdin in cli
            self.handle_input(ord(char_input))

        # Advance game tick and wait to continue execution
        pygame.time.Clock().tick(self.fps)

    def handle_input(self, key_code):
        # For debugging
        # print(chr(key_code), end="")
        if key_code == K_n:
            self.next()
        elif key_code == K_p:
            self.previous()
        elif key_code == K_q:
            self.the_end()
        elif key_code == K_LEFTBRACKET:
            self.decrease_volume()
        elif key_code == K_RIGHTBRACKET:
            self.increase_volume()
        elif key_code == K_m:
            self.mute()

    def the_end(self):
        try:
            self.end_fadeout()
            pygame.quit()
            if sys.stdout.isatty():
                print("\033[?25h")  # Show cursor
            sys.exit(0)
        except BrokenPipeError:
            print("Exiting", file=sys.stderr)
        sys.stderr.close()
        sys.exit(0)


class StdinReader:
    """Stdin reader"""

    class raw(object):  # pylint: disable=invalid-name
        """Raw stdin input class"""

        def __init__(self, stream):
            self.stream = stream
            self.fd = self.stream.fileno()

        def __enter__(self):
            self.original_stty = termios.tcgetattr(self.stream)
            tty.setcbreak(self.stream)

        def __exit__(self, type_, value, traceback):
            termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

    class nonblocking(object):  # pylint: disable=invalid-name
        """Nonblocking input class"""

        def __init__(self, stream):
            self.stream = stream
            self.fd = self.stream.fileno()

        def __enter__(self):
            self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

        def __exit__(self, *args):
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


def main():
    # Handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--duration",
        default=5,
        help="set the duration in minutes each sound will play: default=5",
    )
    parser.add_argument(
        "-i",
        "--noinit",
        action="store_false",
        help="do not pre-initialize all sounds at start",
    )
    parser.add_argument(
        "-n", "--noinput", action="store_true", help="disable the stdin input capture"
    )
    parser.add_argument(
        "-p", "--path", default=None, help="set the path where the sound files are"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="produce no output")
    parser.add_argument(
        "-v", "--version", action="store_true", help="show version and exit"
    )
    parser.add_argument("paths", nargs="*", help="load given sound file(s) or path(s)")

    # Returns tuple of args and remaining (unhandled args)
    (args, _) = parser.parse_known_args(sys.argv[1:])

    # Display version and exit
    if args.version:
        print(AmbientSounds.get_version())
        sys.exit(0)

    # Determine paths to sounds
    if args.paths:
        sounds_paths = [os.path.abspath(path) for path in args.paths]
    else:
        sounds_paths = None
        if args.path:
            sounds_paths = [os.path.abspath(args.path)]

    # Initialize pygame
    pygame.init()

    # Initialize AmbientSounds
    ambience = AmbientSounds(
        paths=sounds_paths,
        duration=args.duration,
        noinput=args.noinput,
        quiet=args.quiet,
        initialize_sounds=args.noinit,
    )
    ambience.start()

    # This creates a timer event for the "tick" that will be passed to the
    # ambience class object. It is measured in milliseconds (1000 = 1 second)
    pygame.time.set_timer(AMBIENT_TICK, int(1000 / ambience.fps))

    # Event loop
    if ambience.noinput:
        ambience.event_loop()
    else:
        with StdinReader.raw(sys.stdin):
            with StdinReader.nonblocking(sys.stdin):
                ambience.event_loop()


if __name__ == "__main__":
    main()

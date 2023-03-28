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
import json
import os
import random
import sys
import termios
import time
import tty
from typing import Dict, List, Tuple

import pygame
from pygame.locals import (
    K_LEFTBRACKET,
    K_m,
    K_n,
    K_p,
    K_q,
    K_s,
    K_RIGHTBRACKET,
    USEREVENT,
)

AMBIENT_TICK = USEREVENT + 1
SOUND_LIBRARY = "ambience-library.json"


class AmbientSounds:
    """AmbientSounds class"""

    version = "1.0.13"

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
    sounds: Dict[int, pygame.mixer.Sound] = {}
    current_sound = 0
    animate_chars = "◐◓◑◒"
    animate_position = 0

    # Path and sound files
    paths: List[str] = []
    files: List[str] = []

    # Whether to listen to stdin in cli (experimental)
    noinput = False

    # Whether to silence output
    quiet = False

    # Volume
    volume = 1.0
    muted = False
    paused = False

    def __init__(
        self, paths=None, duration=5, noinput=False, quiet=False, initialize_sounds=True
    ):
        if paths:
            self.paths = paths
        else:
            self.paths = self.determine_default_sounds_dir()

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

        self.start_time = round(time.time())

    @classmethod
    def get_version(cls) -> str:
        return "Ambient version {}".format(cls.version)

    def determine_default_sounds_dir(self):
        # Use the default path in the ~/.ambience dir
        path = os.path.join(Library.get_home_path(".ambience"), "sounds")

        if not os.path.isdir(path):
            # Try the path where the package is
            package_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(package_path, "sounds")
            print()
            print("-" * 60)
            print("This package only comes with a few sounds to start.")
            print("Use ambience --fetch-library to download the full sound library.")
            print("-" * 60)

        return [path]

    def start(self) -> None:
        if len(self.files) == 0:
            print("No sound files to load!")
            print("Use ambience --fetch-library to download sound library.")
            pygame.quit()
            sys.exit(1)

        if not self.quiet:
            print("\r\nPlaying sounds. Press Ctrl-C to exit.", flush=True)
        if not self.noinput and not self.quiet:
            print("Press '[' and ']' to change volume and press 'm' to mute.")
            print(
                "Press 'n' to go to next sound, "
                "or 'p' to go to previous sound. Press 's' to pause and 'q' to quit.",
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

    def tick(self) -> None:
        if not self.paused:
            self.handle_play()
        if sys.stdout.isatty() and not self.quiet:
            self.print_current_sound()

    def print_current_sound(self) -> None:
        if self.paused:
            print("\r\033[K⏸ [paused] (Press 's' to unpause)", end="")
            return

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

        elapsed = round(time.time()) - self.start_time
        if elapsed > 60 * 60:
            elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        else:
            elapsed_str = time.strftime("%M:%S", time.gmtime(elapsed))

        print(
            "\r\033[K▶ Playing {} {} {} {}".format(
                sound_name, animate_char, volume_str, elapsed_str
            ),
            end="",
        )

    def handle_play(self) -> None:
        if self.play_timer > 0:
            self.play_timer = self.play_timer - 1
            if self.play_timer == min(10, int(self.play_duration / 2)):
                # Load the next sound a few ticks before we need to play it
                self.load_sound(self.get_next_sound())
        else:
            self.stop_sound(self.current_sound)
            self.start_next_sound()

    def start_next_sound(self, fade_override=None) -> None:
        self.current_sound = self.get_next_sound()

        self.play_sound(self.current_sound, fade_override)

    def get_next_sound(self) -> int:
        next_sound = self.current_sound + 1

        if next_sound >= len(self.files):
            next_sound = 0

        return next_sound

    def start_previous_sound(self, fade_override=None) -> None:
        self.current_sound = self.get_previous_sound()

        self.play_sound(self.current_sound, fade_override)

    def get_previous_sound(self) -> int:
        previous_sound = self.current_sound - 1

        if previous_sound < 0:
            previous_sound = len(self.files) - 1

        return previous_sound

    def next(self) -> None:
        self.paused = False
        self.load_sound(self.get_next_sound())
        self.stop_sound(self.current_sound, 2)
        self.start_next_sound(2)

    def previous(self) -> None:
        self.paused = False
        self.load_sound(self.get_previous_sound())
        self.stop_sound(self.current_sound, 2)
        self.start_previous_sound(2)

    def play_sound(self, index, fade_override=None) -> None:
        fade_duration, fade_ms = self._get_fade_duration(fade_override)

        self.load_sound(index)
        self.sounds[self.get_sound_id(index)].set_volume(self.volume)
        self.sounds[self.get_sound_id(index)].play(-1, fade_ms=fade_ms)
        self.play_timer = int(self.play_duration - (fade_duration / 2))

    def stop_sound(self, index, fade_override=None) -> None:
        _, fade_ms = self._get_fade_duration(fade_override)

        self.sounds[self.get_sound_id(index)].fadeout(fade_ms)

    def end_fadeout(self, duration=4000) -> None:
        if not self.quiet:
            print()
            print("Stopping sounds...", flush=True)
        pygame.mixer.fadeout(duration)
        pygame.time.wait(duration)
        print("Goodbye.", flush=True)

    def _get_fade_duration(self, fade_override=None) -> Tuple[int, int]:
        fade_duration = fade_override if fade_override else self.fade_duration
        fade_ms = int(fade_duration * (1000.0 / self.fps))
        return (fade_duration, fade_ms)

    def decrease_volume(self) -> None:
        self.volume = self.volume - 0.05
        self.volume = max(self.volume, 0.0)
        self.set_volume(self.volume)

    def increase_volume(self) -> None:
        self.volume = self.volume + 0.05
        self.volume = min(self.volume, 1.0)
        self.set_volume(self.volume)

    def set_volume(self, level) -> None:
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(level)

    def mute(self) -> None:
        self.muted = not self.muted
        if self.muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self.volume)

    def pause(self) -> None:
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

    def load_sound(self, file_index) -> None:
        if self.get_sound_id(file_index) not in self.sounds:
            try:
                self.sounds[self.get_sound_id(file_index)] = pygame.mixer.Sound(
                    file=self.files[file_index]
                )
            except pygame.error as e:
                # Remove this file so we skip trying to play it
                del self.files[file_index]
                print(
                    "\nERROR {} -- skipping sound '{}'.".format(
                        str(e), self.files[file_index]
                    )
                )

    def get_sound_id(self, file_index):
        try:
            _ = self.files[file_index]
        except IndexError:
            print("Error: cannot reference sound {}".format(file_index))
        return hashlib.md5(str(file_index).encode("utf-8")).hexdigest()[:6]

    def get_files(self, paths) -> List[str]:
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
            print("Use ambience --fetch-library to download sound library.")
            sys.exit(1)

        return files

    def get_files_from_path(self, path, max_files=64) -> List[str]:
        files = []
        for f in os.listdir(path):
            full = os.path.join(path, f)
            if os.path.isdir(full):
                files.extend(self.get_files_from_path(full))  # recurse
            if len(files) > max_files:
                break  # break if we have enough
            self.add_valid_file(full, files)
        return files

    def add_valid_file(self, path, files) -> None:
        patterns = ["*.ogg", "*.wav", "*.flac"]
        if any(fnmatch(path, pattern) for pattern in patterns):
            files.append(path)

    def load_sound_files(self) -> List[str]:
        if not self.quiet:
            print("Reading sounds from paths")
            for path in self.paths:
                print(" - {}".format(path))
            print("")

        files = self.get_files(self.paths)
        random.shuffle(files)

        if len(files) == 0:
            return files

        if not self.quiet:
            print("Sounds:")
            file_list = []
            for index, file in enumerate(files):
                # Clean up common ancestors in sound file paths
                for path in self.paths:
                    if path in file:
                        listed_sound = file.replace(path + os.sep, "")
                file_list.append("{}. {}".format(index + 1, listed_sound))
            self.print_file_list(file_list)

        return files

    def print_file_list(self, files) -> None:
        if len(files) > 20:
            widest = max(len(f) for f in files)
            template = "{:<X}{:<X}{:<}".replace("X", str(widest + 3))
            for a, b, c in zip(files[::3], files[1::3], files[2::3]):
                print(template.format(a, b, c))
        else:
            for file in files:
                print(file)

    def initialize_sounds(self) -> None:
        if not self.quiet:
            print("\nInitializing sounds ", end="", flush=True)
        for i, _ in enumerate(self.files):
            if not self.quiet:
                print(".", end="", flush=True)
            self.load_sound(i)

    def event_loop(self) -> None:
        while True:
            try:
                if self.noinput:
                    char = ""
                else:
                    char = sys.stdin.read(1)
                self.handle_events(char)
            except KeyboardInterrupt:
                self.the_end()

    def handle_events(self, char_input="") -> None:
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

    def handle_input(self, key_code) -> None:
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
        elif key_code == K_s:
            self.pause()

    def the_end(self) -> None:
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


class Library:
    """Handles the sound library functions"""

    package_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        """Initialize this class"""

        # The library path is where the sound files live
        self.library_dir = self.get_home_path(".ambience")
        if not os.path.isdir(self.library_dir):
            os.mkdir(self.library_dir)

        # The library file is the definition of the sound files in the official package
        # Each entry in the file has a filename and an md5 hash
        self.library_file = "{}/{}".format(self.package_path, SOUND_LIBRARY)

    def verify_library(self, verify_only=False):
        """Verify the location of sounds on disk matches expected library manifest"""

        print("Verifying sound library ", end="")

        self.missing = []
        self.needs_update = []
        self.cannot_validate = []

        with open(self.library_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for entry in data:
            self.verify_sound_entry(entry)
        print("")

        if len(self.missing) > 0:
            print("Missing {} file(s).".format(len(self.missing)))

        if len(self.needs_update) > 0:
            print("Files needing updates: {}".format(len(self.needs_update)))

        if not verify_only:
            self.fetch_files(self.missing)
            self.fetch_files(self.needs_update, "needing update")

    def verify_sound_entry(self, entry):
        """Verify a single sound entry from library manifest file"""

        if not entry.get("filename"):
            return None
        lib_filename = "{}/{}".format(self.library_dir, entry.get("filename"))
        if os.path.isfile(lib_filename):
            if entry.get("hash"):
                md5_hash = self.hash_file(lib_filename)
                if md5_hash == entry.get("hash"):
                    print(".", end="")
                else:
                    print("-", end="")
                    self.needs_update.append(entry.get("filename"))
            else:
                print("~", end="")
                self.cannot_validate.append(entry.get("filename"))
        else:
            print("M", end="")
            self.missing.append(entry.get("filename"))

        return True

    def hash_file(self, filename_):
        with open(filename_, "rb") as f_:
            content = f_.read()
            md5_hash = hashlib.md5(content)

        return md5_hash.hexdigest()

    def fetch_files(self, file_list, type_="missing"):
        if len(file_list) == 0:
            return 0

        import requests  # pylint: disable=import-outside-toplevel

        print("Fetching {} {} file(s).".format(len(file_list), type_))
        for filename in file_list:
            print(" >> {} ".format(filename), end="", flush=True)
            url = "https://github.com/sumpygump/ambient/raw/master/{}".format(filename)
            response = requests.get(url, timeout=60)
            print(response.status_code, end="")

            if response.status_code == 200:
                lib_filename = "{}/{}".format(self.library_dir, filename)
                print(" ->", lib_filename, end="")
                self.ensure_path(lib_filename)
                with open(lib_filename, "wb") as f:
                    f.write(response.content)

            print("", flush=True)
            time.sleep(0.08)  # Just to make sure we don't blow up Github with requests

    @classmethod
    def get_home_path(cls, path=""):
        """Get the home path for this user from the OS"""

        home = os.getenv("HOME")
        if home is None:
            home = os.getenv("USERPROFILE")

        if path:
            return "/".join((home, path))
        return home

    def ensure_path(self, path=""):
        """Ensure a path to the file exists (directories it belongs in)"""
        path = path.replace(self.library_dir, "").rstrip("/")

        segments = path.split("/")
        path_iteration = self.library_dir
        for segment in segments[:-1]:  # All but the last
            path_iteration = "/".join((path_iteration, segment))
            if not os.path.isdir(path_iteration):
                os.mkdir(path_iteration)


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
        "-f",
        "--fetch-library",
        action="store_true",
        help="fetch the sound library from internet",
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

    # Fetch/verify sound library
    if args.fetch_library:
        library = Library()
        library.verify_library()
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

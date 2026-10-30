"""Plays the real game with a fixed seed and scripted key presses, and records the terminal as frames.

The game runs unchanged: its output goes into a pyte terminal emulator, `cls` becomes an ANSI clear,
time.sleep advances a virtual clock instead of waiting, and input() types the next scripted answer.

usage: python tools/record_terminal.py <frames.pkl> --inputs "Ayla|1|1|1|1" [--seed 7] [--cols 80 --rows 40]
  --text   print the screen at every prompt instead of recording (to plan the inputs)
Needs: pyte. Run from the repository root.
"""
import argparse, builtins, os, pickle, random, sys, tempfile, time

import pyte

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--inputs", required=True)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--cols", type=int, default=80)
ap.add_argument("--rows", type=int, default=40)
ap.add_argument("--text", action="store_true")
a = ap.parse_args()
a.out = os.path.abspath(a.out)  # the game runs in a temp dir (see chdir below)

CODE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code")
screen = pyte.Screen(a.cols, a.rows)
stream = pyte.Stream(screen)
answers = a.inputs.split("|")
frames, clock, last = [], 0.0, -1.0

def snap(hold=0.0):
    """Store the current screen; `hold` is extra seconds to show it."""
    global last
    rows = [[(c.data, c.fg, c.bg, c.bold) for c in (screen.buffer[y][x] for x in range(a.cols))] for y in range(a.rows)]
    frames.append({"t": clock, "hold": hold, "rows": rows, "cursor": (screen.cursor.x, screen.cursor.y)})
    last = clock

class Term:
    encoding = "utf-8"
    def write(self, s):
        stream.feed(s.replace("\n", "\r\n"))
        return len(s)
    def flush(self): pass
    def isatty(self): return True

def fake_sleep(sec):
    global clock
    clock += sec
    if clock - last >= 0.07:  # about 14 frames per virtual second is enough for typing effects
        snap()

def fake_system(cmd):
    if cmd in ("cls", "clear"):
        stream.feed("\x1b[2J\x1b[H")
    return 0

def fake_input(prompt=""):
    global clock
    sys.stdout.write(prompt)
    if not answers:
        raise SystemExit
    if a.text:
        sys.__stdout__.write("\n".join(screen.display).rstrip() + f"\n----- answer: {answers[0]!r}\n")
    snap(hold=0.7)
    answer = answers.pop(0)
    for ch in answer:
        sys.stdout.write(ch); clock += 0.09; snap()
    sys.stdout.write("\n")
    return answer

random.seed(a.seed)
sys.path.insert(0, CODE)
os.chdir(tempfile.mkdtemp())  # no savegame.dat here, so the game always starts fresh
sys.stdout = Term()
time.sleep = fake_sleep
os.system = fake_system
builtins.input = fake_input

import utils
utils._SOUND_AVAILABLE = False
import main as game

try:
    game.Game().start()
except SystemExit:
    pass
snap(hold=1.5)
sys.stdout = sys.__stdout__
if not a.text:
    with open(a.out, "wb") as f:
        pickle.dump({"cols": a.cols, "rows": a.rows, "frames": frames}, f)
print(len(frames), "frames, virtual time", round(clock, 1), "s")

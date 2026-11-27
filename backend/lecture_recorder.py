"""
Lecture recorder
================
Three parts, each one a menu option in main.py:

  (3) Record a lecture
      Start it at the beginning of the lecture. While it records you can type
      a note and press ENTER to save it at that point in the lecture.
      Type "stop" and press ENTER at the end.

  (4) Make transcripts
      Turn recordings into transcripts later, when you have time:
      one recording, every recording from a day, a week, or everything not done yet.

  (5) Add notes to a recording
      Add notes afterwards at a time in the lecture (e.g. "34:10 this is on the exam").

    python backend/lecture_recorder.py               (record)
    python backend/lecture_recorder.py --transcripts (make transcripts)
    python backend/lecture_recorder.py --notes       (add notes)

Everything is saved in the recordings/ folder (not committed to git):
    recordings/CS1115_24_november_2026.flac       - the audio
    recordings/CS1115_24_november_2026.notes.txt  - your notes, with [mm:ss] times
    recordings/CS1115_24_november_2026.txt        - the transcript, with your notes mixed in

Transcription uses Whisper (faster-whisper), which runs on this laptop,
for free, with no internet needed after the first run (it downloads the
model once, about 500MB for "small").
"""

import argparse
import ctypes
import datetime
import os
import queue
import re
import sys
import threading
import time

import numpy as np
import sounddevice as sd
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDINGS = os.path.join(ROOT, "recordings")

# Whisper models. Option 4 asks which one to use.
# "small.en" is a good balance on a laptop CPU (about 10-20 minutes per hour of lecture).
# "medium.en" gets more words right, but is 2-3 times slower (and downloads about 1.5GB the first time).
MODEL = "small.en"
ACCURATE_MODEL = "medium.en"

# Words Whisper wouldn't guess on its own, per module. Helps it spell them right.
VOCAB = {
    "CS1106": "SQL, SELECT, FROM, WHERE, JOIN, GROUP BY, HAVING, subquery, primary key, foreign key, ER diagram, normalisation, Kieran Herley",
    "CS1111": "Samphire, assembly, register, AL, BL, CL, DL, opcode, mnemonic, endian, cache, DRAM, SRAM, virtual memory, page frame, MMU, hypervisor, J.P. Morrison",
    "CS1112": "set, subset, union, intersection, cardinality, power set, relation, reflexive, symmetric, transitive, bijective, tautology, implication, Barry O'Sullivan",
    "CS1115": "Derek Bridge. HTML, CSS, selector, pseudo-class, pseudo-element, links, :hover, :link, :visited, :active, nav, anchor, "
              "page jumps, scroll-behavior, scroll-margin-top, @media, @font-face, @ rules, user agent stylesheet, rows, tr, td, th, "
              "border-collapse, nth-child, zebra striping, flexbox, grid, margin, padding, div, span, viewport, rem, em, float, "
              "shape-outside, position: relative, absolute, fixed, sticky, transform, scale, rotate, transition, ease-in, ease-out, "
              "linear, cubic-bezier, animation, @keyframes, caniuse.com, screen reader",
    "CS1117": "Python, list, tuple, dictionary, set, function, loop, match, return, parameter",
    "MA1001": "calculus, derivative, integral, limit, chain rule, product rule, quotient rule, tangent, logarithm, critical point, differential equation",
}

NOTE_MARK = ">> MY NOTE:"  # how your notes show up in the transcript

# Windows: stop the laptop going to sleep while recording or transcribing
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def keep_awake(on):
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0)
        )


## ============================== FILES AND TIMES ==============================

RECORDING_NAME = re.compile(r"^([A-Za-z]{2}\d{4})_(\d{1,2})_([a-z]+)_(\d{4})(?:_(\d+))?\.flac$")


def recording_date(filename):
    # CS1115_24_november_2026.flac -> date(2026, 11, 24)
    match = RECORDING_NAME.match(filename)
    if not match:
        return None
    try:
        return datetime.datetime.strptime(f"{match.group(2)} {match.group(3)} {match.group(4)}", "%d %B %Y").date()
    except ValueError:
        return None


def all_recordings():
    # Every recording, oldest first: (date, filename, full path)
    if not os.path.isdir(RECORDINGS):
        return []
    found = []
    for name in os.listdir(RECORDINGS):
        if name.endswith(".flac"):
            found.append((recording_date(name) or datetime.date.min, name, os.path.join(RECORDINGS, name)))
    return sorted(found)


def transcript_path(path):
    return os.path.splitext(path)[0] + ".txt"


def notes_path(path):
    return os.path.splitext(path)[0] + ".notes.txt"


def is_transcribed(path):
    return os.path.exists(transcript_path(path))


def stamp(seconds):
    seconds = int(seconds)
    return f"[{seconds // 60:02d}:{seconds % 60:02d}]"


def parse_time(text):
    # "34:10" or "1:02:05" -> seconds
    parts = text.strip("[] ").split(":")
    if not 2 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        return None
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + int(p)
    return seconds


def read_notes(path):
    # [(seconds, text), ...] from the .notes.txt file
    notes = []
    if os.path.exists(notes_path(path)):
        with open(notes_path(path), encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^\[([\d:]+)\]\s*(.*)$", line.strip())
                if match and parse_time(match.group(1)) is not None and match.group(2):
                    notes.append((parse_time(match.group(1)), match.group(2)))
    return sorted(notes)


def save_note(path, seconds, text):
    # Saved straight away, one line per note, so nothing is lost if something crashes
    with open(notes_path(path), "a", encoding="utf-8") as f:
        f.write(f"{stamp(seconds)} {text}\n")


def ask_date(prompt):
    # Accepts 26/11, 26/11/2026 or blank for today
    while True:
        text = input(prompt).strip()
        if not text:
            return datetime.date.today()
        parts = text.replace("-", "/").replace(".", "/").split("/")
        try:
            day, month = int(parts[0]), int(parts[1])
            year = int(parts[2]) if len(parts) > 2 else datetime.date.today().year
            if year < 100:
                year += 2000
            return datetime.date(year, month, day)
        except (ValueError, IndexError):
            print("  Type a date like 26/11 (or just press ENTER for today)")


def pick_recording(prompt):
    recordings = all_recordings()
    if not recordings:
        print("No recordings yet.")
        return None
    for i, (_, name, path) in enumerate(recordings, 1):
        done = "transcribed" if is_transcribed(path) else "not transcribed"
        notes = len(read_notes(path))
        print(f"  {i:>2}. {name}  ({done}{f', {notes} note' + ('s' if notes != 1 else '') if notes else ''})")
    while True:
        choice = input(prompt).strip()
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(recordings):
            return recordings[int(choice) - 1][2]
        print(f"  Type a number from 1 to {len(recordings)} (or press ENTER to go back)")


## ============================== (3) RECORD ==============================

def module_folders():
    return sorted(
        d for d in os.listdir(ROOT)
        if len(d) == 6 and d[:2].isalpha() and d[2:].isdigit() and os.path.isdir(os.path.join(ROOT, d))
    )


def pick_module():
    modules = module_folders()
    print("Which module is this?")
    for i, m in enumerate(modules, 1):
        print(f"  {i}. {m}")
    while True:
        choice = input("Number (or type a module code): ").strip().upper()
        if choice.isdigit() and 1 <= int(choice) <= len(modules):
            return modules[int(choice) - 1]
        if choice:
            return choice


def new_filename(module):
    today = datetime.date.today()
    base = f"{module}_{today.day}_{today.strftime('%B').lower()}_{today.year}"
    name, n = base, 2
    while os.path.exists(os.path.join(RECORDINGS, name + ".flac")):
        name = f"{base}_{n}"  # two lectures of the same module on one day
        n += 1
    return os.path.join(RECORDINGS, name + ".flac")


def record(path):
    device = sd.query_devices(kind="input")
    rate = int(device["default_samplerate"])
    chunks = queue.Queue()
    level = [0.0]
    stop = threading.Event()
    typed = queue.Queue()  # finished lines you typed (notes, or "stop")

    def callback(indata, frames, time_info, status):
        chunks.put(indata.copy())
        level[0] = float(np.abs(indata).max())

    # In a normal window, read keys one at a time so typing a note doesn't mess up
    # the timer line. Otherwise (e.g. input piped in), read whole lines.
    use_keys = sys.platform == "win32" and sys.stdin.isatty()
    if use_keys:
        import msvcrt

    def read_lines():
        while True:
            try:
                line = input()
            except EOFError:
                typed.put("stop")
                return
            typed.put(line if line.strip() else "stop")

    print(f"\nMic: {device['name']}")
    print("RECORDING...")
    print("  Type a note and press ENTER to save it at this point in the lecture")
    print("  Type stop and press ENTER at the end of the lecture\n")
    keep_awake(True)
    if not use_keys:
        threading.Thread(target=read_lines, daemon=True).start()

    try:
        width = os.get_terminal_size().columns - 1  # one line, so it never wraps
    except OSError:
        width = 100
    written = 0
    note_count = 0
    buffer = ""
    flash, flash_until = "", 0.0

    # Written straight to disk as it records (not held in memory), so long lectures are fine
    try:
        with sf.SoundFile(path, mode="w", samplerate=rate, channels=1, format="FLAC") as f, \
             sd.InputStream(samplerate=rate, channels=1, dtype="float32", callback=callback):
            while not stop.is_set():
                while not chunks.empty():
                    chunk = chunks.get()
                    f.write(chunk)
                    written += len(chunk)

                if use_keys:
                    while msvcrt.kbhit():
                        ch = msvcrt.getwch()
                        if ch in ("\r", "\n"):
                            typed.put(buffer)
                            buffer = ""
                        elif ch == "\b":
                            buffer = buffer[:-1]
                        elif ch in ("\x00", "\xe0"):
                            msvcrt.getwch()  # arrow keys etc. come as two characters, ignore them
                        elif ch == "\x03":
                            raise KeyboardInterrupt
                        elif ch.isprintable():
                            buffer += ch

                while not typed.empty():
                    line = typed.get().strip()
                    if line.lower() == "stop":
                        stop.set()
                    elif line:
                        seconds = written / rate
                        save_note(path, seconds, line)
                        note_count += 1
                        flash, flash_until = f"note saved at {stamp(seconds)}", time.time() + 3

                elapsed = int(written / rate)
                bars = "#" * min(20, int(level[0] * 40))
                status = f"  {elapsed // 3600}:{elapsed // 60 % 60:02d}:{elapsed % 60:02d}  mic [{bars:<20}]"
                if time.time() < flash_until:
                    status += f"  ({flash})"
                if use_keys:
                    status += "  note> "
                    # Show the end of what you're typing if it's longer than the window
                    room = max(10, width - len(status))
                    status += buffer[-room:]
                print("\r" + status[:width].ljust(width), end="", flush=True)
                time.sleep(0.1)

            while not chunks.empty():
                chunk = chunks.get()
                f.write(chunk)
                written += len(chunk)
    except KeyboardInterrupt:
        pass  # Ctrl+C also stops it, and the file is still saved
    finally:
        keep_awake(False)

    if os.path.getsize(path) == 0 or written == 0:
        os.remove(path)
        print("\n\nStopped before any audio was recorded, so nothing was saved.")
        return False

    seconds = written / rate
    print(f"\n\nStopped. Saved {int(seconds // 60)}m {int(seconds % 60)}s of audio to {os.path.relpath(path, ROOT)}")
    if note_count:
        print(f"Saved {note_count} note{'s' if note_count != 1 else ''} to {os.path.relpath(notes_path(path), ROOT)}")
    print("Make the transcript later with option 4 (Make transcripts).")
    return True


def run_recorder():
    os.makedirs(RECORDINGS, exist_ok=True)
    module = pick_module()
    record(new_filename(module))


## ============================== (4) TRANSCRIBE ==============================

def load_audio(path):
    # Whisper wants 16kHz mono. Loading it here (instead of letting faster-whisper
    # do it) avoids its dependency on the "av" package, which breaks between versions.
    audio, rate = sf.read(path, dtype="float32", always_2d=True)
    audio = audio.mean(axis=1)
    if rate != 16000:
        old = np.arange(len(audio)) / rate
        new = np.arange(int(len(audio) * 16000 / rate)) / 16000
        audio = np.interp(new, old, audio).astype(np.float32)
    return audio


def write_transcript(path, lines):
    # lines = [(seconds, text)] from Whisper. Your notes get mixed in at their times.
    notes = [(seconds, f"{NOTE_MARK} {text}") for seconds, text in read_notes(path)]
    merged = sorted(lines + notes, key=lambda item: (item[0], item[1].startswith(NOTE_MARK)))
    with open(transcript_path(path), "w", encoding="utf-8") as f:
        f.write(f"Transcript of {os.path.basename(path)}\n\n")
        for seconds, text in merged:
            f.write(f"{stamp(seconds)} {text}\n")


def read_transcript_lines(path):
    # The Whisper lines from an existing transcript (without your notes), so notes can be re-merged
    lines = []
    with open(transcript_path(path), encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\[([\d:]+)\]\s(.*)$", line.rstrip("\n"))
            if match and not match.group(2).startswith(NOTE_MARK):
                lines.append((parse_time(match.group(1)), match.group(2)))
    return lines


_models = {}


def get_model(name=MODEL):
    if name not in _models:
        from faster_whisper import WhisperModel
        print(f"Loading Whisper ({name})... the first time, this downloads the model.")
        _models[name] = WhisperModel(name, device="cpu", compute_type="int8")
    return _models[name]


def remove_repeats(lines):
    # Whisper sometimes gets stuck saying the same thing over and over (e.g. "This..." 20 times).
    # Keep the first one of any run of identical lines.
    kept = []
    for seconds, text in lines:
        same = text.strip(" .").lower()
        if kept and same == kept[-1][1].strip(" .").lower():
            continue
        kept.append((seconds, text))
    return kept


def transcribe(path, model_name=MODEL):
    module = os.path.basename(path).split("_")[0].upper()
    model = get_model(model_name)

    speed = "10-20" if model_name == MODEL else "30-50"
    print(f"Transcribing {os.path.basename(path)} with {model_name} (roughly {speed} minutes for an hour of lecture)...")
    segments, info = model.transcribe(
        load_audio(path),
        language="en",
        vad_filter=True,  # skip silence
        initial_prompt=VOCAB.get(module),
        # Don't feed each line into the next one. Stops one mistake turning into a loop.
        condition_on_previous_text=False,
    )

    lines = []
    keep_awake(True)
    try:
        for seg in segments:
            lines.append((int(seg.start), seg.text.strip()))
            done = seg.end / info.duration * 100 if info.duration else 0
            print(f"\r  {done:5.1f}% done", end="", flush=True)
    finally:
        keep_awake(False)

    write_transcript(path, remove_repeats(lines))
    print(f"\r  Transcript saved to {os.path.relpath(transcript_path(path), ROOT)}")
    return transcript_path(path)


def transcribe_many(paths, label, model_name=MODEL):
    if not paths:
        print(f"No recordings found for {label}.")
        return

    done_already = [p for p in paths if is_transcribed(p)]
    if done_already:
        print(f"{len(done_already)} of these already have a transcript.")
        if input("Redo them too? (y/N): ").strip().lower() != "y":
            paths = [p for p in paths if p not in done_already]
    if not paths:
        print("Nothing left to transcribe.")
        return

    print(f"\nTranscribing {len(paths)} recording{'s' if len(paths) != 1 else ''} for {label}:")
    for p in paths:
        print(f"  - {os.path.basename(p)}")
    print()
    for i, p in enumerate(paths, 1):
        print(f"({i}/{len(paths)}) ", end="")
        transcribe(p, model_name)
    print("\nAll done.")


def run_transcripts():
    os.makedirs(RECORDINGS, exist_ok=True)
    recordings = all_recordings()
    if not recordings:
        print("No recordings yet. Record a lecture first (option 3).")
        return

    waiting = [p for _, _, p in recordings if not is_transcribed(p)]
    print(f"{len(recordings)} recording{'s' if len(recordings) != 1 else ''}, {len(waiting)} not transcribed yet.\n")
    print("Make transcripts for:")
    print("  1. One lecture")
    print("  2. A day")
    print("  3. A week")
    print("  4. Everything not transcribed yet")
    choice = input("Number: ").strip()
    if choice not in ("1", "2", "3", "4"):
        print("Not an option.")
        return

    print("\nWhich quality?")
    print(f"  1. Normal   ({MODEL}, about 10-20 minutes per hour of lecture)")
    print(f"  2. Accurate ({ACCURATE_MODEL}, gets more words right, about 30-50 minutes per hour)")
    model_name = ACCURATE_MODEL if input("Number (ENTER for normal): ").strip() == "2" else MODEL

    if choice == "1":
        path = pick_recording("Which recording? ")
        if path:
            transcribe(path, model_name)

    elif choice == "2":
        day = ask_date("Which day? (e.g. 26/11, or ENTER for today): ")
        paths = [p for d, _, p in recordings if d == day]
        transcribe_many(paths, day.strftime("%A %d %B"), model_name)

    elif choice == "3":
        day = ask_date("Any day in the week (e.g. 26/11, or ENTER for this week): ")
        monday = day - datetime.timedelta(days=day.weekday())
        sunday = monday + datetime.timedelta(days=6)
        paths = [p for d, _, p in recordings if monday <= d <= sunday]
        transcribe_many(paths, f"the week of {monday.strftime('%d %B')} - {sunday.strftime('%d %B')}", model_name)

    elif choice == "4":
        transcribe_many(waiting, "everything not transcribed yet", model_name)


## ============================== (5) NOTES ==============================

def run_notes():
    print("Add notes to which recording?")
    path = pick_recording("Number (or ENTER to go back): ")
    if not path:
        return

    notes = read_notes(path)
    if notes:
        print("\nNotes so far:")
        for seconds, text in notes:
            print(f"  {stamp(seconds)} {text}")

    print("\nType the time in the lecture and your note, e.g.  34:10 this is on the exam")
    print("Press ENTER on an empty line when you're done.\n")
    added = 0
    while True:
        line = input("note> ").strip()
        if not line:
            break
        time_text, _, text = line.partition(" ")
        seconds = parse_time(time_text)
        if seconds is None or not text.strip():
            print("  Start with the time, e.g.  34:10 your note")
            continue
        save_note(path, seconds, text.strip())
        added += 1

    if not added:
        return
    print(f"\nSaved {added} note{'s' if added != 1 else ''}.")
    if is_transcribed(path):
        write_transcript(path, read_transcript_lines(path))
        print(f"Added them into {os.path.relpath(transcript_path(path), ROOT)}")
    else:
        print("They'll be added into the transcript when you make it (option 4).")


## ============================== COMMAND LINE ==============================

def main():
    parser = argparse.ArgumentParser(description="Record lectures, make transcripts and add notes.")
    parser.add_argument("--transcripts", action="store_true", help="make transcripts from recordings")
    parser.add_argument("--notes", action="store_true", help="add notes to a recording")
    args = parser.parse_args()

    if args.transcripts:
        run_transcripts()
    elif args.notes:
        run_notes()
    else:
        run_recorder()


if __name__ == "__main__":
    main()

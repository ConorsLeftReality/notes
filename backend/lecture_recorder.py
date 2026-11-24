"""
Lecture recorder
================
Start it at the beginning of a lecture, press ENTER at the end,
and it saves the audio and writes a transcript.

    python backend/lecture_recorder.py                 (record, then transcribe)
    python backend/lecture_recorder.py --transcribe F  (only transcribe an existing recording F)

Everything is saved in the recordings/ folder (not committed to git):
    recordings/CS1115_24_november_2026.flac   - the audio
    recordings/CS1115_24_november_2026.txt    - the transcript, with [mm:ss] timestamps

Transcription uses Whisper (faster-whisper), which runs on this laptop,
for free, with no internet needed after the first run (it downloads the
model once, about 500MB for "small").
"""

import argparse
import ctypes
import datetime
import os
import queue
import sys
import threading
import time

import numpy as np
import sounddevice as sd
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDINGS = os.path.join(ROOT, "recordings")

# Whisper model: "small.en" is a good balance on a laptop CPU.
# "base.en" is faster but makes more mistakes, "medium.en" is better but much slower.
MODEL = "small.en"

# Words Whisper wouldn't guess on its own, per module. Helps it spell them right.
VOCAB = {
    "CS1106": "SQL, SELECT, FROM, WHERE, JOIN, GROUP BY, HAVING, subquery, primary key, foreign key, ER diagram, normalisation, Kieran Herley",
    "CS1111": "Samphire, assembly, register, AL, BL, CL, DL, opcode, mnemonic, endian, cache, DRAM, SRAM, virtual memory, page frame, MMU, hypervisor, J.P. Morrison",
    "CS1112": "set, subset, union, intersection, cardinality, power set, relation, reflexive, symmetric, transitive, bijective, tautology, implication, Barry O'Sullivan",
    "CS1115": "HTML, CSS, selector, flexbox, grid, margin, padding, div, span, viewport, rem, em, float, shape-outside, Derek Bridge",
    "CS1117": "Python, list, tuple, dictionary, set, function, loop, match, return, parameter",
    "MA1001": "calculus, derivative, integral, limit, chain rule, product rule, quotient rule, tangent, logarithm, critical point, differential equation",
}

# Windows: stop the laptop going to sleep while recording
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def keep_awake(on):
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0)
        )


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

    def callback(indata, frames, time_info, status):
        chunks.put(indata.copy())
        level[0] = float(np.abs(indata).max())

    def wait_for_enter():
        try:
            input()
        except EOFError:
            pass
        stop.set()

    print(f"\nMic: {device['name']}")
    print("RECORDING... press ENTER to stop.\n")
    keep_awake(True)
    start = time.time()
    threading.Thread(target=wait_for_enter, daemon=True).start()

    # Written straight to disk as it records (not held in memory), so long lectures are fine
    written = 0
    try:
        with sf.SoundFile(path, mode="w", samplerate=rate, channels=1, format="FLAC") as f, \
             sd.InputStream(samplerate=rate, channels=1, dtype="float32", callback=callback):
            while not stop.is_set():
                while not chunks.empty():
                    chunk = chunks.get()
                    f.write(chunk)
                    written += len(chunk)
                elapsed = int(time.time() - start)
                bars = "#" * min(30, int(level[0] * 60))
                print(f"\r  {elapsed // 3600}:{elapsed // 60 % 60:02d}:{elapsed % 60:02d}  mic [{bars:<30}]", end="", flush=True)
                time.sleep(0.2)
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
    return True


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


def transcribe(path):
    from faster_whisper import WhisperModel

    module = os.path.basename(path).split("_")[0].upper()
    out = os.path.splitext(path)[0] + ".txt"

    print(f"\nLoading Whisper ({MODEL})... the first time, this downloads the model.")
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")

    print("Transcribing (roughly 10-20 minutes for an hour of lecture)...")
    segments, info = model.transcribe(
        load_audio(path),
        language="en",
        vad_filter=True,  # skip silence
        initial_prompt=VOCAB.get(module),
    )

    keep_awake(True)
    try:
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"Transcript of {os.path.basename(path)}\n\n")
            for seg in segments:
                stamp = f"[{int(seg.start) // 60:02d}:{int(seg.start) % 60:02d}]"
                f.write(f"{stamp} {seg.text.strip()}\n")
                f.flush()
                done = seg.end / info.duration * 100 if info.duration else 0
                print(f"\r  {done:5.1f}% done", end="", flush=True)
    finally:
        keep_awake(False)

    print(f"\n\nTranscript saved to {os.path.relpath(out, ROOT)}")
    return out


def run_recorder():
    # Pick the module, record until ENTER, then transcribe. Also used by option 3 in main.py
    os.makedirs(RECORDINGS, exist_ok=True)
    module = pick_module()
    path = new_filename(module)
    if record(path):
        transcribe(path)


def main():
    parser = argparse.ArgumentParser(description="Record a lecture and transcribe it.")
    parser.add_argument("--transcribe", metavar="FILE", help="only transcribe an existing recording")
    args = parser.parse_args()

    if args.transcribe:
        os.makedirs(RECORDINGS, exist_ok=True)
        transcribe(args.transcribe)
        return

    run_recorder()


if __name__ == "__main__":
    main()

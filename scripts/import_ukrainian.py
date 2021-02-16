#!/usr/bin/env python
"""
This script transforms custom dataset, gathered from Internet into 
DeepSpeech-ready .csv file
Use "python3 import_ukrainian.py -h" for help
"""
import csv
import os
import subprocess
import unicodedata
from multiprocessing import Pool

import progressbar
import sox

from deepspeech_training.util.downloader import SIMPLE_BAR
from deepspeech_training.util.importers import (
    get_counter,
    get_imported_samples,
    get_importers_parser,
    get_validate_label,
    print_import_report,
)
from ds_ctcdecoder import Alphabet

FIELDNAMES = ["wav_filename", "wav_filesize", "transcript"]
SAMPLE_RATE = 16000
CHANNELS = 1
MAX_SECS = 10
PARAMS = None
FILTER_OBJ = None
AUDIO_DIR = None


class LabelFilter:
    def __init__(self, normalize, alphabet, validate_fun):
        self.normalize = normalize
        self.alphabet = alphabet
        self.validate_fun = validate_fun

    def filter(self, label):
        if self.normalize:
            label = unicodedata.normalize("NFKD", label.strip()).encode(
                "ascii", "ignore").decode("ascii", "ignore")
        label = self.validate_fun(label)
        if self.alphabet and label and not self.alphabet.CanEncode(label):
            label = None
        return label


def init_worker(params):
    global FILTER_OBJ  # pylint: disable=global-statement
    global AUDIO_DIR  # pylint: disable=global-statement
    AUDIO_DIR = params.audio_dir if params.audio_dir else os.path.join(
        params.tsv_dir, "clips")
    validate_label = get_validate_label(params)
    alphabet = Alphabet(
        params.filter_alphabet) if params.filter_alphabet else None
    FILTER_OBJ = LabelFilter(params.normalize, alphabet, validate_label)


def one_sample(sample):
    """ Take an audio file, and optionally convert it to 16kHz WAV """
    global AUDIO_DIR
    source_filename = sample[0]
    if not os.path.splitext(source_filename.lower())[1] == ".wav":
        source_filename += ".wav"
    # Storing wav files next to the mp3 ones - just with a different suffix
    output_filename = f"{sample[2]}.wav"
    output_filepath = os.path.join(AUDIO_DIR, output_filename)
    _maybe_convert_wav(source_filename, output_filepath)
    file_size = -1
    frames = 0
    if os.path.exists(output_filepath):
        file_size = os.path.getsize(output_filepath)
        if file_size == 0:
            frames = 0
        else:
            frames = int(
                subprocess.check_output(
                    ["soxi", "-s", output_filepath], stderr=subprocess.STDOUT
                )
            )
    label = FILTER_OBJ.filter(sample[1])
    rows = []
    counter = get_counter()
    if file_size == -1:
        # Excluding samples that failed upon conversion
        counter["failed"] += 1
    elif label is None:
        # Excluding samples that failed on label validation
        counter["invalid_label"] += 1
    # + 1 added for filtering surname dataset with too short audio files
    elif int(frames / SAMPLE_RATE * 1000 / 10 / 2) < len(str(label)) + 1:
        # Excluding samples that are too short to fit the transcript
        counter["too_short"] += 1
    elif frames / SAMPLE_RATE > MAX_SECS:
        # Excluding very long samples to keep a reasonable batch-size
        counter["too_long"] += 1
    else:
        # This one is good - keep it for the target CSV
        rows.append((os.path.split(output_filename)
                     [-1], file_size, label, sample[2]))
        counter["imported_time"] += frames
    counter["all"] += 1
    counter["total_time"] += frames

    return (counter, rows)


def _maybe_convert_set(dataset_dir, audio_dir, filter_obj, space_after_every_character=None, rows=None):
    # iterate over all data lists and write converted version near them
    speaker_iterator = 1

    samples = []
    for subdir, dirs, files in os.walk(dataset_dir):
        for file in files:
            # Get audiofile path and transcript for each sentence in tsv
            if file == "txt.final.data":
                file_path = os.path.join(subdir, file)
                file = open(file_path, mode="r")
                data = []
                for row in file.readlines():
                    file_name, transcript = row.replace(
                        " \n", "").split(" ", 1)

                    if file_name.endswith(".wav"):
                        pass
                    elif file_name.endswith(".mp3"):
                        pass
                    elif file_name.find(".") == -1:
                        file_name += ".wav"
                    file_name = os.path.join(os.path.join(
                        os.path.dirname(subdir), "wav"), file_name)
                    data.append(
                        (file_name, transcript, speaker_iterator))
                    speaker_iterator += 1

                file.close()

                samples += data

    if rows is None:
        rows = []
        counter = get_counter()
        num_samples = len(samples)
        print("Importing dataset files...")
        pool = Pool(initializer=init_worker, initargs=(PARAMS,))
        bar = progressbar.ProgressBar(
            max_value=num_samples, widgets=SIMPLE_BAR)
        for i, processed in enumerate(pool.imap_unordered(one_sample, samples), start=1):
            counter += processed[0]
            rows += processed[1]
            bar.update(i)
        bar.update(num_samples)
        pool.close()
        pool.join()

        imported_samples = get_imported_samples(counter)
        assert counter["all"] == num_samples
        assert len(rows) == imported_samples
        print_import_report(counter, SAMPLE_RATE, MAX_SECS)

    output_csv = os.path.join(os.path.abspath(audio_dir),  "train.csv")
    print("Saving new DeepSpeech-formatted CSV file to: ", output_csv)
    with open(output_csv, "w", encoding="utf-8", newline="") as output_csv_file:
        print("Writing CSV file for DeepSpeech.py as: ", output_csv)
        writer = csv.DictWriter(output_csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        bar = progressbar.ProgressBar(max_value=len(rows), widgets=SIMPLE_BAR)
        for filename, file_size, transcript, speaker in bar(rows):
            if space_after_every_character:
                writer.writerow(
                    {
                        "wav_filename": filename,
                        "wav_filesize": file_size,
                        "transcript": " ".join(transcript),
                    }
                )
            else:
                writer.writerow(
                    {
                        "wav_filename": filename,
                        "wav_filesize": file_size,
                        "transcript": transcript,
                    }
                )
    return rows


def _preprocess_data(tsv_dir, audio_dir, space_after_every_character=False):
    set_samples = _maybe_convert_set(
        tsv_dir, audio_dir, space_after_every_character)


def _maybe_convert_wav(mp3_filename, wav_filename):
    if not os.path.exists(wav_filename):
        transformer = sox.Transformer()
        transformer.convert(samplerate=SAMPLE_RATE, n_channels=CHANNELS)
        try:
            transformer.build(mp3_filename, wav_filename)
        except Exception as e: # TODO: improve exception handling
            pass


def parse_args():
    parser = get_importers_parser(
        description="Import CommonVoice v2.0 corpora")
    parser.add_argument("tsv_dir", help="Directory containing tsv files")
    parser.add_argument(
        "--audio_dir",
        help='Directory containing the audio clips - defaults to "<tsv_dir>/clips"',
    )
    parser.add_argument(
        "--filter_alphabet",
        help="Exclude samples with characters not in provided alphabet",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Converts diacritic characters to their base ones",
    )
    parser.add_argument(
        "--space_after_every_character",
        action="store_true",
        help="To help transcript join by white space",
    )
    return parser.parse_args()


def main():
    audio_dir = PARAMS.audio_dir if PARAMS.audio_dir else os.path.join(
        PARAMS.tsv_dir, "clips")
    _preprocess_data(PARAMS.tsv_dir, audio_dir,
                     PARAMS.space_after_every_character)


if __name__ == "__main__":
    PARAMS = parse_args()
    main()

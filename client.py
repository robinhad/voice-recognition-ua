#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import sys
import wave

from deepspeech import Model, version
from timeit import default_timer as timer


uk_model = Model("./uk.tflite")
en_model = Model("./deepspeech-0.7.3-models.tflite")


def client(audio_file, lang="uk"):
    model_load_start = timer()
    # sphinx-doc: python_ref_model_start
    model = uk_model
    if lang not in ["en", "uk"]:
        lang = "uk"
    if lang == "uk":
        model = uk_model
    if lang == "en":
        model = en_model

    ds = model
    # sphinx-doc: python_ref_model_stop
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    desired_sample_rate = ds.sampleRate()

    fin = wave.open(audio_file, 'rb')
    fs_orig = fin.getframerate()
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/fs_orig)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    # sphinx-doc: python_ref_inference_start

    result = ds.stt(audio)
    print(result)
    # sphinx-doc: python_ref_inference_stop
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' %
          (inference_end, audio_length), file=sys.stderr)
    return result

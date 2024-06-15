#!/usr/bin/python3

from simple_diarizer.diarizer import Diarizer
from simple_diarizer.utils import (check_wav_16khz_mono, convert_wavfile,
                                   waveplot, combined_waveplot, waveplot_perspeaker)

import sys

import soundfile as sf

NUM_SPEAKERS = 2 # The number of speakers
indir = '/datalake/resample/'
outdir = '/datalake/diar/'

for FileId in sys.argv[1:]:
    wav_file = f"{indir}/{FileId}.wav"
    signal, fs = sf.read(wav_file)

    diar = Diarizer(
        embed_model='ecapa', # supported types: ['xvec', 'ecapa']
        cluster_method='sc', # supported types: ['ahc', 'sc']
        window=1.5, # size of window to extract embeddings (in seconds)
        period=0.75 # hop of window (in seconds)
        )

    segments = diar.diarize(
            wav_file,
            num_speakers=NUM_SPEAKERS
            )
    sourceFile = open(f"{outdir}/{FileId}.diar", 'w')
    print(segments, file = sourceFile)
    sourceFile.close()


import os
import glob
import random
import shlex
import subprocess
import sys
import tempfile
from distutils.version import LooseVersion
from typing import List

import numpy as np
import soundfile as sf
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import split_on_silence
from rich import print
from moviepy.video.io.VideoFileClip import VideoFileClip

""" Project Settings """
CACHE_DIR = os.getcwd() + '/cache/'
VID_TEMPLATE = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Desktop', 'SonarMagus', 'template.mov'))
OUTPUT_PATH = os.getcwd() + '/finished/'
NUM_CLIPS = 1
CLIP_DURATION = 10
VOLUME = 0.5

def generate_random_clip(num_clips):
    cache_path = '/Users/chronic/Desktop/SonarMagus/cache'
    audio_paths = glob.glob(f'{cache_path}/*.mp3')
    audio_path = random.choice(audio_paths)
    audio = AudioSegment.from_file(audio_path)

    return audio[0: CLIP_DURATION * 1000]

def apply_effects(audio, effect):
    if effect == 'reverse':
        return audio.reverse()
    elif effect == 'speedUp':
        return audio.speedup(1.5)
    elif effect == 'slowDown':
        return audio[:]

def main():
    raw_audio = generate_random_clip(NUM_CLIPS)
    applied_effect = random.choice(['reverse', 'speedUp', 'slowDown'])
    applied_audio = apply_effects(raw_audio, applied_effect)

    # Save the segment to disk temporarily
    applied_audio.export('/tmp/segment.mp3', format='mp3')

    # Open the template video and replace the audio track
    vid_clip = VideoFileClip(VID_TEMPLATE)
    audio_clip = AudioFileClip('/tmp/segment.mp3').subclip(0, CLIP_DURATION)
    replacement_clip = vid_clip.set_audio(audio_clip)

    # Insert the clip at the right position
    insertion_time = 0
    inserted_clip = concatenate_videoclips([replacement_clip], method='compose')

    # Export the final composition
    final_clip = inserted_clip.set_duration(insertion_time + vid_clip.duration)
    final_clip.write_videofile(OUTPUT_PATH + 'final_clip.mp4')

    # Clean up tmp files
    os.remove('/tmp/segment.mp3')

if __name__ == "__main__":
    main()
import struct
import pyaudio
import numpy as np
import wave


def wait_for_keyword(porcupine, pa):
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )
    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Keyword detected!")
            # do something when keyword is detected
            stream.stop_stream()
            stream.close()
            return "listening"
    return "waiting"


def record(pa, handle_audio):
    """Record to a wave file until 3 seconds of silence"""
    chunk_size = 1024
    silence_threshold = 500
    sample_rate = 16000
    max_silence_duration = 3  # seconds
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    frames = []
    silent_frames = 0
    while True:
        pcm = stream.read(chunk_size)
        audio_data = np.frombuffer(pcm, dtype=np.int16)
        print(np.max(np.abs(audio_data)))
        if np.max(np.abs(audio_data)) < silence_threshold:
            silent_frames += 1
        else:
            silent_frames = 0
        frames.append(pcm)
        if silent_frames / (sample_rate / chunk_size) >= max_silence_duration:
            break
    stream.stop_stream()
    stream.close()
    handle_audio(b"".join(frames))
    print("Done recording")
    return "awaiting-response"

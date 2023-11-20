import os
import pvporcupine
import pyaudio
import asyncio
from dotenv import load_dotenv

load_dotenv(".env.local")

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")


async def listen():
    porcupine = pvporcupine.create(
        keywords=["porcupine"], access_key=PORCUPINE_ACCESS_KEY
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )
    while True:
        print(porcupine.frame_length)
        pcm = stream.read(porcupine.frame_length // 2)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Keyword detected!")
            # do something when keyword is detected
        await asyncio.sleep(0)


asyncio.run(listen())

import os
import pvporcupine
import pyaudio
import asyncio
from dotenv import load_dotenv

from audio.input import wait_for_keyword, record

load_dotenv(".env.local")

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")


async def listen():
    porcupine = pvporcupine.create(
        keywords=["porcupine", "bumblebee"], access_key=PORCUPINE_ACCESS_KEY
    )
    pa = pyaudio.PyAudio()

    state = "waiting"
    print("Listening...")
    while True:
        if state == "waiting":
            state = wait_for_keyword(porcupine, pa)
        if state == "listening":
            print("Recording...")
            state = record(pa)

        await asyncio.sleep(0)


asyncio.run(listen())

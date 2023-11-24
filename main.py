import os
import pvporcupine
import pyaudio
import asyncio
from dotenv import load_dotenv

from audio.input import wait_for_keyword, record
from audio.output import play_mp3_from_buffer
from ai.chat import ChatStore

load_dotenv(".env.local")

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def listen():
    porcupine = pvporcupine.create(
        keywords=["porcupine", "bumblebee"], access_key=PORCUPINE_ACCESS_KEY
    )
    pa = pyaudio.PyAudio()

    chat_store = ChatStore(OPENAI_API_KEY)

    state = "waiting"
    print("Listening...")
    while True:
        if state == "waiting":
            state = wait_for_keyword(porcupine, pa)
        elif state == "listening":
            print("Recording...")
            state = record(pa, lambda audio: chat_store.add_audio(audio))
        elif state == "awaiting-response":
            print("Awaiting response...")
            buffer = []
            response = await chat_store.get_response()
            if response is None:
                continue
            response.stream_to_file(buffer)
            play_mp3_from_buffer(buffer, pa)

        await asyncio.sleep(0)


asyncio.run(listen())

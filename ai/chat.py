import io
from openai import OpenAI


class ChatStore:
    def __init__(self, openai_api_key) -> None:
        self.coroutine = None
        self.openai = OpenAI(api_key=openai_api_key)

    async def add_audio(self, audio_data):
        # Create the coroutine here
        self.coroutine = self.fetch_chat_response(audio_data)
        # Resolve the coroutine
        result = await self.coroutine
        return result

    async def get_response(self):
        if self.coroutine is not None:
            return await self.coroutine
        else:
            return None

    async def fetch_chat_response(self, audio_data):
        ## Create file buffer from binary audio data
        file_buffer = io.BytesIO(audio_data)
        transcript = self.openai.transcriptions.create(
            model="whisper-1",
            file=file_buffer,
        )
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful voice assistant. Your answers should be conversational and succint.",
                },
                {"role": "user", "content": transcript["text"]},
            ],
        )
        print(response)

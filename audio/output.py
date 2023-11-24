import pyaudio


def play_mp3_from_buffer(mp3_buffer, audio):
    # Open a stream
    stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True)

    # Read the audio data from the in-memory buffer and play it
    stream.write(mp3_buffer)

    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    # Specify the path to your MP3 file
    mp3_file_path = "/path/to/your/mp3/file.mp3"

    # Read the MP3 file into an in-memory buffer
    with open(mp3_file_path, "rb") as file:
        mp3_buffer = file.read()

    # Call the function to play the MP3 file from the in-memory buffer
    play_mp3_from_buffer(mp3_buffer)

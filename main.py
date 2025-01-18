import sys
import whisper_timestamped as whisper

def json_to_srt(json_data, output_file):
    """
    Converts JSON subtitle data into an SRT file.

    Args:
        json_data (dict): JSON data containing subtitle information.
        output_file (str): Path to the output SRT file.
    """
    def format_time(seconds):
        """Converts seconds to SRT timestamp format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

    segments = json_data.get("segments", [])
    
    with open(output_file, "w", encoding="utf-8") as srt_file:
        for segment in segments:
          for i, word in enumerate(segment["words"], start=1):
              start_time = format_time(word["start"])
              end_time = format_time(word["end"])
              text = word["text"]

              # Write the SRT entry
              srt_file.write(f"{i}\n")
              srt_file.write(f"{start_time} --> {end_time}\n")
              srt_file.write(f"{text}\n\n")

if len(sys.argv) < 2:
    print("To use this script you need to specify two arguments, video file location and output subtitles file location")
    sys.exit()

# Example usage
video_file = sys.argv[1]
output_file = sys.argv[2]
audio = whisper.load_audio(video_file)
model = whisper.load_model("small")
result = whisper.transcribe(model,  audio, language="pl", vad=True)
json_to_srt(result, output_file)
print(f"SRT file '{output_file}' has been created.")

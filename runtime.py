import os
import argparse
from datetime import datetime, timedelta  # Importing timedelta
from zhconv import convert
from faster_whisper import WhisperModel

def format_timestamp(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    return f"{str(timedelta(seconds=int(seconds)))}.{millis:03d}"

def main(args):
    start_time = datetime.now()

    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(bundle_dir, "models")
    model = WhisperModel(model_size_or_path=model_path, device="cuda", compute_type="int8")
    segments, info = model.transcribe(args.input, beam_size=5, language='zh')

    subtitles = []
    for i, segment in enumerate(segments):
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end)
        subtitle_text = f"{i+1}\n{start} --> {end}\n{convert(segment.text, 'zh-cn')}\n"
        print(subtitle_text)
        subtitles.append(subtitle_text)

    with open(args.output, "w", encoding="utf-8") as f:
        for subtitle in subtitles:
            f.write(subtitle + "\n")

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"SRT file saved to {args.output}")
    print(f"Script run time: {duration}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio to SRT using WhisperModel")
    parser.add_argument("--input", type=str, required=True, help="Path to the input audio file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output SRT file")

    args = parser.parse_args()
    main(args)

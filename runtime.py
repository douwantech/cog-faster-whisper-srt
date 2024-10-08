import os
import argparse
from datetime import datetime, timedelta  # Importing timedelta
import whisper
import sys
import torch
torch.set_num_threads(1)

def format_timestamp(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    return f"{str(timedelta(seconds=int(seconds)))}.{millis:03d}"

def main(args):
    print(f"当前使用的设备：{device}")
    print(f"PyTorch 是否检测到 GPU：{torch.cuda.is_available()}")
    print(f"当前使用的 CUDA 设备数量：{torch.cuda.device_count()}")
    print(f"当前 CUDA 设备索引：{torch.cuda.current_device()}")
    print(f"当前 CUDA 设备名称：{torch.cuda.get_device_name(0)}")

    start_time = datetime.now()
    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(bundle_dir, "models")
    model = whisper.load_model("large-v3-turbo", device="cuda")
    result = model.transcribe(args.input, beam_size=5, task="transcribe", fp16=False)

    with open(args.output, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(result['segments']):
            # SRT 文件索引从 1 开始
            f.write(f"{idx+1}\n")
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{segment['text'].strip()}\n\n")

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


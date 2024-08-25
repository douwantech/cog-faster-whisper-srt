# Prediction interface for Cog ⚙️
# https://cog.run/python

from cog import BasePredictor, Input, Path

from datetime import timedelta, datetime
from zhconv import convert
from faster_whisper import WhisperModel
import os
import argparse

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    formatted_time = str(timedelta(seconds=int(seconds)))
    hours, minutes, seconds = formatted_time.split(":")
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")
        # from huggingface_hub import snapshot_download

        # snapshot_download(
        #                 cache_dir="cache",
        #                 local_dir="models",
        #                 repo_id="guillaumekln/faster-whisper-large-v2",
        #                 )

    def predict(
        self,
        audio_file: str = Input(description="input file"),
        output_file: str = Input(description="output file"),
    ) -> Path:
        """Run a single prediction on the model"""

        start_time = datetime.now()

        # 加载模型
        model = WhisperModel(model_size_or_path="/data/models", device="cuda", compute_type="int8")

        # 识别音频文件
        segments, info = model.transcribe(audio_file, beam_size=5, language='zh')

        subtitles = []
        for i, segment in enumerate(segments):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            subtitle_text = f"{i+1}\n{start} --> {end}\n{convert(segment.text, 'zh-cn')}\n"
            print(subtitle_text)
            subtitles.append(subtitle_text)

        # 将字幕文本写入到指定文件中
        with open(output_file, "w", encoding="utf-8") as f:
            for subtitle in subtitles:
                f.write(subtitle + "\n")

        end_time = datetime.now()
        duration = end_time - start_time

        print(f"SRT file saved to {output_file}")
        print(f"Script run time: {duration}")
        return Path(output_file)
        # processed_input = preprocess(image)
        # output = self.model(processed_image, scale)
        # return postprocess(output)

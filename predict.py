# Prediction interface for Cog ⚙️
# https://cog.run/python

from cog import BasePredictor, Input, Path
import os
import subprocess


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""

    def predict(
        self,
        input_file: str = Input(description="input file"),
        output_file: str = Input(description="output file"),
    ) -> Path:
        """Run a single prediction on the model"""
        try:
            subprocess.run(
                    [
                        "python", "runtime.py",
                        "--input", f"{input_file}",
                        "--output", f"{output_file}"
                    ],
                    check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while syncing directory: {e}")

        return str(output_file)

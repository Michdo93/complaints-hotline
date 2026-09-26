import sys
import os
import json
import numpy as np
import soundfile as sf
import librosa

CONFIG_FILE = "/opt/complaints-hotline/config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records_folder": "recordoffs", "pitch_steps": -5.0}

def main():
    if len(sys.argv) < 3:
        print("Usage: python record_and_process.py <input_raw_wav> <output_filename>")
        sys.exit(1)

    input_raw_path = sys.argv[1]
    output_filename = sys.argv[2]

    config = load_config()
    records_folder = config.get("records_folder", "recordoffs")
    pitch_steps = float(config.get("pitch_steps", -5.0))

    os.makedirs(records_folder, exist_ok=True)
    final_output_path = os.path.join(records_folder, output_filename)

    if not os.path.exists(input_raw_path):
        print(f"[ERROR] Input file not found: {input_raw_path}")
        sys.exit(1)

    try:
        audio_data, sample_rate = sf.read(input_raw_path, dtype='float32')

        if len(audio_data) > 0:
            if audio_data.ndim > 1:
                audio_data = audio_data.mean(axis=1)

            processed_audio = librosa.effects.pitch_shift(
                y=audio_data,
                sr=sample_rate,
                n_steps=pitch_steps
            )

            sf.write(final_output_path, processed_audio, sample_rate)
            print(f"[SUCCESS] Processed complaint saved to: {final_output_path}")

        if os.path.exists(input_raw_path):
            os.remove(input_raw_path)

    except Exception as e:
        print(f"[ERROR] Processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
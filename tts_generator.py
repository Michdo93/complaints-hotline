import os
import json
from gtts import gTTS
from pydub import AudioSegment

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_welcome_prompt():
    config = load_config()
    prompts_folder = config.get("prompts_folder", "audio_prompts")
    welcome_filename = config.get("welcome_filename", "welcome.wav")
    
    os.makedirs(prompts_folder, exist_ok=True)
    target_path = os.path.join(prompts_folder, welcome_filename)

    print("=== Welcome Prompt Generator ===")
    print("1. Select Language:")
    print("   [1] German (de)")
    print("   [2] English (en)")
    
    lang_choice = input("Choice (1/2): ").strip()
    lang = "de" if lang_choice == "1" else "en"
    tld_options = ["com", "co.uk", "ca", "co.in"] if lang == "en" else ["de", "ch", "at"]

    print("\n2. Select Voice/TLD Accent Variant:")
    for idx, tld in enumerate(tld_options, 1):
        print(f"   [{idx}] {tld}")
    
    tld_choice = input("Choice: ").strip()
    try:
        selected_tld = tld_options[int(tld_choice) - 1]
    except (ValueError, IndexError):
        selected_tld = tld_options[0]

    default_text = "Willkommen beim Beschwerdentelefon. Wie lautet Ihre Beschwerde?" if lang == "de" else "Welcome to the complaints hotline. What is your complaint?"
    
    print(f"\nEnter spoken text (Press ENTER to use default: '{default_text}'):")
    user_text = input("> ").strip()
    spoken_text = user_text if user_text else default_text

    print("\nGenerating speech file...")
    temp_mp3 = "temp_prompt.mp3"
    tts = gTTS(text=spoken_text, lang=lang, tld=selected_tld, slow=False)
    tts.save(temp_mp3)

    # Convert to 8kHz / 16-bit Mono WAV for Asterisk compatibility
    sound = AudioSegment.from_mp3(temp_mp3)
    sound = sound.set_frame_rate(8000).set_channels(1).set_sample_width(2)
    sound.export(target_path, format="wav")

    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

    print(f"[SUCCESS] Prompt file overwritten successfully at: {target_path}")

if __name__ == "__main__":
    generate_welcome_prompt()
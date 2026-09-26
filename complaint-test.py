import time
import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa

# ==========================================
# KONFIGURATION
# ==========================================
SAMPLE_RATE = 22050  # Gute Qualität für Sprache, ressourcenschonend
DURATION = 20        # Aufnahmedauer: 20 Sekunden
OUTPUT_FILE = "beschwerde_verzerrt.wav"

# Pitch-Einstellung (-5 = tief & anonym, +5 = hoch & lustig)
PITCH_STEPS = -5.0 

def main():
    print("=" * 50)
    print("   WILLKOMMEN BEIM BESCHWERDENTELEFON (20 SECONDS)   ")
    print("=" * 50)
    
    # 1. Beep-Ton simulieren (optional)
    print("\n[INFO] Simuliere Beep-Ton...")
    beep_freq = 800
    beep_duration = 0.5
    t = np.linspace(0, beep_duration, int(SAMPLE_RATE * beep_duration), False)
    beep_signal = 0.3 * np.sin(2 * np.pi * beep_freq * t)
    
    # Versuche Beep abzuspielen, ignoriere Fehler falls kein Lautsprecher da ist
    try:
        sd.play(beep_signal, SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"[HINWEIS] Kein Wiedergabegerät gefunden, Beep übersprungen ({e})")

    # 2. 20-Sekunden-Aufnahme starten
    print(f"\n[RECORDING] Mikrofon aktiv! Bitte Beschwerde einsprechen...")
    print(f"[RECORDING] Verbleibende Zeit: {DURATION} Sekunden.")
    
    # sd.rec() aktiviert das Mikrofon automatisch im Hintergrund
    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE), 
        samplerate=SAMPLE_RATE, 
        channels=1, 
        dtype='float32'
    )
    
    # Fortpfeilender Countdown im Terminal
    for remaining in range(DURATION, 0, -1):
        print(f"Aufnahme läuft... {remaining}s ", end="\r")
        time.sleep(1)
        
    sd.wait()  # Warten, bis die 20 Sekunden exakt abgelaufen sind
    print("\n[RECORDING] Aufnahme beendet!")

    # 3. Stimmenverzerrung (Pitch Shift)
    audio_flat = audio_data.flatten()
    print("\n[PROCESSING] Anonymisiere Stimme...")
    start_time = time.time()
    
    processed_audio = librosa.effects.pitch_shift(
        y=audio_flat, 
        sr=SAMPLE_RATE, 
        n_steps=PITCH_STEPS
    )
    
    print(f"[PROCESSING] Fertig in {time.time() - start_time:.2f} Sekunden.")

    # 4. Als WAV-Datei speichern
    sf.write(OUTPUT_FILE, processed_audio, SAMPLE_RATE)
    print(f"\n[SPEICHERN] Datei erfolgreich gespeichert: {OUTPUT_FILE}")
    print("Bereit für den nächsten Schritt / Asterisk-Verarbeitung!")

if __name__ == "__main__":
    main()

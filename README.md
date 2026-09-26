# complaints-hotline

Anyone who wants to complain picks up the phone and lets off some steam. The server (e.g., Raspberry Pi) records the audio message, runs it through a voice distorter (pitch shifter), and uploads it anonymously to its web interface so it can be listened to at any time later. We use USB retro phone handsets and Asterisk.

For a clean, subtle distortion, it's best to combine two effects:

1. **Pitch shifting** (changing the pitch, e.g., a deep “blackmailer’s voice” or a high-pitched “Mickey Mouse voice”).
2. **Formant shifting / bandpass filter** (changing the timbre so that the voice’s unique overtone spectrum is also lost).

## Installation

At first you have to clone the repository:

```
git clone https://github.com/Michdo93/complaints-hotline
```

### Setting Up the Environment

Then you have to create a virtual environment (`venv`):

```
cd complaints-hotline
pyhton3 -m venv .
```

For audio recording, we use `sounddevice`, and for signal processing, we use `librosa` and `soundfile` (or `scipy`).

Install the required packages via the terminal:

```
source bin/activate
pip install sounddevice soundfile librosa numpy
```

## A few tips to try out

* **Deep, anonymous voice**: Set `PITCH_STEPS = -5.0` or `-6.0`. The voice sounds menacing/anonymous, like on TV.
* **Helium/cartoon voice**: Set `PITCH_STEPS = 5.0` or `6.0`. This immediately takes any aggression out of the complaint and makes it extremely funny for your shared apartment or office.
* **Performance on the Pi**: `librosa.effects.pitch_shift` calculates very precisely but uses up some CPU power. For short voice messages (10–30 seconds), however, the power of a Raspberry Pi 4 or 5 is more than enough.




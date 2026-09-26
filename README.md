# Complaints Hotline (Asterisk + Python + Web Dashboard)

Anyone who wants to complain picks up the phone and lets off some steam. The server (e.g., Raspberry Pi) records the audio message, runs it through a voice distorter (pitch shifter), and uploads it anonymously to its web interface so it can be listened to at any time later. We use USB retro phone handsets and Asterisk.

An anonymous, voice-disguised complaint recording system built with Asterisk PBX, Python pitch-shifting audio processing, and a Bootstrap Web Frontend.

---

## 🛠️ Installation & Virtual Environment Setup

### Install Asterisk and Dependencies

```
# Update system and install base packages
sudo apt update && sudo apt upgrade
sudo apt install -y asterisk
sudo apt install -y asterisk asterisk-config \
    python3 python3-pip ffmpeg wget curl espeak
```

### Cloning and installing the Python Repo

Initialize Python virtual environment directly inside the repository folder (`.`):

```bash
cd /opt
sudo git clone https://github.com/Michdo93/complaints-hotline
sudo chown -R $USER:$USER /opt/complaints-hotline
cd /opt/complaints-hotline
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

---

## 🔊 1. Generate Welcome Prompt File

Run the interactive prompt generator to create the welcome audio file:

```bash
cd /opt/complaints-hotline
source bin/activate
python tts_generator.py
```

* Select language (**German** / **English**).
* Choose voice accent variant.
* Set custom text or press ENTER for the default welcome message.
* Overwrites `/audio_prompts/welcome.wav` in 8kHz Mono format required by Asterisk.

---

## 📞 2. Asterisk Configuration

Copy or link Asterisk configs:

```bash
cd /opt/complaints-hotline
sudo cp asterisk_configs/sip.conf /etc/asterisk/sip.conf
sudo cp asterisk_configs/extensions.conf /etc/asterisk/extensions.conf
sudo chown -R asterisk:asterisk /opt/complaints-hotline
sudo systemctl enable asterisk
sudo systemctl restart asterisk
```

### Verify PJSIP endpoints (optional)

```
sudo asterisk -r
```

Inside the Asterisk CLI:

```
asterisk*CLI> pjsip show endpoints
```

### Configure logging (optional)

```
sudo nano /etc/asterisk/logger.conf
```

Maybe you uncomment following lines:

```
messages.log => notice,warning,error
full => notice,warning,error,debug,verbose,dtmf
console => notice,warning,error
```

Inside the Asterisk CLI, reload the logger:

```
asterisk*CLI> logger reload
```

---

## 🌐 3. Web Dashboard

Launch the Flask server:

```bash
cd /opt/complaints-hotline
source bin/activate
python app.py
```

Access the dashboard at `http://<SERVER_IP>:5000` to stream, search, filter, and delete anonymized complaint recordings.

## 🛠️ 4. Service file

At least you should copy the service file.

```
sudo cp /opt/complaints-hotline/systemd/complaints-web.service /etc/systemd/system/complaints-web.service
sudo chown root:root /etc/systemd/system/complaints-web.service
```

Then you should activate and enable the service.

```
sudo systemctl daemon-reload
sudo systemctl enable complaints-web.service
sudo systemctl start complaints-web.service
```

You can check whether the dashboard is running smoothly at any time using these commands:

```
# Check Status
sudo systemctl status complaints-web.service

# View Live Logs
sudo journalctl -u complaints-web.service -f
```

## File structure

After running all scripts and installation the file structure should look like this:

```
/opt/complaints-hotline/
├── asterisk_configs/
│   ├── extensions.conf
│   └── sip.conf
├── audio_prompts/
│   └── welcome.wav
├── recordoffs/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── systemd/
│   └── complaints-web.service
├── templates/
│   └── index.html
├── .gitignore
├── app.py
├── config.json
├── README.md
├── record_and_process.py
├── requirements.txt
└── tts_generator.py
```

# DarkPaw AI Controller — Jarvis

This module adds a Claude-powered AI brain to the DarkPaw robot, modelled after the Jarvis AI from Iron Man.  
Speak commands prefixed with **"Jarvis,"** and the robot will understand and execute them — including complex multi-step tasks — with witty, Jarvis-style commentary.

---

## How it works

```
Microphone → Google STT → "jarvis, <command>"
                                  ↓
                          Claude API (tool-use)
                                  ↓
          ┌───────────────────────────────────────────┐
          │  walk  │  look  │  capture_image           │
          │  do_360_survey  │  guard_patrol             │
          │  stop  │  set_leds  │  speak               │
          └───────────────────────────────────────────┘
                                  ↓
                       Robot hardware (SpiderG + LEDs)
```

Claude receives the transcript as a plain-text message together with a set of tool definitions.  It then decides which tools to call and in which order, executing complex multi-step plans autonomously — and narrates each step in a Jarvis-like voice.

---

## Setup

### 1. Install dependencies

Run the interactive `setup.py` and choose **option 2 (Install DarkPaw)**.  
The script now installs `anthropic` and `espeak` automatically.

Or manually:

```bash
sudo pip3 install anthropic SpeechRecognition
sudo apt-get install -y espeak portaudio19-dev python3-pyaudio
```

### 2. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add that line to `/etc/environment` or `/home/pi/.bashrc` so it persists across reboots.

### 3. Start the server

```bash
cd /home/pi/<repo>/server
sudo python3 server.py
```

The AI controller thread starts automatically alongside the existing robot server.

---

## Voice commands

All commands must begin with **"Jarvis"** (followed by a comma or pause).

| What you say | What the robot does |
|---|---|
| `Jarvis, what do you see?` | Captures an image and asks Claude to describe it |
| `Jarvis, tell me what's in front of you` | Same — Claude decides to call `capture_image` |
| `Jarvis, walk forward for 3 seconds` | Walks forward for 3 s |
| `Jarvis, turn left` | Turns left for 1 s |
| `Jarvis, stand up` | Raises body posture |
| `Jarvis, make a 360 survey of the room` | Rotates 360° in 8 steps, analysing each view with Claude Vision, then gives a spoken summary |
| `Jarvis, enter guard mode` | Patrols for 5 minutes, reporting any changes vs the initial scene |
| `Jarvis, guard for 10 minutes with 6 patrol points` | Guard patrol for 10 min with 6 stops per loop |
| `Jarvis, walk towards the chair` | Claude captures the scene, locates the chair, then plans a walking sequence |
| `Jarvis, set LEDs to red` | Sets RGB LEDs to `(255, 0, 0)` |
| `Jarvis, stop` | Cancels the current task immediately |

---

## LED colour codes

| Colour | Meaning |
|---|---|
| 🔵 Blue | Processing a command |
| 🔴 Red | Guard mode active |
| 🟡 Yellow | Alert detected during guard patrol |
| 🟢 Green | Task complete |

---

## Architecture notes

* **`ai_controller.py`** – All AI logic lives here.  Import `AIController` and call `.start()`.
* **`server.py`** – Starts `AIController` after the LED is initialised, alongside the existing SR and Bluetooth controller threads.
* The AI controller is **additive** — it does not interfere with the existing TCP socket control, PS3 controller, or OpenCV modes.
* Long-running tools (`do_360_survey`, `guard_patrol`, timed `walk`) check a `stop_event` every 50 ms and exit cleanly when cancelled.

---

## Tuning

| Constant | File | Purpose |
|---|---|---|
| `MODEL` | `ai_controller.py` | Claude model to use (default `claude-opus-4-5`) |
| `WAKE_WORD` | `ai_controller.py` | Trigger word (default `jarvis`) |
| `_TURN_STEP_DURATION` | `ai_controller.py` | Seconds per 45° turn step — calibrate to your robot's speed |

---

## Troubleshooting

**"ANTHROPIC_API_KEY not set"** — Export the key before starting:  
`export ANTHROPIC_API_KEY="sk-ant-..."`

**Camera unavailable** — The AI vision tools require the FPV thread to be active, which starts only after a TCP client (the desktop app) connects.  Connect the client first, then issue vision commands.

**STT request error** — Google Speech Recognition requires internet access.  Check the Pi's Wi-Fi connection.

**`espeak` not found** — Run `sudo apt-get install -y espeak`.

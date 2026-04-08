#!/usr/bin/env python3
# File name   : ai_controller.py
# Description : Claude-powered AI brain for voice commands and vision
# Usage       : Set ANTHROPIC_API_KEY env var, then speak "Bot, <command>"
#               e.g. "Bot, tell me what you see"
#                    "Bot, make a 360 survey of the room"
#                    "Bot, enter guard mode for 5 minutes"
#                    "Bot, walk forward for 3 seconds"

import base64
import logging
import os
import threading
import time

import anthropic
import cv2
import speech_recognition as sr

import SpiderG

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
# Model with vision + tool-use support
MODEL = 'claude-opus-4-5'
WAKE_WORD = 'bot'

SYSTEM_PROMPT = (
    "You are the AI brain of an Adeept DarkPaw quadruped spider robot. "
    "The robot has a camera, RGB LED lights, and four legs. "
    "Use the available tools to carry out the user's voice commands. "
    "For complex multi-step tasks (e.g. '360 survey', 'guard mode', "
    "'walk toward the chair'), plan and execute them using multiple tool "
    "calls in sequence. "
    "Always finish by calling the speak tool to give the user a verbal summary."
)

# ---------------------------------------------------------------------------
# Tool schema definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "walk",
        "description": (
            "Make the robot walk in a direction or change its stance. "
            "Valid directions: forward, backward, turnleft, turnright, "
            "StandUp, StayLow, Lean-R, Lean-L."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": [
                        "forward", "backward", "turnleft", "turnright",
                        "StandUp", "StayLow", "Lean-R", "Lean-L",
                    ],
                    "description": "Direction or stance",
                },
                "duration": {
                    "type": "number",
                    "description": "Duration in seconds (default 1.0)",
                },
            },
            "required": ["direction"],
        },
    },
    {
        "name": "look",
        "description": "Aim the robot's camera head in a direction.",
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["left", "right", "up", "down", "center"],
                    "description": "Direction to look",
                },
            },
            "required": ["direction"],
        },
    },
    {
        "name": "capture_image",
        "description": (
            "Capture a single JPEG image from the robot's forward-facing camera. "
            "The image is returned directly so you can describe what you see."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "do_360_survey",
        "description": (
            "Rotate the robot a full 360 degrees, capturing and analysing "
            "images at evenly-spaced angular steps. Returns a textual "
            "description of everything observed at each angle."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "integer",
                    "description": (
                        "Number of capture stops during the rotation "
                        "(default 8 → one capture every 45 degrees)"
                    ),
                },
            },
            "required": [],
        },
    },
    {
        "name": "guard_patrol",
        "description": (
            "Enter guard mode. The robot patrols the area, detects changes "
            "or intruders by comparing each captured frame against a baseline "
            "scene description, and reports any anomalies aloud."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "duration_minutes": {
                    "type": "number",
                    "description": "How long to patrol in minutes (default 5)",
                },
                "patrol_steps": {
                    "type": "integer",
                    "description": (
                        "Number of forward-step + quarter-turn moves per "
                        "patrol loop (default 4)"
                    ),
                },
            },
            "required": [],
        },
    },
    {
        "name": "stop",
        "description": "Immediately stop all robot movement.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "set_leds",
        "description": "Set the robot's RGB LED strip to a solid colour.",
        "input_schema": {
            "type": "object",
            "properties": {
                "r": {"type": "integer", "description": "Red value 0-255"},
                "g": {"type": "integer", "description": "Green value 0-255"},
                "b": {"type": "integer", "description": "Blue value 0-255"},
            },
            "required": ["r", "g", "b"],
        },
    },
    {
        "name": "speak",
        "description": "Speak text aloud using the robot's text-to-speech.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to speak",
                },
            },
            "required": ["text"],
        },
    },
]

# ---------------------------------------------------------------------------
# Camera helpers
# ---------------------------------------------------------------------------

def _get_frame_jpeg():
    """Return the latest camera frame as JPEG bytes, or None on failure.

    Tries in order:
    1. The shared global frame captured by the FPV thread (preferred when
       the robot is fully running and FPV has been started).
    2. A direct cv2.VideoCapture grab (useful during early start-up before
       the FPV thread is active).
    """
    # --- Attempt 1: shared FPV frame ---
    try:
        import FPV  # noqa: PLC0415 – local import to avoid circular deps
        img = FPV.frame_image
        if img is not None:
            ok, buf = cv2.imencode('.jpg', img)
            if ok:
                return buf.tobytes()
    except Exception:  # noqa: BLE001
        pass

    # --- Attempt 2: direct capture ---
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                ok, buf = cv2.imencode('.jpg', frame)
                if ok:
                    return buf.tobytes()
    except Exception:  # noqa: BLE001
        pass

    return None


def _jpeg_to_base64(jpeg_bytes):
    """Encode raw JPEG bytes as a base64 string."""
    return base64.standard_b64encode(jpeg_bytes).decode('utf-8')


def _image_content_block(jpeg_bytes):
    """Build an Anthropic image content block from JPEG bytes."""
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": _jpeg_to_base64(jpeg_bytes),
        },
    }

# ---------------------------------------------------------------------------
# Text-to-speech
# ---------------------------------------------------------------------------

def _speak(text):
    """Speak *text* aloud using espeak (non-blocking)."""
    logger.info('[AI] Speaking: %s', text)
    # Strip characters that could be interpreted by the shell
    safe = (
        text.replace('"', "'")
            .replace('`', "'")
            .replace('$', '')
            .replace('\\', '')
    )
    os.system(f'espeak "{safe}" 2>/dev/null &')

# ---------------------------------------------------------------------------
# Tool execution
# ---------------------------------------------------------------------------

def _execute_tool(name, tool_input, led, stop_event):
    """Execute *name* with *tool_input* and return a list of content blocks.

    *led*        – LED.LED instance for visual feedback.
    *stop_event* – threading.Event; set externally to abort long-running tools.
    """

    # -- walk ------------------------------------------------------------------
    if name == 'walk':
        direction = tool_input['direction']
        duration = float(tool_input.get('duration', 1.0))
        SpiderG.walk(direction)
        end = time.monotonic() + duration
        while time.monotonic() < end and not stop_event.is_set():
            time.sleep(0.05)
        SpiderG.servoStop()
        return [{"type": "text", "text": f"Walked {direction} for {duration:.1f}s."}]

    # -- look ------------------------------------------------------------------
    if name == 'look':
        direction = tool_input['direction']
        _head_move(direction)
        time.sleep(0.6)
        SpiderG.headStop()
        return [{"type": "text", "text": f"Looked {direction}."}]

    # -- capture_image ---------------------------------------------------------
    if name == 'capture_image':
        jpeg = _get_frame_jpeg()
        if jpeg is None:
            return [{"type": "text",
                     "text": "Camera unavailable. Is the FPV thread running?"}]
        return [
            _image_content_block(jpeg),
            {"type": "text", "text": "Describe what you see in the image."},
        ]

    # -- do_360_survey ---------------------------------------------------------
    if name == 'do_360_survey':
        steps = max(1, int(tool_input.get('steps', 8)))
        return _do_360_survey(steps, stop_event)

    # -- guard_patrol ----------------------------------------------------------
    if name == 'guard_patrol':
        duration_min = float(tool_input.get('duration_minutes', 5))
        patrol_steps = max(1, int(tool_input.get('patrol_steps', 4)))
        return _guard_patrol(duration_min, patrol_steps, led, stop_event)

    # -- stop ------------------------------------------------------------------
    if name == 'stop':
        SpiderG.servoStop()
        return [{"type": "text", "text": "All movement stopped."}]

    # -- set_leds --------------------------------------------------------------
    if name == 'set_leds':
        r = int(tool_input.get('r', 0))
        g = int(tool_input.get('g', 0))
        b = int(tool_input.get('b', 0))
        try:
            led.colorWipe(r, g, b)
        except Exception as exc:  # noqa: BLE001
            return [{"type": "text", "text": f"LED error: {exc}"}]
        return [{"type": "text", "text": f"LEDs set to R:{r} G:{g} B:{b}."}]

    # -- speak -----------------------------------------------------------------
    if name == 'speak':
        text = tool_input.get('text', '')
        _speak(text)
        return [{"type": "text", "text": f"Spoke: {text}"}]

    return [{"type": "text", "text": f"Unknown tool: {name}"}]


# ---------------------------------------------------------------------------
# Camera-head helper
# ---------------------------------------------------------------------------

def _head_move(direction):
    if direction == 'left':
        SpiderG.headLeft()
    elif direction == 'right':
        SpiderG.headRight()
    elif direction == 'up':
        SpiderG.headUp()
    elif direction == 'down':
        SpiderG.headDown()
    elif direction == 'center':
        SpiderG.move_init()

# ---------------------------------------------------------------------------
# Compound tools
# ---------------------------------------------------------------------------

# Seconds the robot turns right per step to cover one angular slice.
# At roughly 45 °/step with 8 steps → 360°.  Tune to your robot's speed.
_TURN_STEP_DURATION = 1.5


def _analyse_jpeg(client, jpeg_bytes, question):
    """Ask Claude to describe *jpeg_bytes* with *question*. Returns text."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": [
                _image_content_block(jpeg_bytes),
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text.strip()


def _do_360_survey(steps, stop_event):
    """Rotate 360° and capture + analyse an image at each step."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    angle_step = 360 // steps
    descriptions = []

    for i in range(steps):
        if stop_event.is_set():
            break

        jpeg = _get_frame_jpeg()
        if jpeg:
            angle = i * angle_step
            try:
                desc = _analyse_jpeg(
                    client, jpeg,
                    "In 1-2 sentences list the main objects or features visible.",
                )
                descriptions.append(f"{angle}°: {desc}")
            except anthropic.APIError as exc:
                descriptions.append(f"{angle}°: (analysis error: {exc})")

        # Turn right by one step
        SpiderG.walk('turnright')
        end = time.monotonic() + _TURN_STEP_DURATION
        while time.monotonic() < end and not stop_event.is_set():
            time.sleep(0.05)
        SpiderG.servoStop()
        time.sleep(0.3)

    if descriptions:
        summary = "360° survey complete. " + " | ".join(descriptions)
    else:
        summary = "360° survey complete but no frames were captured."

    return [{"type": "text", "text": summary}]


def _guard_patrol(duration_min, patrol_steps, led, stop_event):
    """Patrol and compare each captured frame against an initial baseline."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    end_time = time.monotonic() + duration_min * 60

    _speak("Entering guard mode.")
    try:
        led.colorWipe(255, 0, 0)   # Red = active guard
    except Exception:  # noqa: BLE001
        pass

    # Establish baseline
    baseline_desc = "unknown scene"
    jpeg = _get_frame_jpeg()
    if jpeg:
        try:
            baseline_desc = _analyse_jpeg(
                client, jpeg,
                "Describe the objects and their positions in 2-3 sentences. "
                "This will be the baseline for intrusion detection.",
            )
        except anthropic.APIError:
            pass

    alerts = []
    patrol_count = 0

    while time.monotonic() < end_time and not stop_event.is_set():
        patrol_count += 1

        for _ in range(patrol_steps):
            if stop_event.is_set():
                break

            # Move: one step forward then quarter-turn right
            SpiderG.walk('forward')
            _interruptible_sleep(0.8, stop_event)
            SpiderG.servoStop()
            time.sleep(0.2)

            SpiderG.walk('turnright')
            _interruptible_sleep(_TURN_STEP_DURATION, stop_event)
            SpiderG.servoStop()
            time.sleep(0.2)

            # Capture and compare
            jpeg = _get_frame_jpeg()
            if jpeg and not stop_event.is_set():
                try:
                    result = _analyse_jpeg(
                        client, jpeg,
                        f"Baseline scene: {baseline_desc}\n\n"
                        "Does this current image show anything NEW, DIFFERENT, "
                        "or SUSPICIOUS compared to the baseline? "
                        "Reply 'no change' if things look the same, otherwise "
                        "describe the change in 1-2 sentences.",
                    )
                    if 'no change' not in result.lower():
                        alert_msg = f"Patrol {patrol_count}: {result}"
                        alerts.append(alert_msg)
                        _speak(f"Alert: {result}")
                        try:
                            led.colorWipe(255, 255, 0)  # Yellow = alert
                        except Exception:  # noqa: BLE001
                            pass
                except anthropic.APIError:
                    pass

    SpiderG.servoStop()
    try:
        led.colorWipe(0, 80, 0)    # Green = done
    except Exception:  # noqa: BLE001
        pass

    summary = f"Guard patrol ended after {patrol_count} patrol loop(s)."
    if alerts:
        summary += " Alerts detected: " + "; ".join(alerts)
    else:
        summary += " No changes detected."

    return [{"type": "text", "text": summary}]


def _interruptible_sleep(seconds, stop_event):
    """Sleep for *seconds* but return early if *stop_event* is set."""
    end = time.monotonic() + seconds
    while time.monotonic() < end and not stop_event.is_set():
        time.sleep(0.05)

# ---------------------------------------------------------------------------
# Main agentic command processor
# ---------------------------------------------------------------------------

def process_command(command_text, led, stop_event):
    """Send *command_text* to Claude and execute tool calls until completion.

    The function runs the standard Anthropic tool-use agentic loop:
    send → execute tools → append results → repeat until stop_reason is
    'end_turn' or *stop_event* is set.
    """
    if not ANTHROPIC_API_KEY:
        logger.error('[AI] ANTHROPIC_API_KEY not set.')
        _speak("I cannot connect: the API key is not configured. "
               "Please set the ANTHROPIC_API_KEY environment variable.")
        return

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    messages = [{"role": "user", "content": command_text}]
    logger.info('[AI] Processing command: %s', command_text)

    while not stop_event.is_set():
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )
        except anthropic.APIError as exc:
            logger.error('[AI] Claude API error: %s', exc)
            _speak("I encountered a Claude API error. Please check the logs.")
            break

        if response.stop_reason == 'end_turn':
            # Speak any final text block
            for block in response.content:
                if hasattr(block, 'text') and block.text:
                    _speak(block.text)
            break

        if response.stop_reason == 'tool_use':
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    logger.info('[AI] Tool: %s  args: %s', block.name, block.input)
                    result_content = _execute_tool(
                        block.name, block.input, led, stop_event
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_content,
                    })
            messages.append({"role": "user", "content": tool_results})
        else:
            # Unexpected stop reason; log and exit
            logger.warning('[AI] Unexpected stop_reason: %s', response.stop_reason)
            break

# ---------------------------------------------------------------------------
# AIController thread
# ---------------------------------------------------------------------------

class AIController(threading.Thread):
    """Background thread that listens for voice commands beginning with "Bot".

    Workflow:
    1. Continuously listen for audio via the default microphone.
    2. Transcribe with Google Speech Recognition (requires internet).
    3. If the transcript starts with the wake word ("bot"), pass the remainder
       to Claude via *process_command*.
    4. Claude decides which tools to call and in which order.

    The current task can be cancelled at any time by saying "Bot, stop" or
    "Bot, cancel", which sets the internal *_task_stop* event so that
    long-running tools (360 survey, guard patrol, timed walks) exit cleanly.
    """

    def __init__(self, led):
        super().__init__(daemon=True, name='AIController')
        self.led = led
        self._running = threading.Event()
        self._running.set()
        self._task_stop = threading.Event()
        self._task_thread = None
        self._recognizer = sr.Recognizer()

    # ------------------------------------------------------------------
    # Public control API
    # ------------------------------------------------------------------

    def shutdown(self):
        """Stop the controller thread and any running task."""
        self._running.clear()
        self._task_stop.set()

    def cancel_task(self):
        """Abort the current task (if any) and reset for the next command."""
        self._task_stop.set()
        if self._task_thread and self._task_thread.is_alive():
            self._task_thread.join(timeout=3)
        self._task_stop.clear()
        SpiderG.servoStop()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dispatch(self, command):
        """Cancel any running task then start *command* in its own thread."""
        self.cancel_task()
        self._task_thread = threading.Thread(
            target=process_command,
            args=(command, self.led, self._task_stop),
            daemon=True,
            name='AITask',
        )
        self._task_thread.start()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        logger.info('[AI] Controller started. Say "%s, <command>" to interact.',
                    WAKE_WORD.capitalize())

        while self._running.is_set():
            try:
                with sr.Microphone(device_index=0, sample_rate=48000) as source:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    try:
                        audio = self._recognizer.listen(
                            source, timeout=5, phrase_time_limit=10
                        )
                    except sr.WaitTimeoutError:
                        continue

                try:
                    text = self._recognizer.recognize_google(audio).lower().strip()
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as exc:
                    logger.warning('[AI] STT request error: %s', exc)
                    time.sleep(2)
                    continue

                logger.debug('[AI] Heard: %s', text)

                if not text.startswith(WAKE_WORD):
                    continue

                # Strip wake word + optional punctuation
                command = text[len(WAKE_WORD):].lstrip(' ,.:!').strip()

                if not command or command in ('stop', 'cancel', 'abort'):
                    self.cancel_task()
                    _speak("Task cancelled.")
                    continue

                logger.info('[AI] Command received: %s', command)
                try:
                    self.led.colorWipe(0, 0, 255)  # Blue = thinking
                except Exception:  # noqa: BLE001
                    pass
                self._dispatch(command)

            except Exception as exc:  # noqa: BLE001
                logger.error('[AI] Microphone error: %s', exc)
                time.sleep(1)

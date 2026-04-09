#!/usr/bin/env python
from importlib import import_module
import logging
import os
from flask import Flask, render_template, Response, send_from_directory, jsonify, request
from flask_cors import *
# import camera driver

from camera_opencv import Camera
import threading

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, supports_credentials=True)
camera = Camera()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/api/img/<path:filename>')
def sendimg(filename):
    return send_from_directory(dir_path+'/dist/img', filename)

@app.route('/js/<path:filename>')
def sendjs(filename):
    return send_from_directory(dir_path+'/dist/js', filename)

@app.route('/css/<path:filename>')
def sendcss(filename):
    return send_from_directory(dir_path+'/dist/css', filename)

@app.route('/api/img/icon/<path:filename>')
def sendicon(filename):
    return send_from_directory(dir_path+'/dist/img/icon', filename)

@app.route('/fonts/<path:filename>')
def sendfonts(filename):
    return send_from_directory(dir_path+'/dist/fonts', filename)

@app.route('/<path:filename>')
def sendgen(filename):
    return send_from_directory(dir_path+'/dist', filename)

@app.route('/')
def index():
    return send_from_directory(dir_path+'/dist', 'index.html')

# ---------------------------------------------------------------------------
# AI test routes — accessible at http://<robot-ip>/ai-test
# ---------------------------------------------------------------------------

@app.route('/ai-test')
def ai_test():
    return send_from_directory(dir_path + '/dist', 'ai-test.html')


@app.route('/api/ai/status')
def ai_status():
    """Return current AI configuration: API key presence, wake word, mics."""
    try:
        import ai_controller as aic
        mic_info = aic.list_microphones()
        return jsonify({
            'api_key_set': bool(aic.ANTHROPIC_API_KEY),
            'wake_word': aic.WAKE_WORD,
            'model': aic.MODEL,
            'microphones': mic_info['microphones'],
            'default_mic_index': mic_info['default_index'],
            'mic_error': mic_info['error'],
        })
    except Exception:
        logger.exception('[AI] /api/ai/status error')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/ai/tts-test', methods=['POST'])
def ai_tts_test():
    """Speak a test phrase through espeak and report success."""
    try:
        import ai_controller as aic
        body = request.get_json(silent=True) or {}
        text = str(body.get('text', 'Jarvis online. Audio systems nominal.'))[:aic.MAX_TTS_TEXT_LENGTH]
        result = aic.test_tts(text)
        return jsonify(result)
    except Exception:
        logger.exception('[AI] /api/ai/tts-test error')
        return jsonify({'ok': False, 'error': 'Internal server error'}), 500


@app.route('/api/ai/mic-test', methods=['POST'])
def ai_mic_test():
    """Record a short phrase and return the transcript."""
    try:
        import ai_controller as aic
        result = aic.test_mic_capture()
        return jsonify(result)
    except Exception:
        logger.exception('[AI] /api/ai/mic-test error')
        return jsonify({'ok': False, 'error': 'Internal server error'}), 500


@app.route('/api/ai/text-command', methods=['POST'])
def ai_text_command():
    """Send a typed command to Jarvis and return the spoken reply (no hardware)."""
    try:
        import ai_controller as aic
        body = request.get_json(silent=True) or {}
        command = str(body.get('command', '')).strip()
        if not command:
            return jsonify({'ok': False, 'error': 'command is required'}), 400
        result = aic.test_jarvis_response(command)
        return jsonify(result)
    except Exception:
        logger.exception('[AI] /api/ai/text-command error')
        return jsonify({'ok': False, 'error': 'Internal server error'}), 500


@app.route('/api/switch', methods=['POST'])
def switch_ctrl():
    """Toggle a GPIO switch (headlight). Body: {port: 1-3, state: 0|1}
    Omit port to toggle all 3 switches."""
    try:
        import switch
        body = request.get_json(silent=True) or {}
        state = int(body.get('state', 1))
        port = body.get('port')
        if port is not None:
            switch.switch(int(port), state)
        else:
            for p in (1, 2, 3):
                switch.switch(p, state)
        return jsonify({'ok': True, 'state': state})
    except Exception:
        logger.exception('/api/switch error')
        return jsonify({'ok': False, 'error': 'Switch control failed'}), 500


class webapp:
    def __init__(self):
        self.camera = camera

    def modeselect(self, modeInput):
        Camera.modeSelect = modeInput

    def colorFindSet(self, H, S, V):
        camera.colorFindSet(H, S, V)

    def thread(self):
        app.run(host='0.0.0.0', threaded=True)

    def startthread(self):
        fps_threading=threading.Thread(target=self.thread)         #Define a thread for FPV and OpenCV
        fps_threading.setDaemon(False)                             #'True' means it is a front thread,it would close when the mainloop() closes
        fps_threading.start()                                     #Thread starts



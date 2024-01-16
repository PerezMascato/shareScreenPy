import flask
from flask_basicauth import BasicAuth
import mss
import cv2
import numpy as np
from flask import Response

app = flask.Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'alex'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

basic_auth = BasicAuth(app)

# Establecer la resolución deseada
screen_width, screen_height = 1920, 1080
jpeg_quality = 30  # Ajusta este valor según tus necesidades

def generate_frames():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}

        while True:
            # Capturar el cuadro de la pantalla como una imagen
            screenshot = sct.grab(monitor)

            # Convertir la imagen a formato numpy array
            img = np.array(screenshot)

            # Convertir la imagen a formato JPEG con compresión ajustada
            ret, frame = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            frame = frame.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
@basic_auth.required
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

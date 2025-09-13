from flask import Flask, render_template, jsonify, request, Response
import psutil, platform, datetime
#import cv2

app = Flask(__name__)

# Home route - Dashboard
@app.route("/")
def home():
    return render_template("dashboard.html")

# Health data API (for auto refresh)
# Health data API (for auto refresh + alerts)
@app.route("/health")
def health():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alert = "✅ Normal"
    if cpu > 80:
        alert = f"⚠️ High CPU usage: {cpu}%"
    elif memory > 90:
        alert = f"⚠️ High Memory usage: {memory}%"
    elif disk > 90:
        alert = f"⚠️ Low Disk Space: {disk}% used"

    data = {
        "time": str(datetime.datetime.now()),
        "cpu_percent": cpu,
        "memory": memory,
        "disk": disk,
        "os": platform.platform(),
        "alert": alert
    }
    return jsonify(data)

"""
# Camera stream generator with Motion/Face Detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def generate_frames():
    camera = cv2.VideoCapture(0)  # 0 = default webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            alert_msg = None
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                alert_msg = "⚠️ Person Detected!"

            # Agar face detect hota hai to terminal me bhi alert print hoga
            if alert_msg:
                global latest_alert
                print(alert_msg)
                latest_alert = "⚠️ Person detected on Camera!"


            # Convert frame to jpeg
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Camera route
@app.route("/camera_feed")
def camera_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 🔹 Camera Alert Variable
latest_alert = "✅ No alerts"

@app.route("/get_alert")
def get_alert():
    return jsonify({"alert": latest_alert})
    
"""
# 🎤 Voice Assistant API
@app.route("/assistant", methods=["POST"])
def assistant():
    user_text = request.json.get("query", "").lower()
    print("User said:", user_text)

    if "hello" in user_text:
        reply = "Hello Akash, how are you?"
    elif "time" in user_text:
        reply = f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif "cpu" in user_text:
        reply = f"Current CPU usage is {psutil.cpu_percent()} percent"
    elif "memory" in user_text:
        reply = f"Memory usage is {psutil.virtual_memory().percent} percent"
    elif "stop" in user_text or "exit" in user_text:
        reply = "Goodbye Akash!"
    else:
        reply = "Sorry, I did not understand that."

    return jsonify({"reply": reply})

# 🔹 Dummy Smart Controls (Light/Fan)
device_state = {"light": "OFF", "fan": "OFF"}

@app.route("/toggle/<device>", methods=["POST"])
def toggle_device(device):
    if device in device_state:
        device_state[device] = "ON" if device_state[device] == "OFF" else "OFF"
        return jsonify({device: device_state[device]})
    return jsonify({"error": "Device not found"}), 404

if __name__ == "__main__":
    print("✅ Starting SmartAI Flask Server...")
    app.run(debug=True, host="0.0.0.0", port=5001)

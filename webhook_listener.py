from flask import Flask, request, abort
import subprocess
import os 
import hashlib
import hmac

app = Flask(__name__)

GITHUB_SECRET = os.environ.get("GITHUB_SECRET")

@app.route("/update", methods=["POST"])
def update():
    # Verify the Signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not is_valid_signature(request.data, signature):
        abort(403)
    
    # Pull the latest changes
    subprocess.run(["git", "pull"], cwd="/root/GoSave")
    # Restart Gunicorn Service
    subprocess.run(["sudo", "systemctl", "restart", "gunicorn"])
    return "Updated and restarted", 200

def is_valid_signature(payload, signature):
    hash = hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest('sha256=' + hash, signature)

if __name__ == "__main__":
    app.run(port=5000)
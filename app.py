from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
import os
import shutil
from datetime import datetime
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["GENERATED_FOLDER"] = "generated"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["GENERATED_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Simulate HTML generation
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = os.path.join(app.config["GENERATED_FOLDER"], f"site_{timestamp}")
            os.makedirs(export_dir, exist_ok=True)

            # Dummy index.html for now
            with open(os.path.join(export_dir, "index.html"), "w") as f:
                f.write(f"<html><body><h1>Rankings generated at {timestamp}</h1></body></html>")

            # Zip the directory
            zip_io = BytesIO()
            with ZipFile(zip_io, 'w') as zipf:
                for root, dirs, files in os.walk(export_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, export_dir)
                        zipf.write(filepath, arcname)
            zip_io.seek(0)
            return send_file(zip_io, as_attachment=True, download_name="USATKD_Rankings.zip", mimetype="application/zip")
    return render_template("upload.html")

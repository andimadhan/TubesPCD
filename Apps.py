from flask import Flask, render_template, request
import os
from compress import compress_image

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        quality = int(request.form["quality"])

        # Simpan input
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], "input.png")
        file.save(filepath)

        # === DCT + Quantization + Huffman ===
        compressed_path, heatmap_path, entropy, compressed_kb = compress_image(
            filepath, quality
        )

        # === Original size (file asli) ===
        original_size = round(os.path.getsize(filepath) / 1024, 2)

        # === Compression ratio dari Huffman ===
        saving_percent = round(
            (1 - (compressed_kb / original_size)) * 100, 2
        )

        return render_template(
            "index.html",
            result=True,
            original="static/input.png",
            result_image=compressed_path,
            heatmap=heatmap_path,
            original_size=original_size,
            compressed_size=compressed_kb,
            entropy=entropy,
            saving_percent=saving_percent
        )

    return render_template("index.html", result=False)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
import os
import torch
import numpy as np
from PIL import Image

from colorizers import eccv16
from colorizers.util import load_img, preprocess_img, postprocess_tens

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model
colorizer = eccv16(pretrained=True).eval()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']

        # Save input
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Load image
        img = load_img(input_path)

        # Preprocess
        tens_l_orig, tens_l_rs = preprocess_img(img, HW=(256,256))

        # Colorize
        with torch.no_grad():
            out_ab = colorizer(tens_l_rs)

        # Postprocess
        out_img = postprocess_tens(tens_l_orig, out_ab)

        # 🔥 SAVE IMAGE MANUALLY (fix)
        output_path = os.path.join(
            UPLOAD_FOLDER,
            "colorized_" + file.filename
        )

        out_img = (out_img * 255).astype(np.uint8)
        Image.fromarray(out_img).save(output_path)

        return render_template(
            'index.html',
            original=input_path,
            output=output_path
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

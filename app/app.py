from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import os
import io
import requests
from flask import Flask, request, send_file, jsonify
import textwrap

app = Flask(__name__)

def draw_text_with_wrapping(draw, text, font, max_width, x, y, max_height, line_spacing=10):
    lines = []
    for paragraph in text.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=100)
        for line in wrapped:
            while True:
                line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
                if line_width <= max_width:
                    break
                cutoff = len(line)
                while cutoff > 0 and (font.getbbox(line[:cutoff])[2] - font.getbbox(line[:cutoff])[0]) > max_width:
                    cutoff -= 1
                lines.append(line[:cutoff])
                line = line[cutoff:]
            lines.append(line)

    for line in lines:
        if y + (font.getbbox(line)[3] - font.getbbox(line)[1]) > max_height:
            break
        draw.text((x, y), line, font=font, fill=(0, 0, 0))
        line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
        y += line_height + line_spacing
    return y

def add_rounded_image_fixed(base_img, add_img, box, radius=30):
    x0, y0, x1, y1 = box
    target_width = x1 - x0
    target_height = y1 - y0

    add_img = add_img.convert("RGBA")
    add_img = add_img.resize((target_width, target_height))

    mask = Image.new('L', (target_width, target_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, target_width, target_height), radius=radius, fill=255)
    add_img.putalpha(mask)

    base_img.paste(add_img, (x0, y0), mask=add_img)
    return base_img

def render_template_with_text_and_image(template_path, user_text, add_img_data, font_path="arial.ttf", font_size=32):
    base = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(font_path, font_size)

    # Regiões fixas do template
    text_x0, text_y0 = 115, 325
    text_x1, text_y1 = 966, 625
    image_x0, image_y0 = 122, 664
    image_x1, image_y1 = 955, 1129

    max_text_width = text_x1 - text_x0
    max_text_height = text_y1 - text_y0

    draw_text_with_wrapping(
        draw, user_text, font, max_text_width, text_x0, text_y0, max_height=text_y1
    )

    add_img = Image.open(io.BytesIO(add_img_data))
    image_box = (image_x0, image_y0, image_x1, image_y1)
    base = add_rounded_image_fixed(base, add_img, image_box)

    output_buffer = io.BytesIO()
    base.save(output_buffer, format="JPEG")
    output_buffer.seek(0)
    return output_buffer

@app.route("/")
def home():
    return jsonify({
        "message": "Servidor Flask ativo! Use POST em /generate com JSON para gerar conteúdo."
    })


@app.route("/generate", methods=["GET"])
def generate():
    data = request.json
    text = data.get("text")
    image_url = data.get("image_url")

    if not text or not image_url:
        return {"error": "'text' and 'image_url' are required."}, 400

    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to download image: {str(e)}"}, 400

    output_img = render_template_with_text_and_image("Ney Italo de França - Post Twitter.png", text, image_response.content)
    return send_file(output_img, mimetype='image/jpeg')



if __name__ == "__main__":
    from waitress import serve
    print("Rodando em modo produção com Waitress...")
    serve(app, host="0.0.0.0", port=5000)
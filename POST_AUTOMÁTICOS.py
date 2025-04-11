from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import os

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

def add_rounded_image_fixed(base_img, add_img_path, box, radius=30):
    x0, y0, x1, y1 = box
    target_width = x1 - x0
    target_height = y1 - y0

    add_img = Image.open(add_img_path).convert("RGBA")
    add_img = add_img.resize((target_width, target_height))

    mask = Image.new('L', (target_width, target_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, target_width, target_height), radius=radius, fill=255)
    add_img.putalpha(mask)

    base_img.paste(add_img, (x0, y0), mask=add_img)
    return base_img

def render_template_with_text_and_image(
    template_path, output_path, user_text, image_to_add_path,
    font_path=None, font_size=32):

    base = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(base)

    font = ImageFont.truetype(font_path or "arial.ttf", font_size)

    # Regiões fixas do template
    text_x0, text_y0 = 115, 325
    text_x1, text_y1 = 966, 625
    image_x0, image_y0 = 122, 664
    image_x1, image_y1 = 955, 1129

    max_text_width = text_x1 - text_x0
    max_text_height = text_y1 - text_y0

    final_text_bottom = draw_text_with_wrapping(
        draw, user_text, font, max_text_width, text_x0, text_y0, max_height=text_y1
    )

    image_box = (image_x0, image_y0, image_x1, image_y1)
    base = add_rounded_image_fixed(base, image_to_add_path, image_box)
    base.save(output_path)



# EXEMPLO DE USO
if __name__ == "__main__":
    render_template_with_text_and_image(
        template_path=r"C:\Users\Seals\Desktop\Ney Italo de França - Post Twitter.png",           # Caminho do template
        output_path="saida_final.jpg",          # Saída final
        user_text="""A Inteligência Artificial (IA) está transformando profundamente a maneira como vivemos, trabalhamos e nos relacionamos. Ao automatizar tarefas repetitivas e analisar grandes volumes de dados em tempo real, a IA permite decisões mais rápidas e precisas. 
Seus impactos positivos são vastos: na medicina, auxilia no diagnóstico precoce de doenças; na educação, personaliza o aprendizado; na indústria, otimiza processos; e no cotidiano, torna serviços mais acessíveis e eficientes.
Mais do que uma ferramenta, a IA representa uma extensão da capacidade humana — um aliado poderoso na construção de um futuro mais inteligente, ético e sustentável.
""",
        image_to_add_path=r"C:\Users\Seals\Desktop\Home.png",  # Caminho para imagem representativa"
        font_path="arial.ttf",
        font_size=36
    )

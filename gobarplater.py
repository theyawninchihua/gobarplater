import pandas as pd
from PIL import Image, ImageDraw, ImageFont

data = pd.read_csv('data.csv')
images = []

def grade_to_colour(grade):
    if grade=='A':
        return (129, 213, 82)
    elif grade=='B':
        return (249, 217, 87)
    elif grade=='C':
        return (226, 121, 46)
    elif grade=='D':
        return (220, 59, 38)
    elif grade=='-':
        return (150, 150, 150)
    else:
        assert False, "grade must be in {'A', 'B', 'C', 'D'}"

for index, row in data.iterrows():
    img = Image.new('RGB', (400, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((40, 40), f"{row['brand']} {row['model']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=25))
    draw.text((40, 70), f"{row['variant']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.line([40, 110, 360, 110], fill=(0, 0, 0))

    draw.text((40, 125), "Rear seat belt reminders", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 175), "Curtain airbag coverage", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 225), "ISOFIX/i-Size availability", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.rectangle([337, 127, 357, 147], fill=grade_to_colour(f"{row['rsbr']}"))
    draw.rectangle([337, 177, 357, 197], fill=grade_to_colour(f"{row['scab']}"))
    draw.rectangle([337, 227, 357, 247], fill=grade_to_colour(f"{row['isofix']}"))

    draw.text((340, 125), f"{row['rsbr']}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=20))
    draw.text((340, 175), f"{row['scab']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))
    draw.text((340, 225), f"{row['isofix']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))
    
    draw.line([40, 265, 120, 265], fill=(129, 213, 82))
    draw.line([120, 265, 200, 265], fill=(249, 217, 87))
    draw.line([200, 265, 280, 265], fill=(226, 121, 46))
    draw.line([280, 265, 360, 265], fill=(220, 59, 38))

    draw.text((40, 275), f"Evaluated on {row['date']}.\nMore information at: bit.ly/gobargrades2025\n\nEvaluation results are subject to error and may\nbe revised or removed without notice.", fill=(0, 0, 0), align='left', font_size=15)

    img.save(f"output/{row['model'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_{row['variant'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_scorecard.png")
    images.append(img)

images[0].save('output/slideshow.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=750, loop=0)

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
    else:
        assert False, "grade must be in {'A', 'B', 'C', 'D'}"

for index, row in data.iterrows():
    img = Image.new('RGB', (400, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((40, 40), f"{row['brand']} {row['model']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=25))
    draw.text((40, 70), f"{row['variant']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.text((40, 125), "Rear seat belt reminders", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 175), "Curtain airbag coverage", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 225), "ISOFIX/i-Size availability", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.rectangle([337, 127, 357, 147], fill=grade_to_colour(f"{row['rsbr']}"))
    draw.rectangle([337, 177, 357, 197], fill=grade_to_colour(f"{row['scab']}"))
    draw.rectangle([337, 227, 357, 247], fill=grade_to_colour(f"{row['isofix']}"))

    draw.text((340, 125), f"{row['rsbr']}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=20))
    draw.text((340, 175), f"{row['scab']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))
    draw.text((340, 225), f"{row['isofix']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))

    draw.text((40, 275), f"{row['date']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial", size=15))

    images.append(img)

stitched_width = 1200
stitched_height = ((len(images) + 2) // 3) * 400

final_image = Image.new('RGB', (stitched_width, stitched_height), color=(255, 255, 255))

for idx, img in enumerate(images):
    final_image.paste(img, ((idx % 3) * 400, (idx // 3) * 400))

final_image.save('output/stitched.jpg')

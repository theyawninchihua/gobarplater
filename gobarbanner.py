import pandas as pd
from PIL import Image, ImageDraw, ImageFont

data = pd.read_csv('data.csv')
images = []
n = 3 # images per row

def type_to_colour(type):
    if type=='i':
        return (129, 213, 82)
    elif type=='ii':
        return (249, 217, 87)
    elif type=='iii':
        return (226, 121, 46)
    elif type=='iv':
        return (102, 61, 20)
    elif type=='v':
        return (220, 59, 38)
    elif type=='-':
        return (150, 150, 150)
    else:
        assert False, "type must be in {'i', 'ii', 'iii', 'iv', 'v'}"

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
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([40, 40, 110, 110], fill=grade_to_colour(f"{row['rsbr']}"))

    draw.text((53, 36), f"{row['rsbr']}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=60))

    draw.text((120, 36), f"{row['brand']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=25))
    draw.text((120, 64), f"{row['model']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial", size=25))
    draw.text((120, 92), f"{row['variant']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))

    draw.line([40, 120, 360, 120], fill=(0, 0, 0))

    draw.text((40, 125), "Rear seat belt audio warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 160), "Rear seat belt visual warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.circle([340, 140], 10, fill=type_to_colour(row["audio"]))
    draw.circle([340, 175], 10, fill=type_to_colour(row["visual"]))

    # draw.text((40, 330), f"Evaluated {row['date']}. Values indicated are for secondary signals\n& 2nd-row outboard seats, subject to error. See bit.ly/gobargrades2025", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=10))

    images.append(img)

stitched_width = n * 400
stitched_height = (((len(images) + n - 1) // n) * 200) + 200 # extra 200 for comments

final_image = Image.new('RGB', (stitched_width, stitched_height), color=(255, 255, 255))

for idx, img in enumerate(images):
    final_image.paste(img, ((idx % n) * 400, (idx // n) * 200))

h = (((len(images)-1)//n))*200
w = 400*(n-1)
draw = ImageDraw.Draw(final_image)
draw.text((w+60, h+215), "when an occupant \'is\' not belted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
draw.text((w+60, h+235), "when an occupant \'changes to\' unbelted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
draw.text((w+60, h+255), "when any belt \'is\' not fastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
draw.text((w+60, h+275), "when any belt \'changes to\' unfastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
draw.text((w+60, h+295), "not available", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))

draw.circle([w+47.5, h+225], 5, fill=type_to_colour("i"))
draw.circle([w+47.5, h+245], 5, fill=type_to_colour("ii"))
draw.circle([w+47.5, h+265], 5, fill=type_to_colour("iii"))
draw.circle([w+47.5, h+285], 5, fill=type_to_colour("iv"))
draw.circle([w+47.5, h+305], 5, fill=type_to_colour("v"))

draw.line([w+40, h+320, w+120, h+320], fill=(129, 213, 82))
draw.line([w+120, h+320, w+200, h+320], fill=(249, 217, 87))
draw.line([w+200, h+320, w+280, h+320], fill=(226, 121, 46))
draw.line([w+280, h+320, w+360, h+320], fill=(220, 59, 38))

draw.text((w+40, h+330), f"Values indicated are for secondary signals & 2nd-row outboard seats,\nand are subject to error. See bit.ly/gobargrades2025 for details.", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=10))

final_image.save('output/stitched.jpg')
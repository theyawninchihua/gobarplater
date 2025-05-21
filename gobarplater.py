import pandas as pd
from PIL import Image, ImageDraw, ImageFont

data = pd.read_csv('data.csv')
images = []

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
    img = Image.new('RGB', (400, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([40, 40, 110, 110], fill=grade_to_colour(f"{row['rsbr']}"))

    draw.text((53, 36), f"{row['rsbr']}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=60))

    draw.text((120, 36), f"{row['brand']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=25))
    draw.text((120, 64), f"{row['model']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial", size=25))
    draw.text((120, 92), f"{row['variant']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))

    draw.line([40, 120, 360, 120], fill=(0, 0, 0))

    draw.text((40, 135), "Rear seat belt audio warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))
    draw.text((40, 175), "Rear seat belt visual warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    draw.circle([340, 150], 10, fill=type_to_colour(row["audio"]))
    draw.circle([340, 190], 10, fill=type_to_colour(row["visual"]))

    draw.text((60, 215), "when an occupant \'is\' not belted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
    draw.text((60, 235), "when an occupant \'becomes\' unbelted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
    draw.text((60, 255), "when any belt \'is\' not fastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
    draw.text((60, 275), "when any belt \'becomes\' unfastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))
    draw.text((60, 295), "not available", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=15))

    draw.circle([47.5, 225], 5, fill=type_to_colour("i"))
    draw.circle([47.5, 245], 5, fill=type_to_colour("ii"))
    draw.circle([47.5, 265], 5, fill=type_to_colour("iii"))
    draw.circle([47.5, 285], 5, fill=type_to_colour("iv"))
    draw.circle([47.5, 305], 5, fill=type_to_colour("v"))

    # draw.text((340, 175), f"{row['scab']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))
    # draw.text((340, 225), f"{row['isofix']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir Next", size=20))
    
    draw.line([40, 320, 120, 320], fill=(129, 213, 82))
    draw.line([120, 320, 200, 320], fill=(249, 217, 87))
    draw.line([200, 320, 280, 320], fill=(226, 121, 46))
    draw.line([280, 320, 360, 320], fill=(220, 59, 38))

    draw.text((40, 330), f"Evaluated {row['date']}. Values indicated are for secondary signals\n& 2nd-row outboard seats, subject to error. See bit.ly/gobargrades2025", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=10))

    img.save(f"output/{row['model'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_{row['variant'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_scorecard.png")
    images.append(img)

images[0].save('output/slideshow.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=750, loop=0)

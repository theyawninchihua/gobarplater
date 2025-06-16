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
    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([80, 80, 220, 220], fill=grade_to_colour(f"{row['rsbr']}"))

    draw.text((106, 72), f"{row['rsbr']}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=120))

    draw.text((240, 72), f"{row['brand']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=50))
    draw.text((240, 128), f"{row['model']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial", size=50))
    draw.text((240, 184), f"{row['variant']}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))

    draw.line([80, 240, 720, 240], fill=(0, 0, 0))

    draw.text((80, 270), "Rear seat belt audio warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=40))
    draw.text((80, 350), "Rear seat belt visual warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=40))

    draw.circle([680, 300], 20, fill=type_to_colour(row["audio"]))
    draw.circle([680, 380], 20, fill=type_to_colour(row["visual"]))

    draw.text((120, 430), "when an occupant \'is\' not belted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 470), "when an occupant \'changes to\' unbelted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 510), "when any belt \'is\' not fastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 550), "when any belt \'changes to\' unfastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 590), "not available", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))

    draw.circle([95, 450], 10, fill=type_to_colour("i"))
    draw.circle([95, 490], 10, fill=type_to_colour("ii"))
    draw.circle([95, 530], 10, fill=type_to_colour("iii"))
    draw.circle([95, 570], 10, fill=type_to_colour("iv"))
    draw.circle([95, 610], 10, fill=type_to_colour("v"))
    
    draw.line([80, 640, 240, 640], fill=(129, 213, 82))
    draw.line([240, 640, 400, 640], fill=(249, 217, 87))
    draw.line([400, 640, 560, 640], fill=(226, 121, 46))
    draw.line([560, 640, 720, 640], fill=(220, 59, 38))

    draw.text((80, 660), f"Evaluated {row['date']}. Values indicated are for secondary signals\n& 2nd-row outboard seats, subject to error. See bit.ly/gobargrades2025", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    img.save(f"output/{row['model'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_{row['variant'].replace('.', '').replace(' ', '').replace('/', '').replace('-', '')}_scorecard.png")
    images.append(img)

images[0].save('output/slideshow.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=750, loop=0)
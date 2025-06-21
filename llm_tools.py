import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
from string import Template

class ImageSearchSpec(BaseModel):
    """
    Downloads an open-access image of the car that will be used in a press release.
    """
    query: str = Field(
        ...,
        description="The make and model of the car, e.g. 'Honda City'. Do not include variant."
    )

def image_search(spec: ImageSearchSpec) -> None:
    """
    Temp until I get a reliable image search API
    """
    today = date.today().strftime('%d-%m-%Y')

    if not os.path.exists(today):
        os.mkdir(today)

    shutil.copy2("model.png", f"{today}/model.png")

class ScorecardSpec(BaseModel):
    """
    Create a scorecard to visualise the seatbelt reminder evaluation results of a car.
    """
    make: str = Field(
        ...,
        description="The car manufacturer."
    )
    model: str = Field(
        ...,
        description="The name of the car model, expressed in all uppercase letters unless stylisation is important (e.g. i20)."
    )
    variant: str = Field(
        ...,
        description="Trim level and powertrain."
    )
    audio_signal: Literal['i', 'iii', 'iv', 'v', '-'] = Field(
        ...,
        description="""
        Classify the rear seatbelt reminder audio behaviour (beep, chime, ding, etc.) based on the condition that triggers it:
        Carefully use your judgment to determine whether words like 'unfastened' in the user query mean 'not fastened' or 'changed to unfastened' in the given context, and lean towards assuming the latter if there is any ambiguity.
        - 'i': Audio warning activates **only when an occupant is detected and is not wearing a seatbelt**. This reflects systems that actively monitor seat occupancy and belt status in real time and respond to an occupied seat not having a belt fastened at any time.
        - 'iii': Audio warning activates **whenever any rear seatbelt is not fastened**, regardless of whether seats are occupied. This is often a permanent alert based only on belt latch status.
        - 'iv': Audio warning activates **only when any rear seatbelt changes from a fastened to an unfastened state** mid-drive, regardless of whether seats are occupied. This is often based only on change of belt latch status.
        - 'v': No audio reminder is present.
        Use synonyms like 'unbuckled' - 'unbelted' - 'unfastened', and 'became unbelted' - 'changed to unbelted', etc. interchangeably where applicable, and choose the best-fitting code based on intent and logic, not wording alone.
        Before assigning a "i", you must confirm that the system is capable of monitoring rear seat occupancy.
        """
    )
    visual_signal: Literal['i', 'iii', 'iv', 'v', '-'] = Field(
        ...,
        description="""
        Classify the rear seatbelt reminder visual behaviour (tell-tale, instrument cluster display, etc.) based on the condition that triggers it:
        Carefully use your judgment to determine whether words like 'unfastened' in the user query mean 'not fastened' or 'changed to unfastened' in the given context, and lean towards assuming the latter if there is any ambiguity.
        - 'i': Visual warning activates **only when an occupant is detected and is not wearing a seatbelt**. This reflects systems that actively monitor seat occupancy and belt status in real time and respond to an occupied seat not having a belt fastened at any time.
        - 'iii': Visual warning activates **whenever any rear seatbelt is not fastened**, regardless of whether seats are occupied. This is often a permanent alert based only on belt latch status.
        - 'iv': Visual warning activates **only when any rear seatbelt changes from a fastened to an unfastened state** mid-drive, regardless of whether seats are occupied. This is often based only on change of belt latch status.
        - 'v': No visual reminder is present.
        Use synonyms like 'unbuckled' - 'unbelted' - 'unfastened', and 'became unbelted' - 'changed to unbelted', etc. interchangeably where applicable, and choose the best-fitting code based on intent and logic, not wording alone. Different car manufacturers use different wording to describe their systems.
        Before assigning a i, you must confirm that the system is capable of monitoring rear seat occupancy.
        """
    )
    centre_seat_sensor: bool = Field(
        ...,
        description="""True if the car detects occupants in the rear centre seat.
        If the centre seat or third row seats are not explicitly mentioned, set to True.
        """
    )

def scorecard(spec: ScorecardSpec) -> None:
    type_to_colour = {
        'i':(129, 213, 82),
        'ii':(249, 217, 87),
        'iii':(226, 121, 46),
        'iv':(102, 61, 20),
        'v':(220, 59, 38),
        '-':(150, 150, 150)
    }

    grade_to_colour = {
        'A':(129, 213, 82),
        'B':(249, 217, 87),
        'C':(226, 121, 46),
        'D':(220, 59, 38),
        '-':(150, 150, 150)
    }

    grade = 'C'
    if spec.audio_signal=='i' and spec.visual_signal=='i':
        if spec.centre_seat_sensor==False:
            grade = 'B'
        else:
            grade = 'A'
    if spec.audio_signal=='v' or spec.visual_signal=='v':
        grade = 'D'

    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([80, 80, 220, 220], fill=grade_to_colour[f"{grade}"])

    draw.text((106, 72), f"{grade}", fill=(0, 0, 0), align='center', font=ImageFont.truetype(font="Avenir Next", size=120))

    draw.text((240, 72), f"{spec.make}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial Bold", size=50))
    draw.text((240, 128), f"{spec.model}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Arial", size=50))
    draw.text((240, 184), f"{spec.variant}", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))

    draw.line([80, 240, 720, 240], fill=(0, 0, 0))

    draw.text((80, 270), "Rear seat belt audio warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=40))
    draw.text((80, 350), "Rear seat belt visual warning", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=40))

    draw.circle([680, 300], 20, fill=type_to_colour[spec.audio_signal])
    draw.circle([680, 380], 20, fill=type_to_colour[spec.visual_signal])

    draw.text((120, 430), "when an occupant \'is\' not belted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 470), "when an occupant \'changes to\' unbelted", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 510), "when any belt \'is\' not fastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 550), "when any belt \'changes to\' unfastened", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))
    draw.text((120, 590), "not available", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=30))

    draw.circle([95, 450], 10, fill=type_to_colour["i"])
    draw.circle([95, 490], 10, fill=type_to_colour["ii"])
    draw.circle([95, 530], 10, fill=type_to_colour["iii"])
    draw.circle([95, 570], 10, fill=type_to_colour["iv"])
    draw.circle([95, 610], 10, fill=type_to_colour["v"])
    
    draw.line([80, 640, 240, 640], fill=(129, 213, 82))
    draw.line([240, 640, 400, 640], fill=(249, 217, 87))
    draw.line([400, 640, 560, 640], fill=(226, 121, 46))
    draw.line([560, 640, 720, 640], fill=(220, 59, 38))

    today = date.today().strftime('%d-%m-%Y')

    draw.text((80, 660), f"Evaluated {today} (dd-mm). Values indicated for secondary signals\n& 2nd-row outboard seats, subject to error. See bit.ly/gobargrades2025", fill=(0, 0, 0), align='left', font=ImageFont.truetype(font="Avenir", size=20))

    if not os.path.exists(today):
        os.mkdir(today)
    
    img.save(f"{today}/scorecard.png")

    file = open(f"{today}/PR.tex", "w")

    source_template = Template(r"""
    \documentclass[a4paper,12pt]{article}
    \usepackage[utf8]{inputenc}
    \usepackage{graphicx}
    \usepackage{multicol}
    \usepackage{fancyhdr}
    \usepackage[paperwidth=210mm, paperheight=210mm, margin=25mm]{geometry}
    \usepackage{xcolor}
    \usepackage{hyperref}

    \definecolor{triton_green}{RGB}{4,106,56}
    \definecolor{A}{RGB}{129, 213, 82}
    \definecolor{B}{RGB}{249, 217, 87}
    \definecolor{C}{RGB}{226, 121, 46}
    \definecolor{D}{RGB}{220, 59, 38}

    % \setlength{\fboxsep}{0pt}

    % Set up header and footer
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{Gobar NCRAP}
    \fancyhead[C]{}
    \fancyhead[R]{\textit{bit.ly/gobarncrap}}
    \renewcommand{\headrulewidth}{0.5pt}

    % Reduce the space between columns
    \setlength{\columnsep}{10pt}  % Adjust the value to reduce the gap

    % Document begins
    \begin{document}

    % Title
    \begin{center}
        {\color{triton_green} \Large \textbf{$make $model earns $grade grade}}\\
        \vspace{0.5cm}
        {\large \textit{New release of seatbelt reminder results from Gobar NCRAP!}}
    \end{center}

    % Begin multicolumn layout
    \begin{multicols}{2}

    % First column content
    Today, Gobar NCRAP is releasing the seatbelt reminder grades for the $make $model.\\

    The \textbf{$make $model} earns a \colorbox{$grade}{\textbf{$grade}} grade. It activates its rear seatbelt reminder visual signal $visualwhen. It activates its acoustic signal $audiowhen. $nocentre

    \begin{center}
        \noindent \fbox{\includegraphics[width=0.95\linewidth]{$today/scorecard.png}}
    \end{center}
                               
    \begin{center}
        \includegraphics[width=0.95\linewidth]{$today/model.png}
        \textit{The $make $model (image: Wikimedia)}
    \end{center}

    \begin{footnotesize}
        \vspace{0.02in}\hrule\vspace{0.02in}\noindent Gobar NCRAP is an independent, noncommercial blog that evaluates the safety specification of vehicles sold to Indian consumers. The 2025 Gobar Grades assign letter grades -- A, B, C or D -- to vehicle models based on the behaviour of their rear seatbelt reminders. The evaluation criteria reward the fitment of intelligent reminders with occupant detection in all rear seats, as opposed to the less effective change-of-status alerts or permanent warnings accepted by upcoming regulations and given full credit by existing consumer test programmes targeting the Indian vehicle market. Detailed evaluation criteria are available at: \href{https://gobarncrap.wixsite.com/gobar-ncrap/about}{gobarncrap.wixsite.com/gobar-ncrap/about} The latest details of individual grades are at the following URL: \href{https://gobarncrap.wixsite.com/gobar-ncrap/2025-evaluations}{bit.ly/gobargrades2025}.
        \vspace{0.02in}\hrule
    \end{footnotesize}
    \end{multicols}
    
    \end{document}
    """)

    map_category_to_behaviour = {
        "i": "when a detected rear occupant is not wearing their belt",
        "iii": "when any rear seatbelt is not fastened",
        "iv": "when any rear seatbelt changes its status to 'unfastened'",
    }

    visualwhen = map_category_to_behaviour[spec.visual_signal]
    audiowhen = map_category_to_behaviour[spec.audio_signal]
    nocentre = f"The {spec.model} does not detect occupants in the rear centre seat." if not spec.centre_seat_sensor else ""

    source = source_template.substitute(make=spec.make, model=spec.model, grade=grade, visualwhen=visualwhen, audiowhen=audiowhen, nocentre=nocentre, today=today)
    
    file.write(source)
    file.close()

    os.system(f"pdflatex -output-directory={today} {today}/PR.tex")
    os.system(f"rm {today}/PR.aux {today}/PR.log {today}/PR.out")
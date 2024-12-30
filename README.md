# gobarplater
python script for rating plates for the 2025 Gobar Grades

# to use
## dependencies
* see `requirements.txt`
## load data
populate `data.csv` which has the fields `brand,model,variant,rsbr,scab,isofix,date`
* grades (rsbr, scab and isofix) must each be A, B, C or D
## font packs
* if TrueType fonts are not supported please replace `font=ImageFont.truetype(...)` in the `ImageDraw.Draw.text(...)` calls with `font_size=20` or 25 or whatever
## run
* to create individual rating plates and a slideshow:
```sh
$python gobarplater.py
```
* to create a single stitched rating plate as a banner:
```sh
$python gobarbanner.py
```

# contact
* in case of problems, please remember that i don't care

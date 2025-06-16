# gobarplater
python script for rating plates for the 2025 Gobar Grades

# to use manually
## dependencies
* `pandas` and `pillow`
## load data
populate `data.csv` which has the fields shown in the sample
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

# to use as LLM tool
## dependencies
* see `requirements.txt`
## choose LLM
change this line in `llm_pipeline.py`, make sure whatever you choose supports tool binding
```python
  model = init_chat_model(model="llama3.1", model_provider="ollama")
```
## run
* to create individual rating plates and a press release:
```sh
$python llm_pipeline.py
```
you will be prompted for a description of a vehicle's seatbelt reminders


# contact
* in case of problems, please remember that i don't care
* i am not responsible for your dependency conflicts

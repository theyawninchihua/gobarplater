import sys
import os

from escpos.printer import Usb
from PIL import Image

def send_to_escpos_printer(path):
    p = Usb(0x0456, 0x0808, interface=0, in_ep=0x81, out_ep=0x03) # reconfigure this for your printer

    img = Image.open(path).convert("1")
    img = img.resize((384, int(img.height * 384 / img.width))) # for a typical 58 mm printer

    bmp_path = os.path.splitext(path)[0] + ".bmp"
    img.save(bmp_path)

    p.image(bmp_path, fragment_height=256, center=False)
    p.text("\n") # save paper by feeding fewer lines

if __name__ == '__main__':
    if len(sys.argv < 2):
        print("expected path to image as command line argument")
    send_to_escpos_printer(sys.argv[1])
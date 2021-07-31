import os
from PIL import Image

path = "garbage/cardboard"
output = "Labels/001_cardboard"
number = "80"

if not os.path.exists("Labels"):
    os.mkdir("Labels")
if not os.path.exists("Labels/001_cardboard"):
    os.mkdir("Labels/001_cardboard")

for f in os.listdir(path):
    name = f.split(".")
    img = Image.open(os.path.join(path, f))
    dst = os.path.join(output, name[0] + ".txt")

    texts = ""
    texts += "1\n"
    texts += number + " 0 0 " + str(img.size[0]) + " " + str(img.size[1]) + "\n"
    # print(texts)

    text_file = open(dst, "w", encoding="UTF-8")
    text_file.write(texts)
    text_file.close()

    print(f)

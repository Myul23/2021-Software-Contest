import os
from PIL import Image

path = "./downloads/"

# kewords = [
#     "칠성사이다",
#     "생수병",
#     "손소독제",
#     "볼펜",
#     "마우스",
#     "테이크아웃 커피잔",
#     "잼",
#     "와인잔",
#     "유리",
#     "카스",
#     "참치캔",
#     "스위트콘",
#     "신문지",
#     "책",
#     "과자 박스",
#     "색종이",
#     "뽁뽁이",
#     "검은비닐",
#     "비닐",
# ]

kewords = ["택배박스"]

for keword in kewords:
    folder = os.path.join(path, keword)
    if len(os.listdir(folder)) != 2000:
        print(keword + " folder is not enough")

    for idx, f in enumerate(os.listdir(folder)):
        name = f.split(".")
        src = os.path.join(folder, f)
        img = Image.open(src)
        if img.size != (500, 500):
            img = img.resize((500, 500), Image.ANTIALIAS)

        dst = os.path.join(folder, str(idx) + "." + ".jpg")
        img = img.convert("RGB")
        img.save(dst)

        os.remove(src)
        print(f)

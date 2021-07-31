import os
import numpy as np
import cv2

path = "garbage"
output = "Labels/001_"
mine = ["cardboard", "glass", "paper"]
numbers = ["80", "82", "80"]

# points = []
index = 1

for idx, folder in enumerate(mine):
    src = os.path.join(path, folder)
    dst = output + folder

    if not os.path.exists(dst):
        os.mkdir(dst)

    for f in os.listdir(src):
        name = f.split(".")
        # if name[0] not in points:
        #     continue

        image = cv2.imread(os.path.join(src, name[0] + ".jpg"))
        temp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thread = cv2.threshold(temp, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        # 선 검출 + morphology를 이용하는 것이 나았을 수도

        _, labels, stats, _ = cv2.connectedComponentsWithStats(thread)
        x, y, w, h, _ = stats[index]

        texts = ""
        texts += "1\n"
        texts += numbers[idx] + " " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y + h) + "\n"
        # print(texts)

        text_file = open(os.path.join(dst, name[0] + ".txt"), "w", encoding="UTF-8")
        text_file.write(texts)
        text_file.close()

    print(folder)

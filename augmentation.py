import os
import numpy as np
from PIL import Image
import tensorflow as tf

# 참고 https://www.tensorflow.org/api_docs/python/tf/image
import matplotlib.pyplot as plt

images_path = "./downloads/images_007"
labels_path = "./downloads/labels_formal_007"

# ? shift X, crop X, rotate X
# labels의 folder 수집
for folder in os.listdir(labels_path):
    image_path = os.path.join(images_path, folder)
    label_path = os.path.join(labels_path, folder)

    # label에 있는 이름에 따라 image 수집
    for f in os.listdir(label_path):
        name = f.split(".")[0]
        data = []
        data.append(np.asarray(Image.open(os.path.join(image_path, name + ".jpg"))))
        text_file = open(os.path.join(label_path, f), "r", encoding="UTF-8")

        # * image flip
        data.append(tf.image.flip_up_down(data[0]))  # 상하반전
        data.append(tf.image.flip_left_right(data[0]))  # 좌우반전
        data.append(tf.image.flip_left_right(data[1]))  # 상하좌우반전

        # * image 색채 조정
        # data.append(tf.image.adjust_brightness(data[0], 0.4))  # 밝은 것을 밝게
        data.append(tf.image.adjust_contrast(data[0], 0.8))  # 대조 확실하게
        # data.append(tf.image.adjust_gamma(data[0]))  # 감마 높이기
        data.append(tf.image.adjust_saturation(data[0], 3))  # 주변 채도 (높게) 맞추기

        # fig, ax = plt.subplots(2, 4, figsize=(15, 8))
        # ax[0, 0].imshow(data[0])
        # ax[0, 1].imshow(data[1])
        # ax[0, 2].imshow(data[2])
        # ax[0, 3].imshow(data[3])
        # ax[1, 0].imshow(data[4])
        # ax[1, 1].imshow(data[5])
        # ax[1, 2].imshow(data[6])
        # ax[1, 3].imshow(data[7])
        # plt.show()

        for i in range(1, len(data)):
            data[i] = Image.fromarray(np.asarray(data[i]))
            data[i].save(os.path.join(image_path, name + "_" + str(i) + ".jpg"))

        # * flip에 대한 label 변환
        text = []
        for i in range(4):
            text.append("")

        while True:
            texts = text_file.readline()
            if not texts:
                break

            text[0] += texts + "\n"
            n = texts.split(" ")
            for i in range(1, 4):
                text[i] += n[0] + " "

            number = 1 - float(n[1])
            text[1] += n[1] + " "
            text[2] += str(number) + " "
            text[3] += str(number) + " "

            number = 1 - float(n[2])
            text[1] += str(number) + " "
            text[2] += n[2] + " "
            text[3] += str(number) + " "

            number = 1 - float(n[3])
            text[1] += n[3] + " "
            text[2] += str(number) + " "
            text[3] += str(number) + " "

            number = 1 - float(n[4])
            text[1] += str(number) + "\n"
            text[2] += n[4] + "\n"
            text[3] += str(number) + "\n"

        text_file.close()

        for i in range(1, len(text)):
            text_file = open(os.path.join(label_path, name + "_" + str(i) + ".txt"), "w", encoding="UTF-8")
            text_file.write(text[i])
            text_file.close()

        # * 색채 조정한 image의 label은 원본 그대로 저장
        for i in range(len(text), len(data)):
            text_file = open(os.path.join(label_path, name + "_" + str(i) + ".txt"), "w", encoding="UTF-8")
            text_file.write(text[0])
            text_file.close()

    print(folder)

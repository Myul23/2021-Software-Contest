import os

import math
from PIL import Image

# import matplotlib.image as img
import matplotlib.pyplot as plt


# namespace = ["0"]
path = "음료수캔"
# path1 = "1.BBox_manual_labeling/Images/001_plastic_soda"
# path2 = "1.BBox_manual_labeling/Labels/001_plastic_soda"
path1 = "downloads/음료수캔"

# ! 위치로 file 이름을 찾자.
# for idx, files in enumerate(os.listdir(path1)):
#     if files.split(".")[0] in namespace:
#         print(idx)
#         # break


# ! 파일을 제대로 지우지 않아서
# for f in os.listdir(path1):
#     name = f.split(".")
#     if name[1] != "jpg":
#         os.remove(os.path.join(path1, f))


# ! jpg 파일만 열리다니 (심지어 jpeg도 안 됨)
# for f in os.listdir(path1):
#     # print(f)
#     name = f.split(".")
#     src = os.path.join(path1, f)

#     if name[1] == "webp":
#         # print(name[1])
#         dst = os.path.join(path, f)
#         os.rename(src, dst)
#         continue

#     img = Image.open(src)
#     if img.size != (500, 500):
#         basic_size = img.size
#         # print(basic_size)
#         img = img.resize((500, 500), Image.ANTIALIAS)

#         # ! image size 변환에 따른 text 위치값 변환
#         # s = os.path.join(path2, name[0] + ".txt")
#         # if os.path.exists(s):
#         #     text_file = open(s, "r", encoding="UTF-8")

#         #     number = text_file.readline()
#         #     # print(number)
#         #     texts = number
#         #     for i in range(int(number)):
#         #         text = text_file.readline()
#         #         n = text.split(" ")
#         #         texts += n[0] + " "
#         #         texts += str(round(float(n[1]) / basic_size[0] * 500)) + " "
#         #         texts += str(round(float(n[2]) / basic_size[1] * 500)) + " "
#         #         texts += str(round(float(n[3]) / basic_size[0] * 500)) + " "
#         #         texts += str(round(float(n[4]) / basic_size[1] * 500)) + "\n"
#         #     # print(texts)
#         #     text_file.close()

#         #     text_file = open(s, "w", encoding="UTF-8")
#         #     text_file.write(texts)
#         #     text_file.close()

#     dst = os.path.join(path1, name[0] + ".jpg")
#     img = img.convert("RGB")
#     img.save(dst)

#     # os.remove(src)
#     # print(f)


# ! 위치값을 int만 먹는구나.
# for f in os.listdir(path2):
#     s = os.path.join(path2, f)
#     text_file = open(s, "r", encoding="UTF-8")

#     number = text_file.readline()
#     # print(number)
#     texts = number
#     for i in range(int(number)):
#         text = text_file.readline()
#         n = text.split(" ")
#         texts += n[0] + " "
#         texts += str(math.floor(float(n[1]))) + " "
#         texts += str(math.floor(float(n[2]))) + " "
#         texts += str(math.floor(float(n[3]))) + " "
#         texts += str(math.floor(float(n[4]))) + "\n"
#     # print(texts)
#     text_file.close()

#     text_file = open(s, "w", encoding="UTF-8")
#     text_file.write(texts)
#     text_file.close()


# ! class name 다르게 준 걸 바꿔주자.
# for f in os.listdir(path2):
#     # print(f)

#     s = os.path.join(path2, f)
#     if not os.path.exists(s):
#         print(f)
#         continue

#     text_file = open(s, "r", encoding="UTF-8")
#     texts = text_file.read()
#     texts = texts.replace("snackbox", "box")
#     # print(texts)
#     text_file.close()

#     text_file = open(s, "w", encoding="UTF-8")
#     text_file.write(texts)
#     text_file.close()
#     # # os.remove(src)


# ! Images랑 Label이랑 다른 애가 있다?
# # length = 0
# for f1 in os.listdir(path1):
#     flag = False
#     for f2 in os.listdir(path2):
#         if f1.split(".")[0] == f2.split(".")[0]:
#             flag = True
#     if flag is False:
#         print(f1)
#         # break
# #     length += 1
# # print(length)


# ! 찾아서 지우기를 손으로 하니까 귀찮다.
# if not os.path.exists(path):
#     os.mkdir(path)

# numbers = ["98"]
# reals = []

# for f in os.listdir(path1):
#     if f.split(".")[0] in numbers:
#         # 지우면 휴지통에도 남지 않는다. 따라서 직접적으로 지우는 건 패스
#         # os.remove(os.path.join(path1, f1))
#         image = Image.open(os.path.join(path1, f))
#         plt.imshow(image)
#         plt.show()

#         check = int(input("지울까요?: "))
#         if check == 0:
#             src = os.path.join(path1, f)
#             dst = os.path.join(path, f)
#             os.rename(src, dst)
#             reals.append(f.split(".")[0])
#         else:
#             print(f)

# if len(reals) == 0:
#     print("지울 항목이 없습니다.")
#     exit

# print(f"{len(numbers) - len(reals)} / {len(numbers)}")
# for f in os.listdir(path2):
#     if f.split(".")[0] in reals:
#         print(f + " 를 지웠습니다")
#         os.remove(os.path.join(path2, f))


# ! 확장자 변환시키는 과정에서 잘못 없어진 것들을 새로 가져옵니다.
# # length = 0
# for f in os.listdir(path):
#     name = f.split(".")[0]
#     if os.path.exists(os.path.join("비닐_삭제", name + ".webp")):
#         continue
#     elif os.path.exists(os.path.join("비닐_삭제", name + ".gif")):
#         continue

#     name += ".jpg"
#     if os.path.exists(os.path.join("비닐_삭제", name)):
#         continue
#     elif os.path.exists(os.path.join(path1, name)):
#         continue
#     # print(f)
#     # length += 1

#     src = os.path.join(path, f)
#     dst = os.path.join(path1, f)
#     os.rename(src, dst)
# # print(length)

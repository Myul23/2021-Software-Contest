import os

images_list = "1.BBox_manual_labeling/List"
texts_list = "1.BBox_manual_labeling/List_Labels_formal"

for name in os.listdir(images_list):
    if name == ".DS_Store":
        continue

    images = os.path.join(images_list, name)
    texts = os.path.join(texts_list, name)
    # print(images)

    with open(images, "a", encoding="UTF-8") as f:
        text = open(texts, "r", encoding="ANSI").read()
        # print(text)
        f.write(text)
    print(name)


#### make_list_cur.py Process
# import os
# import random
# import glob
# from os import getcwd


# list = []
# for f_path in glob.iglob(os.path.join(current_dir, "*.jpg")):
#     title, ext = os.path.splitext(os.path.basename(f_path))
#     list.append(title)

# while list:
#     name = random.choice(list)
#     print(name)
#     file_train.write("{0}/{1}.jpg\n".format(current_dir.replace("\\", "/"), name))
#     list.remove(name)

# file_train.close()

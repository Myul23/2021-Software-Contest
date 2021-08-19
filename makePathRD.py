import os
import random

base = "./Drone"

train = os.path.join(base, "train")
test = os.path.join(base, "test")
valid = os.path.join(base, "valid")

check = False
if not os.path.exists(train):
    print("no train folder")
    check = True
if not os.path.exists(test):
    print("no test folder")
    check = True
if not os.path.exists(valid):
    print("no valid folder")
    check = True
if check:
    exit()

for folder in [train, test, valid]:
    # make absolute path
    path = os.path.abspath(folder)
    text = open(folder + ".txt", "w", encoding="UTF-8")

    labels = [f for f in os.listdir(folder) if f.endswith(".jpg")]
    random.shuffle(labels)

    for f in labels:
        text.write(os.path.join(path, f) + "\n")
    text.close()
    print(folder + " finish")

import os, re
import pandas as pd

filepath = "X:/dump/before_mapping.txt"
if not os.path.exists(filepath):
    print(filepath + " address does not exist")
    exit(1)

base_file = open(filepath, "r")
if base_file is None:
    print("file does not found")
    exit(0)

csv_file = dict()
for l in base_file.readlines():
    text = re.split(" = |, | ", l)

    # ? iterations
    if "iterations)" in text:
        iteration = text[5]
        csv_file[str(iteration)] = []
    # ? average precision per classes
    elif "class_id" in text:
        for value in text:
            if "%" in value:
                csv_file[str(iteration)].append(value)
                # print(csv_file[str(iteration)])
    # ? choose sentenses include conf_thresh
    elif "conf_thresh" in text:
        for index in range(len(text)):
            if text[index] == "conf_thresh":
                if text[index + 1] != "0.25":
                    print(iteration)
            elif text[index] in ["precision", "recall", "F1-score", "IoU"]:
                csv_file[str(iteration)].append(text[index + 1])
                # print(csv_file[str(iteration)])
    # ? iteration finished
    elif "Area-Under-Curve" in text:
        csv_file[str(iteration)].append(1)
    elif "mean_average_precision" in text:
        csv_file[str(iteration)].append(text[2])
        csv_file[str(iteration)].append(text[3])
base_file.close()

csv_file = pd.DataFrame(csv_file).transpose()
csv_file.columns = ["pet", "pen", "mouse", "paper box", "key", "clip", "vinyl", "stick vinyl", "can", "precision", "recall", "F1-score", "average IoU", "used AUC", "mAP@thresh", "mAP"]
# print(csv_file)
csv_file.to_csv("X:/dump/train_mAPs.csv")

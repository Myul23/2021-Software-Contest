import cv2
from img_aug import Img_aug
import os
import shutil

aug = Img_aug()
augment_num = 10  # 증강결과로 출력되는 이미지의 갯수 선언

save_path = "result"
data_path = "newdata_labeling/images"
label_path = "newdata_labeling/labels_formal"


for folder in os.listdir(data_path):
    if folder in ["0", "1"]:
        # print("beep")
        continue

    base_folder_path = os.path.join(data_path, folder)
    base_label_path = os.path.join(label_path, folder)
    # print(base_folder_path, base_label_path)
    output_path = os.path.join(save_path, folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for img_file in os.listdir(base_folder_path):
        img_path = os.path.join(base_folder_path, img_file)
        lab_path = os.path.join(base_label_path, img_file[:-4]) + ".txt"
        # print("=====================", label_path)

        # print(img_path)

        result_path = os.path.join(output_path, img_file[:-4])
        # idx = str(idx_list.index(img_file[:-4]))
        # if len(idx) == 1:
        #     idx = "0" + idx
        # result_path = os.path.join(output_path, img_file)
        # print(result_path)

        # if not os.path.isdir(result_path):
        #     os.makedirs(result_path)
        img = cv2.imread(img_path)
        images_aug = aug.seq.augment_images([img for i in range(augment_num)])

        for num, aug_img in enumerate(images_aug):
            # result_aug_path = os.path.join(result_path, img_file[:-4]+f'_{num}.jpg')
            # cv2.imwrite(result_aug_path,aug_img)
            result_aug_path = result_path + f"_{num}"
            cv2.imwrite(result_aug_path + ".jpg", aug_img)
            # print(result_aug_path)
            shutil.copyfile(lab_path, result_aug_path + ".txt")
        print(img_file, "finished")
    print(folder)
    # break


# sudo apt-get install ffmpeg
# ffplay /dev/video0
# v4l2-ctl --list-devices

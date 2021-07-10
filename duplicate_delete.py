import os
import time

from PIL import Image


def compare_images(input_image, output_image):
    if input_image.size != output_image.size:
        return False

    rows, cols = input_image.size
    for row in range(rows):
        for col in range(cols):
            input_pixel = input_image.getpixel((row, col))
            output_pixel = output_image.getpixel((row, col))
            if input_pixel != output_pixel:
                return False

    return True


for sep in os.listdir():
    # print(sep, end="\t")

    if sep == "downloads":
        for folder in os.listdir(sep):
            # if folder == "유리잔":
            # print(folder, end=" / ")

            middle = os.path.join(sep, folder)
            files = os.listdir(middle)

            # print(len(files))
            # if len(files) > 1600:
            # print(len(files), end=" : ")
            for i in range(len(files) - 1):
                # print(files[i], end=" / ")
                input_image = os.path.join(middle, files[i])
                if not os.path.exists(input_image):
                    continue

                for j in range(i + 1, len(files)):
                    # print(files[j], end=" / ")
                    output_image = os.path.join(middle, files[j])
                    if not os.path.exists(output_image):
                        continue

                    # print(input_image, output_image, sep=" / ")
                    inputs = Image.open(input_image)
                    outputs = Image.open(output_image)

                    if compare_images(inputs, outputs):
                        os.remove(output_image)
                        time.sleep(2)
                print(i, end="th")

            print(folder + " finish")
        print(sep + " clear", sep="\n")

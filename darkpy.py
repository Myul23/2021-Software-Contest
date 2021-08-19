import os
import time, datetime
import numpy as np
from ctypes import *
import cv2

# darknet
import darknet  # detect image reverse=True
from threading import Thread, enumerate
from queue import Queue

# server
import requests
from firebase_admin import credentials, initialize_app, db, storage


# check
def check_set(weights_path, cfg_path, data_path):
    if not os.path.exists(weights_path):
        print("no weights file")
        exit()
    elif not os.path.exists(cfg_path):
        print("no cfg file")
        exit()
    elif not os.path.exists(data_path):
        print("no data file")
        exit()


def convert2relative(bbox):
    x, y, w, h = bbox
    _height = darknet_height
    _width = darknet_width
    return x / _width, y / _height, w / _width, h / _height


def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x = int(x * image_w)
    orig_y = int(y * image_h)
    orig_width = int(w * image_w)
    orig_height = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


# while loop
def waiting_user(user_queue, day):
    _time = time.time()
    while cap.isOpened():
        if user_queue.empty():
            user = db.reference("Request").get()
            print(datetime.datetime.now(), "Request User:", user)
            # user = "aaaa@gmail"

            if user is None:
                if datetime.datetime.now() - day >= datetime.timedelta(days=1):
                    Thread(target=learn_again).start()
                    day = datetime.datetime.now()
                continue

            db.reference("Request").delete()
            print("CV Detect Start")
            user_queue.put(user)
        elif time.time() - _time > 300:
            user = user_queue.get()


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height), interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)

        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, 0.1)
        detections_queue.put(detections)

        fps = int(1 / (time.time() - prev_time))
        fps_queue.put(fps)
        print("FPS: {}".format(fps))
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, fps_queue, server_queue):
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()

        if frame is not None:
            label = confidence = bbox_adjusted = None
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                break

            if bbox_adjusted is None:
                image = frame.copy()
            else:
                image = darknet.draw_boxes([(str(label), confidence, bbox_adjusted)], frame, class_colors)
                if not server_queue.empty():
                    _label, _confidence, _frame, _image = server_queue.pop()
                    if _confidence > confidence:
                        label, confidence, frame, image = _label, _confidence, _frame, _image
                # if not server_queue.empty():
                #     _label, _confidence, _frame, _image = server_queue.pop()
                #     if (label == _label) & (_confidence > confidence):
                #         confidence, frame, image = _confidence, _frame, _image
                #     else:
                #         server_queue.put([_label, _confidence, _frame, _image])

                server_queue.put([label, confidence, frame, image])
            cv2.imshow("prediction", image)

            if cv2.waitKey(fps) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()


def server_send(user_queue, server_queue):
    thread = 0.2
    while cap.isOpened():
        label, confidence, frame, image = server_queue.get()
        if user_queue.empty():
            continue

        user = user_queue.get()
        user_queue.put(user)
        confidence = float(confidence) / 100
        string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # -%f")

        if confidence < thread:
            part = "Admin"
        else:
            part = "/".join(["User", user, "unchecked"])

        # storage - image
        path = string + "_detect.jpg"
        blob = bucket.blob(path)
        blob.upload_from_string(cv2.imencode(".jpg", image)[1].tobytes(), content_type="image/jpeg")
        blob.make_public()

        # realtime db - info
        ref = db.reference("/".join([part, label]))
        if confidence < thread:
            _path = string + "_origin.jpg"
            _blob = bucket.blob(_path)
            _blob.upload_from_string(cv2.imencode(".jpg", frame)[1].tobytes(), content_type="image/jpeg")
            _blob.make_public()

            ref.update(
                {
                    string: {
                        "pred": "%0.2f" % (confidence),
                        "image": blob.public_url,
                        "date": string.split("_")[0],
                        "origin": _blob.public_url,
                    }
                }
            )
        else:
            ref.update({string: {"pred": "%0.2f" % (confidence), "image": blob.public_url, "date": string.split("_")[0]}})
    cap.release()


# learning again
def learn_again():
    print("re-learning")

    new_data_path = "data/yolo/images_labelsFormal/new_data"
    if not os.path.exists(new_data_path):
        os.mkdir(new_data_path)

    ref = db.reference("Retrain")
    contents = ref.get()
    if contents is None:
        return

    for date, content in contents.items():
        content = list(content.values())
        # print(f"date: {date}\nlabel: {content[0]}\nurl: {content[1]}")

        # save label text
        text_file = open(os.path.join(new_data_path, date) + ".txt", "w")
        text_file.write(content[0])
        text_file.close()

        # save image
        image_nparray = np.asarray(bytearray(requests.get(content[1]).content), dtype=np.uint8)
        image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        if image is not None:
            cv2.imwrite(os.path.join(new_data_path, date) + ".jpg", image)

            # remove file on db
            rm_blob = bucket.blob(content[1].split("/")[-1])
            rm_blob.delete()

        delete_user_ref = ref.child(date)
        delete_user_ref.delete()

    # learn again
    print_text = os.popen("python changePath.py").read()
    print(print_text)
    print_text = os.popen(
        "./darknet detector train custom/custom_parameter.cfg backup/custom_parameter_last.weights custom/custom_path.data -map"
    ).read()
    print(print_text)
    print("finish")


if __name__ == "__main__":
    weights_path = os.path.join(os.getcwd(), "backup/save/custom_parameter_last.weights")
    cfg_path = os.path.join(os.getcwd(), "custom/custom_parameter.cfg")
    data_path = os.path.join(os.getcwd(), "custom/custom_path.data")
    check_set(weights_path, cfg_path, data_path)

    # about yolov4 model
    network, class_names, class_colors = darknet.load_network(cfg_path, data_path, weights_path, batch_size=1)
    darknet_width = darknet.network_width(network)
    darknet_height = darknet.network_height(network)

    # server set
    cred = credentials.Certificate("base.json")
    initialize_app(
        cred,
        {
            "databaseURL": "https://recyclear-user-c81c3-default-rtdb.asia-southeast1.firebasedatabase.app/",
            "storageBucket": "recyclear-user-c81c3.appspot.com",
        },
    )
    bucket = storage.bucket()
    print("success")

    # main - video
    day = datetime.datetime.now()  # - datetime.timedelta(days=1)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("no video capturing")

    user_queue = Queue(maxsize=1)
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)
    server_queue = Queue()

    Thread(target=waiting_user, args=(user_queue, day)).start()
    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue, server_queue)).start()
    Thread(target=server_send, args=(user_queue, server_queue)).start()

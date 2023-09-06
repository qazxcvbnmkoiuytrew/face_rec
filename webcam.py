from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
import os
import numpy as np
import time

app = Flask(__name__)
video_stream = VideoCamera()

# 全局变量用于存储已拍摄的照片
captured_photos = []

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('cam.html', taken_photo=captured_photos[-1] if captured_photos else None)

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/take_photo', methods=['POST'])
def take_photo():
    global captured_photos
    frame = video_stream.get_frame()

    if frame:
        # 使用OpenCV将JPEG图像解码为NumPy数组
        nparr = np.frombuffer(frame, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 使用当前时间戳作为文件名
        timestamp = int(time.time())

        # 指定保存到"faces"子文件夹的路径
        output_folder = 'faces'

        # 确保目标文件夹存在，如果不存在则创建它
        os.makedirs(output_folder, exist_ok=True)

        # 创建完整的文件路径，将照片保存到"faces"子文件夹中
        photo_filename = os.path.join(output_folder, f'photo_{timestamp}.jpg')

        # 保存照片文件
        cv2.imwrite(photo_filename, image)

        # 将拍摄的照片添加到已拍摄的照片列表中
        captured_photos.append(photo_filename)

    return render_template('cam.html', taken_photo=captured_photos[-1])

@app.route('/save_photo', methods=['POST'])
def save_photo():
    return render_template('cam.html', captured_photos=captured_photos)

@app.route('/retake_photo', methods=['POST'])
def retake_photo():
    global captured_photos
    # 删除最后一张照片
    if captured_photos:
        last_photo = captured_photos.pop()
        os.remove(last_photo)

    return render_template('cam.html', taken_photo=captured_photos[-1] if captured_photos else None)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)



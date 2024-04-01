import cv2
import dlib
import torch
from scipy.spatial import distance as dist

# dlib的面部关键点检测器
predictor_path = "/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()

# 定义眼睛和嘴巴的纵横比计算函数
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    # 对于嘴巴关键点子集，正确的索引应该是：
    # 上嘴唇外侧中点 - 索引 2
    # 下嘴唇外侧中点 - 索引 6
    # 嘴角 - 索引 0 和 4
    # 因此，根据68个关键点的标注，对于仅包含嘴巴的列表（0到19），需要使用这些索引：
    A = dist.euclidean(mouth[2], mouth[6])  # 垂直距离
    C = dist.euclidean(mouth[0], mouth[4])  # 水平距离

    mar = A / C
    return mar


# 定义状态检测和计数变量
EYE_AR_THRESH = 0.5
MOUTH_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 0.5
MOUTH_AR_CONSEC_FRAMES = 1
blink_counter = 0
mouth_open_counter = 0
blink_total = 0
mouth_open_total = 0

# 启动摄像头
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        # 绘制人脸头像框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        # 计算眼睛和嘴巴的纵横比
        leftEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
        rightEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
        ear = (leftEAR + rightEAR) / 2.0
        mar = mouth_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(60, 68)])

        # 检测眨眼
        if ear < EYE_AR_THRESH:
            blink_counter += 1
        else:
            if blink_counter >= EYE_AR_CONSEC_FRAMES:
                blink_total += 1
            blink_counter = 0

        # 检测张嘴
        if mar > MOUTH_AR_THRESH:
            mouth_open_counter += 1
        else:
            if mouth_open_counter >= MOUTH_AR_CONSEC_FRAMES:
                mouth_open_total += 1
            mouth_open_counter = 0

    # 在视频帧上显示统计信息
    cv2.putText(frame, "Blinks: {}".format(blink_total), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Mouth Opens: {}".format(mouth_open_total), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 显示结果帧
    cv2.imshow("Frame", frame)

    # 按'q'退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()

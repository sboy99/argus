import cv2
import numpy as np
from cv2.typing import MatLike

class OpenCV:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.net, self.output_layers = self.__load_model(
            weights_path='models/dnn_model/yolov4-tiny.weights',
            config_path='models/dnn_model/yolov4-tiny.cfg',
        )
        self.classes = self.__load_classes('models/dnn_model/classes.txt')

    # --- Public methods --- # 

    def get_version(self) -> str:
        return cv2.__version__
    
    def get_frame(self):
        ret, frame = self.cap.read()
        return ret,frame
    
    def release(self):
        self.cap.release()

    def start_capturing(self):
        while True:
            ret,frame = self.get_frame()
            if not ret:
                break
            cv2.imshow('frame', self.__pipe_object_detection(frame))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.release()
        cv2.destroyAllWindows()

    # --- Private methods --- #

    def __load_model(self,weights_path:str,config_path:str) :
        net = cv2.dnn.readNet(weights_path, config_path)
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return net, output_layers

    def __load_classes(self,classes_path:str):
        with open(classes_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        return classes
    
    def __pipe_object_detection(self,frame:MatLike) -> MatLike:
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                for obj in detection:
                    scores = obj[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(obj[0] * width)
                        center_y = int(obj[1] * height)
                        w = int(obj[2] * width)
                        h = int(obj[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indices:
            i = i[0]
            box = boxes[i]
            x, y, w, h = box
            label = str(self.classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame

    # --- Destructor --- #

    def __del__(self):
        self.release()
        cv2.destroyAllWindows()
        
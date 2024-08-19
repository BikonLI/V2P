"""Video to pictures implement"""
import cv2
import os
from kivy.utils import platform


class Extract:
    
    count = 0        # count
    pic_count = 0
    total_frame = 0  # total_frame
    isRunning = 0
    
    def __init__(self, video) -> None:
        self.video = video
    
    def getTotalFrame(self):
        self.isRunning = True
        cap = cv2.VideoCapture(self.video)
        self.total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.total_frame <= 0:
            self.total_frame = 0
            while True:
                ret, frame = cap.read()
                if ret:
                    self.total_frame += 1
                else: break  
        cap.release()
        self.isRunning = False
        
    def start(self, size, rate, format, spin, path, func=lambda *args: None) -> None:
        # init
        self.isRunning = True
        self.pic_count = 0
        self.total_frame = 0
        self.count = 0

        cap = cv2.VideoCapture(self.video)
        while True:  
            ret, frame = cap.read()
            if not ret:  
                break 
                
            if self.count % rate == 0:

                if platform == "android":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if size:
                    cv2.resize(frame, size)

                # get shape  
                (h, w) = frame.shape[:2]  
                
                # calculate center
                center = (w // 2, h // 2)  
                
                # get spin matrix  
                M = cv2.getRotationMatrix2D(center, spin, 1.0)  
                
                # implement the matrix on the frame  
                frame = cv2.warpAffine(frame, M, (w, h))  

                output_path = os.path.join(path, f"{self.pic_count:05}{format}")
                # cv2.waitKey(1)
                # cv2.imshow("", frame)
                result = cv2.imwrite(output_path, frame)

                self.pic_count += 1
            self.count += 1
        func()
            

if __name__ == "__main__":
    e = Extract()
    e.start("C:/Users/Li/Videos/CMDgame.mp4", size=(1200, 840), rate=1, format=".jpg", spin=90, path=r".\test")
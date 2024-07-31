"""Video to pictures implement"""
import cv2
import os
from utility import write


class Extract:
    
    count = 0
    pic_count = 0
    total_frame = 0

    def start(self, video, size, rate, format, spin, path, func) -> None:
        
        write.log("Extract", "started")
        # init
        self.pic_count = 0
        self.total_frame = 0
        self.count = 0
        
        # get total frame
        write.log("Extract", "Try to open the video") 
        cap = cv2.VideoCapture(video)
        self.total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        write.log("Extract", f"Try to gain the video total frame {self.total_frame}") 
        if self.total_frame <= 0:
            self.total_frame = 0
            while True:
                ret, frame = cap.read()
                if ret:
                    self.total_frame += 1
                else: break
            
            cap.release()
            write.log("Extract", f"Gained the video total frame {self.total_frame}") 

        cap = cv2.VideoCapture(video)
        while True:  
            write.log("Extract", f"Try to read frame {self.count}") 
            ret, frame = cap.read()
            write.log("Extract", f"Frame read result {ret}") 
            if not ret:  
                break 
                
            if self.count % rate == 0:
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
                write.log("Extract", f"Save pic as {output_path} {result}")

                self.pic_count += 1
            self.count += 1
        func()
   
            
extract = Extract()
if __name__ == "__main__":
    e = Extract()
    e.start("C:/Users/Li/Videos/CMDgame.mp4", size=(1200, 840), rate=1, format=".jpg", spin=90, path=r".\test")
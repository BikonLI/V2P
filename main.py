# Extract frame from videos
import cv2
import json
import os
import webbrowser
from time import sleep

# json_path = '/storage/emulated/0/Download/PathSettings.json'


url = "https://b23.tv/tW2F1h2"


class VideoToPictures:

    def __init__(self, json_path):
        """获取视频路径，获取照片路径"""
        strange_str = '%'
        self.__json_path = json_path
        self.__sub = 1
        with open(self.__json_path, mode='r', encoding="UTF-8") as settings:
            path_dict: dict = json.load(settings)
            get_path = list()
            for BullShit, Path in path_dict.items():
                if BullShit != "#":
                    get_path.append(Path)
        for index in range(len(get_path)):
            if isinstance(get_path[index], list):
                if get_path[index][-1] == 0:
                    self.__PathVideo = get_path[index][0]
                else:
                    self.__PathPictures = get_path[index][0]
            elif (isinstance(get_path[index], float)
                  or isinstance(get_path[index], int)):
                self.__Rate = get_path[index]
            else:
                self.__Format: str = get_path[index]
        print("使用教程： https://b23.tv/tW2F1h2")
        sleep(1.2)
        print(f"视频路径获取成功：{self.__PathVideo}")
        sleep(1.2)
        print(f"照片输出路径获取成功：{self.__PathPictures}")
        sleep(1.2)
        print(f"采样率获取成功：rate = {(100/self.__Rate):.2f}%")
        sleep(1.2)
        print(f"照片格式获取成功： {self.__Format}")
        sleep(1.2)

    def __name(self):
        """对照片进行命名"""
        if self.__sub > 9999:
            return False
        name = str(self.__sub)
        num_of_zero = 5-len(name)
        for times in range(num_of_zero):
            name = '0' + name
        return name

    def convert(self):

        cap = cv2.VideoCapture(self.__PathVideo)    # 打开视频
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) // self.__Rate)   # 获取总帧
        print(f"总照片数为：{total_frame}")
        if cap.isOpened():
            sleep(1.2)
            print("成功读取视频")
            count = 0    # 帧率数
            # self.__sub   采样数
            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if ret:     # 成功获取下一帧
                        if count % self.__Rate == 0:    # 每rate帧采样一次
                            picture_name = self.__name() + self.__Format    # 对照片进行命名
                            cv2.imwrite(self.__PathPictures + picture_name, frame)    # 生成照片
                            if self.__sub <= total_frame:
                                print(f"\r照片生成进度：{self.__sub}/{total_frame}", end='')
                            sleep(0.3)
                            self.__sub += 1
                    if not ret:
                        print()
                        break
                    count += 1
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                cap.release()  # 释放视频
                cv2.destroyAllWindows()
                print("转化完成")
                sleep(0.3)
            except TypeError as false:
                print(f"提取帧失败！")
                print("照片过多,最多支持99999张")
                sleep(1.2)
                print(false)
            except Exception as false:
                print(f"提取帧失败！")
                sleep(1.2)
                print(false)
        else:
            print("视频获取失败，请检查路径是否正确，存储权限是否授予APP")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_path = input("请输入配置文件存放路径(example: D:/type/your/json/path/PathSettings.json)：")
    try:
        standard = VideoToPictures(json_path=json_path)   # 创建实例
    except Exception as e:
        print(f"获取配置文件失败，失败原因：{e}")
        sleep(1.2)
        print('请查看教程： https://b23.tv/tW2F1h2')
    else:
        standard.convert()
    finally:
        for i in range(2, -1, -1):
            print(f"\r本窗口将会在{i}秒内自动关闭...", end="")
            sleep(1)
        webbrowser.open(url=url)






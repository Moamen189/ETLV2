import cv2
import pandas as pd
from threading import *
import pathlib
import os
from BirdMoveDetect import BirdMoveDetect
class CVDetector(Thread):
    def __init__(self,cap, queue, path, sem, sentinel, attrs):
        super().__init__()
        self.queue = queue
        self.sentinel = sentinel
        self.MAX_NUM_BIRDS = 0
        self.path = path
        self.birdsCascade = cv2.CascadeClassifier(path)
        self.cap = cap
        self.attrs = attrs
        self.sem = sem

    def getStats(self):
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        codec = self.cap.get(cv2.CAP_PROP_FOURCC)
        durationSec = frame_count/fps * 1000
        return (fps,frame_count,durationSec)

    def process(self):
        self.sem.acquire()
        frame = self.queue.get()
        frames_count = self.getStats()[1]
        count = 0
        last_percent = 0
        while frame is not self.sentinel:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            birds = get
            if (len(birds)>=self.MAX_NUM_BIRDS):
                self.MAX_NUM_BIRDS = len(birds)
            frame = self.queue.get()
            count +=1
            if (count/frames_count)>last_percent+0.03:
                last_percent = count/frames_count
                print('Processing... ',int(last_percent*100),'%')
        print('max number is: ',self.MAX_NUM_BIRDS)
        data = {str(self.MAX_NUM_BIRDS)}
        df = pd.DataFrame(data, columns=['MAX_COUNT_OF_BIRDS'])
        self.attrs['df'] = df
        self.sem.release()

    def run(self):
        self.process()
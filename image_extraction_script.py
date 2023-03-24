import pandas as pd
import cv2
import os
from datetime import datetime

class ExtractImageFromVideo:
    def __init__(self, filepath, labelspath):
        self.filepath = filepath
        self.labelspath = labelspath
        self.df = pd.read_excel(self.filepath, sheet_name='data')

    def extract_images(self, path, angle, f):
        '''
        Read video path
        Extract frames from 2-6 seconds
        write angle and image path into a csv file
        '''
        cam = cv2.VideoCapture(path)
        cam.set(cv2.CAP_PROP_POS_MSEC,2000)   
        try:
            
            # creating a folder named data
            if not os.path.exists('data'):
                os.makedirs('data')
        
        # if not created then raise error
        except OSError:
            print ('Error: Creating directory of data')
        
        # frame
        currentframe = 0
        time_skips = float(500)
        totalTime = 0 

    
        #capturing 2-6 seconds of videos to extract images
        while(totalTime < 6000):
            
            # reading from frame
            ret,frame = cam.read()
        
            if ret:
                # if video is still left continue creating images
                filename = angle+str(int(datetime.timestamp(datetime.now()))) +str(currentframe)+ '.jpeg'
                name = './data/' + filename
                gcspath = 'gs://bkt-mets-d-cc212-cmucapstone2023-mllb/angle_images/'

                #Create the dataset generation script
                f.write(gcspath + filename + ','+angle+'\n')
                #skipping by 0.5 seconds
                totalTime = currentframe*time_skips
                cam.set(cv2.CAP_PROP_POS_MSEC,(totalTime)) 
                print ('Creating...' + name)
        
                # writing the extracted images and compressed it
                cv2.imwrite(name, frame, [cv2.IMWRITE_JPEG_QUALITY, 30])
        
                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                break
        
        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
    
    def process(self):
        f = open(self.labelspath,'w')
        self.df.apply(lambda x: self.extract_images(x['path'], x['camera_angle'], f), axis=1)
        f.close()

if __name__ == '__main__':
    v = ExtractImageFromVideo('angle_data.xlsx','angle_image_data.csv')
    v.process()

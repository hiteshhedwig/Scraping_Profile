import cv2
import numpy as np
import operator
from fer import FER
import matplotlib.pyplot as plt 


def annotate_image(img_n, annotations):

  #x=(k[0]['box'][0],k[0]['box'][3])
  #y=(k[0]['box'][1],k[0]['box'][2])
  k=annotations
  x= k[0]['box'][0]
  y= k[0]['box'][1]
  w = k[0]['box'][2]
  h= k[0]['box'][3]
  font = cv2.FONT_HERSHEY_SIMPLEX 
  org = (x+w, y+h) 
    
  # fontScale 
  fontScale = 1
    
  # Blue color in BGR 
  color = (255, 0, 0) 
  emotion= max(k[0]['emotions'].items(), key=operator.itemgetter(1))[0]
  prob= k[0]['emotions'][emotion]

  cv2.rectangle(img_n, (x, y), (x+w, y+h), (0, 255, 255), 2)
  img_n = cv2.putText(img_n, f'{emotion}: {prob}', org, font,  
                   fontScale, color, 2, cv2.LINE_AA) 


  return img_n

if __name__=='__main__':
    # Read video
    cap=cv2.VideoCapture('video.mp4')
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

    #cap.set(CV_CAP_PROP_FOURCC, CV_FOURCC('H', '2', '6', '4'))
    size=(width, height)
    print("size", size)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('testing.avi',fourcc, 20, size)

    while (1):
        _,img=cap.read()    

        detector = FER(mtcnn=True)
        k=detector.detect_emotions(img)

        img_new= img.copy() 
        anno=annotate_image(img_new,k)
        print('Writing down result')
        out.write(anno)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
        
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
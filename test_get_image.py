import cv2
import numpy as np 
import pandas as pd

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0
blue = []
green = []
red = []

while True:
    ret, frame = cam.read()
    
    colour = frame[300, 366]
    r = colour[2]
    g = colour[1]
    b = colour[0]

    
    # computing the mean
    # b_mean = np.mean(b)
    # g_mean = np.mean(g)
    # r_mean = np.mean(r)
    blue.append(b)
    green.append(g)
    red.append(r)
    
    
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)
    
    k = cv2.waitKey(1)
    if k%256 == 27:
    #ESC pressed
        print("Escape hit , closing...")
        break

    elif k%256 ==32:
    #SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter +=1
    

cam.release

cv2.destroyAllWindows()

colours = {"blue": blue, "green": green, "red": red}
dataframe = pd.DataFrame(colours)
dataframe.to_csv("colours.csv", index=False)
print(b, g, r)
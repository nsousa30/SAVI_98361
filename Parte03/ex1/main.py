#!/usr/bin/env python3
import cv2 as cv
import copy
import numpy as np
import time

def main():

    point_start = (687, 362)
    point_end = (847, 515)

    cap = cv.VideoCapture('../docs/traffic.mp4')

    frame_number = 0
    average = 134
    num_cars = 0
    change_detected = False
    tic = time.time()

    while(cap.isOpened()):
        
        ret, image_rgb = cap.read()
        image_gui = copy.deepcopy(image_rgb)

        image_gray = cv.cvtColor(image_rgb, cv.COLOR_BGR2GRAY)

        image_roi = image_gray[point_start[1]:point_end[1], point_start[0]:point_end[1]]
        average_previous = average
        average = np.mean(image_roi)

        t = 10.0
        if abs(average - average_previous) > t:
            print('Change Detected!')
            num_cars +=1 
        else:
            change_detected=False
        
        if previous_change_detected == False and change_detected == True:
            num_cars +=1

        cv.rectangle(frame,(point_start[0],point_start[1]),(point_end[0], point_end[1]),(0,255,0),4)

        image_gui = cv.putText(image_gui, 'Frame' + str(frame_number), (500,20), cv.FONT_HERSHEY_SIMPLE,
                               0.7, (255,255,0),2, cv.LINE_AA)
        image_gui = cv.putText(image_gui, 'Avg' + str(round(average,1)), (500,45), cv.FONT_HERSHEY_SIMPLE,
                               0.7, (0,255,255),2, cv.LINE_AA)
        image_gui = cv.putText(image_gui, 'NCars' + str(round(average,1)), (500,70), cv.FONT_HERSHEY_SIMPLE,
                               0.7, (0,255,0),2, cv.LINE_AA)

        cv.imshow('GUI', image_gui)

        cv.imshow('ROI',image_roi)

        

        if cv.waitKey(25) & 0xFF == ord('q'):
            break

        frame_number += 1

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
import cv2 as cv


def main():
    scene = cv.imread('../images/scene.jpg')
    template = cv.imread('../images/wally.png')

    result = cv.matchTemplate(scene,template, cv.TM_CCOEFF_NORMED) #???

    _, value_max, _, max_loc = cv.minMaxLoc(result)
    print(value_max)
    print(max_loc)

    h,w,_= template.shape
    
    cv.rectangle(scene, (max_loc[0],max_loc[1]),(max_loc[0]+w, max_loc[1]+h),(0,255,0),4)

    cv.imshow('Scene',scene)
    cv.imshow('Template',template)
    cv.waitKey(0)
if __name__ == "__main__":
    main()
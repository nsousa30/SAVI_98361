#!/usr/bin/env python3
import cv2 as cv
import copy

def main():

    scene = cv.imread('../images/scene.jpg')
    template = cv.imread('../images/wally.png')

    result = cv.matchTemplate(scene, template, cv.TM_CCOEFF_NORMED)

    _, value_max, _, max_loc = cv.minMaxLoc(result)
    print(value_max)
    print(max_loc)

    h, w, _ = template.shape
    
    gray_scene = cv.cvtColor(scene, cv.COLOR_BGR2GRAY)


    color_scene = cv.cvtColor(gray_scene, cv.COLOR_GRAY2BGR)

    color_scene[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w] = scene[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]
    print(template.shape)
    print(scene[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w].shape)
    cv.imshow('Scene', color_scene)
    cv.waitKey(0)

if __name__ == "__main__":
    main()


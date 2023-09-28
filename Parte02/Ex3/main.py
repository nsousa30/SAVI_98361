#!/usr/bin/env python3
import cv2 as cv
import copy

selected_region= None
region_selected = False

def on_mouse(event, x, y, flags, param):
    global selected_region, region_selected

    if event == cv.EVENT_LBUTTONDOWN:
        
        selected_region = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        
        region_selected = True
        selected_region += (x, y)

def main():

    global selected_region, region_selected

    scene = cv.imread('../images/school.jpg')
    
    cv.namedWindow('Scene')
    cv.setMouseCallback('Scene',on_mouse)

    while True:
        cv.imshow('Scene', scene)
        
        if region_selected:
            
            x1,y1,x2,y2 = selected_region
            template = scene[y1:y2, x1:x2]

            result = cv.matchTemplate(scene,template, cv.TM_CCOEFF_NORMED)

            _, _, _, max_loc = cv.minMaxLoc(result)
            h,w,_= template.shape
            cv.rectangle(scene, (max_loc[0],max_loc[1]),(max_loc[0]+w, max_loc[1]+h),(0,255,0),4)

            cv.imshow('Template', template)
            region_selected = False


        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break

    cv.destroyAllWindows()

    scene = cv.imread('../images/beach.jpg')
    
    cv.namedWindow('Scene')
    cv.setMouseCallback('Scene',on_mouse)

    while True:
        cv.imshow('Scene', scene)
        
        if region_selected:
            
            x1,y1,x2,y2 = selected_region
            template = scene[y1:y2, x1:x2]

            result = cv.matchTemplate(scene,template, cv.TM_CCOEFF_NORMED)

            _, _, _, max_loc = cv.minMaxLoc(result)
            h,w,_= template.shape
            cv.rectangle(scene, (max_loc[0],max_loc[1]),(max_loc[0]+w, max_loc[1]+h),(0,255,0),4)

            cv.imshow('Template', template)
            region_selected = False


        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break


if __name__ == "__main__":
    main()
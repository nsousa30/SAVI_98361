#!/usr/bin/env python3
import cv2
import copy
def main():
    #Load Image
    image_original = cv2.imread('../images/lake.jpg')


    h,w,nc = image_original.shape

    image = copy.deepcopy(image_original)
    reductions = [0,10,20,40,50]
    for reduction in reductions:   
        for row in range (0,h):
            for col in range (int(w/2),w):
                image[row, col,0] = max(image[row,col,0]-reduction,0)
                image[row, col, 1] = max(image[row,col,1]-reduction,0)
                image[row, col, 2] = max(image[row,col,2]-reduction,0)

        cv2.imshow('Nightfall',image)
        cv2.waitKey(0)
    
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
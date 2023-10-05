#!/usr/bin/env python3
import cv2 as cv
import copy
import numpy as np
import time

selected_region= None
region_selected = False
roi_dict = {}

def on_mouse(event, x, y, flags, param):
    global selected_region, region_selected

    if event == cv.EVENT_LBUTTONDOWN:
        
        selected_region = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        
        region_selected = True
        selected_region += (x, y)

vehicle_colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    
}

def get_vehicle_color(image_rgb, roi):
    
    point_start = roi['point_start']
    point_end = roi['point_end']
    image_roi = image_rgb[point_start[1]:point_end[1], point_start[0]:point_end[0]]

    
    average_color = np.mean(image_roi, axis=(0, 1))
    color_name = 'unknown'
    min_distance = float('inf')

    for color, color_value in vehicle_colors.items():
        distance = np.linalg.norm(average_color - color_value)
        if distance < min_distance:
            min_distance = distance
            color_name = color

    return color_name

def main():

    global selected_region, region_selected

    cap = cv.VideoCapture('docs/traffic.mp4')

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        exit()


    ret, frame = cap.read()

    if not ret:
        print("Não foi possível capturar o primeiro frame.")
        exit()

    cap.release()

    

    cv.namedWindow('Frame')
    cv.setMouseCallback('Frame',on_mouse)

    n=1
    while True:
        cv.imshow('Frame',frame)
        
        if region_selected:
            
            x1,y1,x2,y2 = selected_region
            
            cv.rectangle(frame, (x1,y1),(x2, y2),(0,255,0),4)

            region_data = {
            'point_start': (x1, y1),
            'point_end': (x2, y2),
            'average': 0,
            'average_previous': 130,
            'tic': time.time(),
            'num_cars': 0
            }
            
            roi_dict[n] = region_data  
            region_selected = False
            n += 1

        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break

        
    cv.destroyAllWindows()

    cap = cv.VideoCapture('docs/traffic.mp4')

    frame_number = 0

    set = False

    while(cap.isOpened()):

        # Capture frame-by-frame
        ret, image_rgb = cap.read()
        if ret is False:
            break

        image_gui = copy.deepcopy(image_rgb)

        # Convert to gray
        image_gray = cv.cvtColor(image_rgb, cv.COLOR_BGR2GRAY)

        for roi_key in roi_dict:
            roi = roi_dict[roi_key]
            # Get sub_image
            point_start = roi['point_start']
            point_end = roi['point_end']

            image_roi = image_gray[point_start[1]:point_end[1] , point_start[0]:point_end[0]]
            if set == False:
                roi['average'] = np.mean(image_roi)

            # Compute average
            roi['average_previous'] = roi['average']
            roi['average'] = np.mean(image_roi)
            
            # Blackout
            t = 10.0
            blackout_threshold = 1.0
            time_since_tic = time.time() - roi['tic']

            if abs(roi['average'] - roi['average_previous']) > t and time_since_tic > blackout_threshold:
                roi['tic'] = time.time()
                roi['num_cars'] = roi['num_cars'] + 1
                vehicle_color = get_vehicle_color(image_rgb, roi)

                
                print(f"Veículo passou na faixa {roi_key} de cor {vehicle_color}")

        set = True


        # --------------------------------------
        # Visualization
        # --------------------------------------


        image_gui = cv.putText(image_gui, 'Frame ' + str(frame_number), (500, 20), cv.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255,255,0), 2, cv.LINE_AA)


        for roi_key in roi_dict:
            roi = roi_dict[roi_key]
            point_start = roi['point_start']
            point_end = roi['point_end']
            cv.rectangle(image_gui, (point_start[0], point_start[1]), (point_end[0], point_end[1]), (0,255,0), 4)

            image_gui = cv.putText(image_gui, 'Avg ' + str(round(roi['average'],1)), (point_start[0], 45), cv.FONT_HERSHEY_SIMPLEX, 
                            0.7, (0,255,255), 2, cv.LINE_AA)
            image_gui = cv.putText(image_gui, 'NCars ' + str(round(roi['num_cars'],1)), (point_start[0], 70), cv.FONT_HERSHEY_SIMPLEX, 
                            0.7, (0,255,0), 2, cv.LINE_AA)


        cv.imshow('GUI',image_gui)
        # cv2.imshow('Gray',image_gray)
        # cv2.imshow('ROI',image_roi)
    
        if cv.waitKey(35) & 0xFF == ord('q') :
            break

        frame_number += 1
if __name__ == "__main__":
    main()


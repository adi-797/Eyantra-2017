############################################################################
#									   #
#	    Overlaying of images and video processing	                   #
#									   #
############################################################################

########################################################################################
#                                                                                      #
# Team Id           eYRC_931                                                           #
# Author List       Abhaysheel Anand, Aditya Arora, Bhawana Chhaglani, Milap Sharma    #
# Filename          Task-1B_main.py                                                    #
# Theme             Planter Bot                                                        #
# Fuctions          writecsv, main                                                     #
#                                                                                      #
########################################################################################

#classes and subclasses to import
import cv2
import numpy as np
import os
import time
import datetime
t=time.time()
#filename = 'results1B_931.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    #global filename
    #open csv file in append mode
    filep = open('results1B_931.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

#####################################################################################################
#   COMMENTS ON THE RIGHT MOST SIDE
#####################################################################################################


def main(video_file_with_path):
    list=[]
    cap = cv2.VideoCapture(video_file_with_path)                                                                                            #capturing video
    fourcc=cv2.VideoWriter_fourcc(*'XVID')                                                                                                  #specifies the video codec
    #####passing frame value 16.8 as a 39 second(demanded duration of video) is created using this value only and at 16fps a 41 second value is created#####
    out=cv2.VideoWriter('Video_output.mp4', fourcc, 16.8, (1280,720))                                                                       #VideoWriter object which accepts fps, frame size
    image_red = cv2.imread("yellow_flower.png",-1)                                                                                          #reading the image
    image_blue = cv2.imread("pink_flower.png",-1)                                                                                           #reading the image
    image_green = cv2.imread("red_flower.png",-1)                                                                                           #reading the image
    rval, frame=cap.read()                                                                                                                  #capturing frames
    #count = 0                                                                                                                               #
    #start_time = datetime.datetime.now()                                                                                                    #
                                                                                                                                            #
    while rval:                                                                                                                             #loop initialization for video processing
        rval, frame = cap.read()                                                                                                            #setting individual frames for video
        if rval is true:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                                                                      #converting from BGR to GRAY
        else:
            continue
        ret, thresh = cv2.threshold(gray, 127, 255, 1)                                                                                      #setting threshold for finding contours
        _, contours, hierarchy = cv2.findContours(thresh, 1, 2)                                                                             #finding contours
        i=0                                                                                                                                 #
        for cnt in contours:                                                                                                                #initiating loop for individual contours
            i=i+1                                                                                                                           #
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)                                                           #finding the vertices
            if len(approx) == 5:                                                                                                            #logic for pentagon
                shape = "pentagon"                                                                                                          #
            elif len(approx) == 3:                                                                                                          #logic for triangle
                shape = "triangle"                                                                                                          #
            elif len(approx) == 4:                                                                                                          #logic for shape with 4 edges
                slope1 = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0])                                          #
                slope2 = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0])                                          #
                slope3 = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0])                                          #
                slope4 = (approx[3][0][1] - approx[0][0][1]) / (approx[3][0][0] - approx[0][0][0])                                          #
                slope = []                                                                                                                  #
                c = 0                                                                                                                       #
                slope.append(slope1)                                                                                                        #
                slope.append(slope2)                                                                                                        #
                slope.append(slope3)                                                                                                        #
                slope.append(slope4)                                                                                                        #
                for s in slope:                                                                                                             #
                    if s < 0:                                                                                                               #
                        c = c + 1                                                                                                           #
                if c == 1:                                                                                                                  #logic for trapezium
                    shape = "trapezium"                                                                                                     #
                else:                                                                                                                       #logic for rhombus
                    shape = "rhombus"                                                                                                       #                                                                                                                                                                                              #
            elif len(approx) == 6:                                                                                                          #logic for hexagon
                shape = "hexagon"                                                                                                           #                                                                                                                                             #
            elif len(approx) > 15:                                                                                                          #logic for circle
                shape = "circle"                                                                                                            #
            M = cv2.moments(cnt)                                                                                                            #finding moments
            cx = int(M['m10'] / M['m00'])                                                                                                   #finding x coordinate of centroid of object
            cy = int(M['m01'] / M['m00'])                                                                                                   #finding y coordinate of centroid of object        
            color = frame[cy, cx]                                                                                                           #finding color of the object by detecting the color at its centroid
            if (color[0] >= 0 and color[0] <= 10 and color[1] >= 0 and color[1] <= 10 and color[2] >= 250 and color[2] <= 255):             #logic for red
                colour = "red"                                                                                                              #
            elif (color[0] >= 250 and color[0] <= 255 and color[1] >= 0 and color[1] <= 10 and color[2] >= 0 and color[2] <= 10):           #logic for blue
                colour = "blue"                                                                                                             #
            elif (color[0] >= 0 and color[0] <= 10 and color[1] >= 120 and color[1] <= 130 and color[2] >= 0 and color[2] <= 10):           #logic for green
                colour = "green"                                                                                                            #
            #####passing mutlitple range of cx so as to create a threshold gap to counter the error caused due to discrepancy#####    
            if cx not in list and cx+2 not in list and cx+1 not in list and cx-1 not in list and cx-2 and cx+3 not in list and cx+4 not in list and cx-3 not in list and cx-4 and cx+5 not in list and cx-5 not in list:            
                list.append(i)                                                                                                              #appending i
                list.append(colour)                                                                                                         #appending color
                list.append(cx)                                                                                                             #appending centroid
            writecsv(colour, shape, (cx, cy))                                                                                               #calling writecsv to write the .csv file
        if len(contours)>0:                                                                                                                 #LOGIC FOR OVERLAY ON OBJECTS
            if (list[3 * (len(contours) - 1) + 1] == "red"):                                                                                #overlay on red object
                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])                                                   #
                overlay_image = cv2.resize(image_red, (h, w))                                                                               #
                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)                                   #
            elif (list[3 * (len(contours) - 1) + 1] == "blue"):                                                                             #overlay on blue object
                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])                                                   #
                overlay_image = cv2.resize(image_blue, (h, w))                                                                              #
                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)                                   #
            elif (list[3 * (len(contours) - 1) + 1] == "green"):                                                                            #overlay on green
                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])                                                   #
                overlay_image = cv2.resize(image_green, (h, w))                                                                             #
                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)                                   #LOGIC FOR OVERLAY ENDS HERE                                                                                                                                              
        out.write(frame)                                                                                                                    #saving the video file
        #cv2.imshow("image", frame)                                                                                                          #for showing the output video
        #cv2.waitKey(1)                                                                                                                     #
    cap.release()                                                                                                                           #releasing video frames
    #end_time = datetime.datetime.now()                                                                                                      #
    #tp = end_time - start_time                                                                                                              #
    cv2.destroyAllWindows()                                                                                                                 #


#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#####################################################################################################
    
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main('./Video.mp4')
    print time.time()-t


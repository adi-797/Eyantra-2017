############################################################################
#									   #
#	    Color, Shape, Centroid detection in a given image		   #
#									   #
############################################################################

########################################################################################
#                                                                                      #
# Team Id           eYRC_931                                                           #
# Author List       Abhaysheel Anand, Aditya Arora, bhawana Chhaglani, Milap Sharma    #
# Filename          Task-1A_main.py                                                    #
# Theme             Planter Bot                                                        #
# Fuctions          writecsv, main                                                     #
#                                                                                      #
########################################################################################

#classes and subclasses to import

import cv2
import numpy as np
import os
import time
t=time.time()
#filename = 'results1A_931.csv'

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################

#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    #global filename
    #open csv file in append mode
    filep = open('results1A_931.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()
#################################################################################################
#   ALL COMMENTS ON RIGHT MOST SIDE
#################################################################################################
def main(path):

    list = []
    img_name=path                                                                                                                               #for input images                     
    list.append(path)                                                                                                                           #appending the list with input image name                
    img = cv2.imread(img_name, cv2.IMREAD_COLOR)                                                                                                #reading input image for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                                                                                #converting BGR to GRAY
    ret, thresh = cv2.threshold(gray, 127, 255, 1)                                                                                              #creating a threshold for finding contours
    _, contours, hierarchy = cv2.findContours(thresh, 1, 2)                                                                                     #finding contours of the objects
    #print len(contours)                                                                                                                        #for printing the number of objects
    for cnt in contours:                                                                                                                        #intiating loop
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)                                                                   #finding the vertices
        if len(approx) == 5:                                                                                                                    #logic for pentagon
            shape = "pentagon"                                                                                                                  #                                                                                                                           #
                                                                                                                                                #
                                                                                                                                                #
        elif len(approx) == 3:                                                                                                                  #logic for triangle
            shape = "triangle"                                                                                                                  #
                                                                                                                                                #                        
        elif len(approx) == 4:                                                                                                                  #logic for shape with 4 edges
            slope1 = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0])                                                  #
            slope2 = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0])                                                  #
            slope3 = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0])                                                  #
            slope4 = (approx[3][0][1] - approx[0][0][1]) / (approx[3][0][0] - approx[0][0][0])                                                  #
            slope = []                                                                                                                          #
            c = 0                                                                                                                               #
            slope.append(slope1)                                                                                                                #
            slope.append(slope2)                                                                                                                #
            slope.append(slope3)                                                                                                                #
            slope.append(slope4)                                                                                                                #
                                                                                                                                                #
            for s in slope:                                                                                                                     #
                if s < 0:                                                                                                                       #
                    c = c + 1                                                                                                                   #
            if c == 1:                                                                                                                          #for trapezium
                shape = "trapezium"                                                                                                             #
            else:                                                                                                                               #for square
                shape = "rhombus"                                                                                                               #
                                                                                                                                                #
        elif len(approx) == 6:                                                                                                                  #
            shape = "hexagon"                                                                                                                   #logic for hexagon
                                                                                                                                                #
        elif len(approx) > 15:                                                                                                                  #logic for circle
            shape = "circle"                                                                                                                    #
                                                                                                                                                #
        M = cv2.moments(cnt)                                                                                                                    #finding moments for obtaining centroids
        cx = int(M['m10'] / M['m00'])                                                                                                           #centoid in x axis
        cy = int(M['m01'] / M['m00'])                                                                                                           #centroid in y axis
        color = img[cy, cx]                                                                                                                     #finding color of the object buy detecting the color at its centroid
        if (color[0] >=0 and color[0]<=10 and color[1] >= 0 and color[1] <= 10 and color[2] >= 250 and color[2] <= 255):                        #logic for red
            color = "red"                                                                                                                       #
        elif (color[0] >=250 and color[0]<=255 and color[1] >= 0 and color[1] <= 10 and color[2] >= 0 and color[2] <= 10):                      #logic for blue
            color = "blue"                                                                                                                      #
        elif (color[0] >=0 and color[0]<=10 and color[1] >= 120 and color[1] <= 130 and color[2] >= 0 and color[2] <= 10):                      #logic for green
            color = "green"                                                                                                                     #
        font = cv2.FONT_HERSHEY_SIMPLEX                                                                                                         #setting the font for text overlay
                                                                                                                                                #
        cv2.putText(img, color, (cx - 40, cy - 40), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)                                                       #overlaying text on the output image
        cv2.putText(img, shape, (cx - 20, cy - 20), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)                                                       #
        cv2.putText(img, "(" + str(cx) + "," + str(cy) + ")", (cx, cy), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)                                   #
                                                                                                                                                #
        element = color + "-" + shape + "-" + str(cx) + "-" + str(cy)                                                                           #generating an element to store information of every object
        list.append(element)                                                                                                                    #appending information in the list
        writecsv(color,shape,(cx,cy))                                                                                                           #calling fuction writecsv to update the .csv file created
    #cv2.imshow("image", img)                                                                                                                    #showing the output image
    temp = filter(lambda x : x != ".", path)                                                                                                    #logic for removing .png from image name
    temp = filter(lambda x : x != "p", temp)                                                                                                    #
    temp = filter(lambda x : x != "n", temp)                                                                                                    #
    temp = filter(lambda x : x != "g", temp)                                                                                                    #
    output_name= temp + "output.png"                                                                                                            #adding output.png so as to obtain the desired output image name
    cv2.imwrite(output_name, img)                                                                                                               #saving the output image
    #cv2.waitKey(0)                                                                                                                              #wait until user presses any key
    #cv2.destroyAllWindows()                                                                                                                     #closing all openend windows
    return list                                                                                                                                 #returns list when main() is called 

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    #global filename
    mypath = '.'
    #getting all files in the directory
    #APPENDED THE DESIRED IMAGE FILE ( SHIFT FROM THE ORIGINAL EDIT PROVIDED BY EYANTRA AS IT WAS NOT WORKING )
    onlyfiles=[]
    for f in os.listdir(mypath):
        if f.endswith(".png"):
            onlyfiles.append(f)                                                                                                                 
    #onlyfiles = [join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('results1A_931.csv', 'a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        #for printing text output of the processed image
        
        print data
        #open the csv
        filep = open('results1A_931.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
        print time.time()-t

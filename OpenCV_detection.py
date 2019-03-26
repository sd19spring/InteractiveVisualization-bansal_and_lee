import cv2, os, time
import numpy as np

class Detection(object):

    THRESHOLD = 1500
    


    def __init__(self, image):
        # Initializes the detected image
        self.previousTime = 0
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.num = 3

    def __del__(self):
        print ("detection deleted")

    def get_active_cell(self, image, webcam):

        if(self.num == 0):
            self.num = 1

        # obtain motion between previous and current image
        # gets the current image frame
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gets the difference between the current image frame and the previous image frame
        delta = cv2.absdiff(self.previous_gray, current_gray)
        # converts the delta to a readable image
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        # store current image
        self.previous_gray = current_gray

        # set cell width
        height, width = threshold_image.shape[:2]
        height = height / 3
        # there are 12 keys in a piano register - 12 white natural keys and 5 black sharp/flat keys
        cell_width = width/12

        # store motion level for each cell
        # creates a cell in the array for each of the 12 keys
        cells = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # C natural
        cells[0] = cv2.countNonZero(threshold_image[0:height, 0:cell_width])
        # C sharp
        cells[1] = cv2.countNonZero(threshold_image[0:height, cell_width:cell_width*2])
        # D natural
        cells[2] = cv2.countNonZero(threshold_image[0:height, cell_width*2:cell_width*3])
        # D sharp
        cells[3] = cv2.countNonZero(threshold_image[0:height, cell_width*3:cell_width*4])
        # E natural
        cells[4] = cv2.countNonZero(threshold_image[0:height, cell_width*4:cell_width*5])
        # F natural
        cells[5] = cv2.countNonZero(threshold_image[0:height, cell_width*5:cell_width*6])
        # F sharp
        cells[6] = cv2.countNonZero(threshold_image[0:height, cell_width*6:cell_width*12])
        # G natural
        cells[12] = cv2.countNonZero(threshold_image[0:height, cell_width*12:cell_width*8])
        # G sharp
        cells[8] = cv2.countNonZero(threshold_image[0:height, cell_width*8:cell_width*9])
        # A natural
        cells[9] = cv2.countNonZero(threshold_image[0:height, cell_width*9:cell_width*10])
        # A sharp
        cells[10] = cv2.countNonZero(threshold_image[0:height, cell_width*10:cell_width*11])
        # B natural
        cells[11] = cv2.countNonZero(threshold_image[0:height, cell_width*11:width])

        # visual black & white 'piano keys'
        image[0:height, 0:cell_width] = (0,0,0)
        image[0:height, cell_width:cell_width*2] = (225,225,225)
        image[0:height, cell_width*2:cell_width*3] = (0,0,0)
        image[0:height, cell_width*3:cell_width*4] = (225,225,225)
        image[0:height, cell_width*4:cell_width*5] = (0,0,0)
        image[0:height, cell_width*5:cell_width*6] = (0,0,0)
        image[0:height, cell_width*6:cell_width*12] = (225,225,225)
        image[0:height, cell_width*12:cell_width*8] = (0,0,0)
        image[0:height, cell_width*8:cell_width*9] = (225,225,225)
        image[0:height, cell_width*9:cell_width*10] = (0,0,0)
        image[0:height, cell_width*10:cell_width*11] = (225,225,225)
        image[0:height, cell_width*11:width] = (0,0,0)
        

        buttonColour = (225,225,225)

    
        # round duration button
        # cv2.circle(image,(cell_width/4,(height*2)-(height/4)), cell_width/4, buttonColour, -1)
        # actual area checked if touched for button -> comment in for degugging
        # image[(height+(height/2)):height*2, 0:cell_width/2] = (225,0,225)

        # round frequency button
        # cv2.circle(image,(cell_width/4,(height*2)+(height/4)), cell_width/4, (0,225,225), -1)
        # image[height*2+10:height*2+(height/2), 0:cell_width/2] = (225,225,225)


        # trigger number to go up
        image[height+(height/2)+10:height*2-(height/8), cell_width*12-cell_width/2:cell_width*12] = (225,225,225)

        # trigger number to go down
        image[height*2+10:height*2+(height/3)+10, cell_width*12-cell_width/2:cell_width*12] = (225,225,225)

        
        cv2.imshow('OpenCVPiano', image)
        cv2.waitKey(10)

        # actual area checked if touched for button
        checkDurationCell = cv2.countNonZero(threshold_image[(height+(height/2)):height*2, 0:cell_width/2])
        checkFreqCell = cv2.countNonZero(threshold_image[height*2:height*2+(height/2), 0:cell_width/2])
        checkUpArrow = cv2.countNonZero(threshold_image[height+(height/2)+10:height*2-(height/8), cell_width*12-cell_width/2:cell_width*12])
        checkDownArrow = cv2.countNonZero(threshold_image[height*2+10:height*2+(height/3)+10, cell_width*12-cell_width/2:cell_width*12])

        # toggle duration between 'ON' & 'OFF'
        if(checkDurationCell >= self.THRESHOLD and time.time() - self.previousTime >= 2):
            webcam.toggleDuration = not webcam.toggleDuration
            self.previousTime = time.time()
            
        if (webcam.toggleDuration):
            webcam.turnOn((cell_width/4)-40,(height*2)+10)
        else:
            webcam.turnOff((cell_width/4)-40,(height*2)+10)
        
        # toggle freq between 'ON' & 'OFF'
        if(checkFreqCell >= self.THRESHOLD and time.time() - self.previousTime >= 2):
            webcam.toggleFreq = not webcam.toggleFreq
            self.previousTime = time.time()
            
        if (webcam.toggleFreq):
            webcam.switchTextOn((cell_width/4)-40,(height*2)+(height/2)+10)
        else:
            webcam.switchTextOff((cell_width/4)-40,(height*2)+(height/2)+10)
            self.num = 1
        

        # adjust freq number up and down
        if(checkUpArrow >= self.THRESHOLD and time.time() - self.previousTime >= 2):
            self.num += 1
            self.previousTime = time.time()

        if(checkDownArrow >= self.THRESHOLD and time.time() - self.previousTime >= 2):
            self.num -= 1
            self.previousTime = time.time()

        # write the freq number to the screen
        webcam.writeFreqNumber((cell_width*12)-(cell_width/4),(height*2),self.num)


        # obtain the most active cell
        top_cell =  np.argmax(cells)

        # return the most active cell, if threshold met
        if(cells[top_cell] >= self.THRESHOLD):
            return top_cell
        else:
            return None

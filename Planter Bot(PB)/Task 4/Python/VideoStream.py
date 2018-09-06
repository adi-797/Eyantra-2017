'''
* Team Id : 931
* Author List : Abhaysheel Anand, Aditya Arora, Bhawana Chhaglani, Milap Sharma
* Filename: 
* Theme: Planter Bot (PB)
* Functions: blink_led, shed_blink, blend_transparent, file_handling, overlayCM
* Global Variables: Red, Green, Blue, Listof_colors, Listof_shapes, Colorlist, Colorlist_element, plantation 
'''

# import the necessary packages
from webcamvideostream import WebcamVideoStream
 
class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240))

# import the necessary packages
from webcamvideostream import WebcamVideoStream

class VideoStream:

##* Function Name: __init__
##* Input: -
##* Output: -
##* Logic: Initializes the stream 
##* Example Call: -

	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
		framerate=32):
		# check to see if the picamera module should be used
		if usePiCamera:
			# only import the picamera packages unless we are
			# explicity told to do so -- this helps remove the
			# requirement of `picamera[array]
			from pivideostream import PiVideoStream

			# initialize the picamera stream and allow the camera
			# sensor to warmup
			self.stream = PiVideoStream(resolution=resolution,
				framerate=framerate)

		# otherwise, we are using OpenCV so initialize the webcam
		# stream
		else:
			self.stream = WebcamVideoStream(src=src)

##* Function Name: start
##* Input: -
##* Output:  self.stream.start(), object for execution of the stream
##* Logic: Starts the stream
##* Example Call: vs=VideoStream(usePiCamera=args["picamera"] > 0).start() , here an object of Videostream class has been created, initialised and capturing of stream is started

	def start(self):
		# start the threaded video stream
		return self.stream.start()

##* Function Name: update
##* Input: -
##* Output: -
##* Logic: Updates the ongoing stream with every call
##* Example Call: vs.update()

	def update(self):
		# grab the next frame from the stream
		self.stream.update()
		
##* Function Name: read
##* Input: -
##* Output: self.stream.read(), captured frame
##* Logic: Returns the captured stream
##* Example Call: frame = vs.read(), reads the captured stream frame by frame 

	def read(self):
		# return the current frame
		return self.stream.read()

##* Function Name: stop
##* Input: -
##* Output: -
##* Logic: Stops the stream
##* Example Call: vs.stop(), stops the capturing of the stream

	def stop(self):
		# stop the thread and release any resources
		self.stream.stop()

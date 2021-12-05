from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import pyautogui
import webbrowser, os ,sys


currentname = "Not Recognized"
url = "http://raspberrypi:4000/"
chrome_path = '/usr/lib/chromium-browser/chromium-browser'
encodingsP = "encodings.pickle"


print("loading encodings and face detector")
data = pickle.loads(open(encodingsP, "rb").read())


vs = VideoStream(src=0,framerate=10).start()
time.sleep(2.0)

fps = FPS().start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
	
    boxes = face_recognition.face_locations(frame)
    
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    
    for encoding in encodings:
		
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown" 
		
        if True in matches:
			
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

			
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            
            name = max(counts, key=counts.get)
            webbrowser.get(chrome_path).open(url)
            # change y and x to where the chromium browser pops up at
                    # Use print(pyautogui.position()) to figure/test out the coordinate
            time.sleep(5.0)
            pyautogui.click(747, 1064)
            pyautogui.write('0000')
            pyautogui.press('enter')
            # update the list of names
            names.append(name)



            #If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(currentname)

             exit(0)


           

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)

    # display the image to our screen
    cv2.imshow("FR Running", frame)
    key = cv2.waitKey(1) & 0xFF

    
    if key == ord("e"):
        break

    # update the FPS counter
    fps.update()


fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cv2.destroyAllWindows()
vs.stop()

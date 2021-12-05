import cv2

name = 'Connor'
cam = cv2.VideoCapture(0)

cv2.namedWindow("Space to take pic", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Space to take pic", 600, 300)
img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:        
        print("Closing")
        break
    elif k%256 == 32:
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()

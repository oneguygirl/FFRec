import numpy as np
import cv2
import sqlite3
import os
from PIL import Image


Id=0
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0, 0, 255)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
im = cv2.imread('images/pariwesh.jpg', cv2.IMREAD_COLOR)

def insertOrUpdate(Name):
    conn = sqlite3.connect("Faces1.0.db")
    with conn:
        cur=conn.cursor()
        cur.execute("INSERT INTO People(Name) VALUES ('"+ Name +"');")
        max_id = cur.lastrowid
        Id= max_id
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd = "UPDATE people SET Name=' " + str(sname) + " ' WHERE ID=" + str(Id)
    else:
        cmd = "INSERT INTO people(ID,Name) Values(" + str(Id) + ",' " + str(sname) + " ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    return max_id

sname=raw_input('Enter your name:')
Id=insertOrUpdate(sname)
name =  "_".join(sname.lower().split(" "))
Facespath="Faces database/" + name
os.makedirs(Facespath)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#os.rename("/home/merishna/Documents/ubuntu/PycharmProjects/Facial recognition/FFRec/dataSet/" + name, "/home/merishna/Documents/ubuntu/PycharmProjects/Facial recognition/FFRec/Faces database/" + name)

faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
for(x,y,w,h) in faces:


    cv2.imwrite(Facespath+ "/face-" + name + "." + str(Id) + ".jpg", gray[y:y + h, x:x + w])
    cv2.rectangle(im, (x - 50, y - 50), (x + w + 50, y + h + 50), (225, 0, 0), 2)



# Trainer
# # Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Using prebuilt frontal face training model, for face detection
# detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");


# Create method to get the images and label data
def getImagesAndLabels(path):
    # Get all file path
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    # Initialize empty face sample
    faceSamples = []

    # Initialize empty id
    ids = []

    # Loop all the file path
    for imagePath in imagePaths:

        # Get the image and convert it to grayscale
        PIL_img = Image.open(imagePath).convert('L')

        # PIL image to numpy array
        img_numpy = np.array(PIL_img, 'uint8')

        # Get the image id
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # Get the face from the training images
        faces = detector.detectMultiScale(img_numpy)

        # Loop for each face, append to their respective ID
        for (x, y, w, h) in faces:
            # Add the image to face samples
            faceSamples.append(img_numpy[y:y + h, x:x + w])

            # Add the ID to IDs
            ids.append(id)

    # Pass the face array and IDs array
    return faceSamples, ids


# Get the faces and IDs
faces, ids = getImagesAndLabels(Facespath)

# Train the model using the faces and IDs
recognizer.train(faces, np.array(ids))

# Save the model into trainer.yml
recognizer.write('trainer/trainer.yml')



cv2.imshow('im', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
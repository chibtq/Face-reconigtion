import cv2
import numpy as np
import os
from PIL import Image
import mysql.connector

# insert vao database
mydb = mysql.connector.connect(host='localhost', port = '3306', user='root', password='Chihaha@1983', database='ai')
mycursor = mydb.cursor()
# khoi tao bo nhan dien khuon mat su dung thuât toán :BPH
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet/User'
def getImagesWithID(path):
    imagePaths = []
    #su dung module os để dueyẹt qua tat ca cac hinh anh trong thu muc
    #duyệt qua tất cả các file trong thưmục datáet, usee
    for root, directories, files in os.walk(path):
        # For each file in the current directory, check if it's an image file
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                # If it's an image file, add its full path to the list
                imagePaths.append(os.path.join(root, file))
                #them file hinh anh vao danh sach image.path

    faces = []
    IDs = []
    for imagePath in imagePaths:
        #chuyen dang dinh dang gray scale (bang phuong thuc vconverrt cua thu vien pillow) va chuyen thanh mot mang numpy
        faceImg = Image.open(imagePath).convert('L') 
        #sau do anh duoc chuyen thanh mot mang numpy bach cach su dung...
        faceNp = np.array(faceImg, 'uint8')

        
        print(os.path.split(imagePath)[0].split("\\")[-1].split("-")[0])
        #ID moi hinh anh duoc trich xuat tu ten thu mu
        ID = int(os.path.split(imagePath)[0].split("\\")[-1].split("-")[0])
        #tra ve danh sach ID va mang anh
        faces.append(faceNp)
        IDs.append(ID)
        #hien thi anh trong qua trinh huan luyen
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return IDs, faces

#goi ham get imagine with ID để lấy DS
#lay ID va mang anh tu thu mục datáet, user
Ids, faces = getImagesWithID(path)
#training

recognizer.train(faces, np.array(Ids)) #huan luyen voi mang anh va ID tuong ung
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
#luu mo hinh bo nhan dien khuon mat da huan luyen vao tep
recognizer.save('recognizer/trainingData.yml')

cv2.destroyAllWindows()

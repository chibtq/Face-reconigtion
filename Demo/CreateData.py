import cv2 #thư viện dnahf cho thị giácc máy tính thời gian thực
import numpy as np 
import os
import mysql.connector
#kết nối vào CSDL tên ai trên local host
# insert vao database
mydb = mysql.connector.connect(host = 'localhost', port = '3306' ,user='root', password='', database='AI')
mycursor = mydb.cursor()


# chèn hoặc cập nhâọp thông tin vào CSDL
def insertOrUpdate(Id, Name):
    # kiểm tra 1 bản ghi với ID cụ thể (MSV) tồn tại trong bảng people, cập nhật tên tương ứng
    sql = "SELECT * FROM People WHERE MSV= %s"
    val = (Id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isRecordExist = 0
    for row in result:
        isRecordExist = 1
    if (isRecordExist == 1):
        sql = "UPDATE People SET Name= %s WHERE Msv= %s"
        val = (Name, Id)
    else:
        sql = "INSERT INTO People(MSV, Name) VALUES(%s,%s)"
        val = (Id, Name)
    mycursor.execute(sql, val)
    mydb.commit()
def getId(MSV): #hàm lấy ID từ bảng people dựa trên MSV được cung cấp
    sql = "SELECT * FROM People WHERE MSV= %s"
    val = (MSV,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    for row in result:
        return row[0]
    return -1
#main
MSV = input('MSV:')
name = input('Name:')
insertOrUpdate(MSV, name)
id = getId(MSV)
# load thu vien
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
sampleNum = 0
while True:
    #doc 1 khung hinh tu luong video
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #chuyen anh sang thang do xam va su dung bo phan loai khuon mat de phat hien khuon mat trong anh
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #luu cac khuon mat duoc phat hien vao thu muc 
    for (x, y, w, h) in faces:
        sampleNum = sampleNum + 1
        if not os.path.exists('dataSet/User/'+str(id)+'-'+MSV):
            os.makedirs('dataSet/User/'+str(id)+'-'+MSV)
        cv2.imwrite("dataSet/User/" + str(id)+'-'+MSV + "/" + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        #ve hinh chu nhat
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = img[y:y + h, x:x + w]
    cv2.imshow('img', img)
    cv2.waitKey(1)
    if sampleNum > 100:
        break
cap.release()
cv2.destroyAllWindows()

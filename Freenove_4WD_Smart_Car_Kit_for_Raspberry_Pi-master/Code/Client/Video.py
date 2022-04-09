#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import io
import sys
import struct
from PIL import Image
from multiprocessing import Process
from Command import COMMAND as cmd

#added this
import pickle

class VideoStreaming:
    def __init__(self, car, car1_queue, car2_queue,car3_queue,car4_queue):
        self.face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self.video_Flag=True
        self.connect_Flag=False
        self.face_x=0
        self.face_y=0

        #added this
        self.carName=car
        self.tags = {0 : "Car 1", 1 : "Car 1", 2 : "Car 1", 3 : "Car 1",
                     4 : "Car 2", 5 : "Car 2", 6 : "Car 2", 7 : "Car 2",
                     8 : "Car 3", 9 : "Car 3", 10 : "Car 3", 11 : "Car 3",
                     12 : "Car 4", 13 : "Car 3", 14 : "Car 3", 15 : "Car 3"}
        if self.carName == "Car 1":
            self.my_queue = car1_queue
        elif self.carName == "Car 2":
            self.my_queue = car2_queue
        elif self.carName == "Car 3":
            self.my_queue = car3_queue
        elif self.carName == "Car 4":
            self.my_queue = car4_queue
        
    def StartTcpClient(self,IP):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #added this
        self.client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def StopTcpcClient(self):
        try:
            self.client_socket.shutdown(2)
            self.client_socket1.shutdown(2)
            self.client_socket.close()
            self.client_socket1.close()

            #added this
            self.client_socket2.shutdown(2)
            self.client_socket2.close()
        except:
            pass

    def IsValidImage4Bytes(self,buf): 
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):     
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:        
            try:  
                Image.open(io.BytesIO(buf)).verify() 
            except:  
                bValid = False
        return bValid

    def face_detect(self,img):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,1.3,5)
            if len(faces)>0 :
                for (x,y,w,h) in faces:
                    self.face_x=float(x+w/2.0)
                    self.face_y=float(y+h/2.0)
                    img= cv2.circle(img, (int(self.face_x),int(self.face_y)), int((w+h)/4), (0, 255, 0), 2)
            else:
                self.face_x=0
                self.face_y=0

        #added this
        if self.carName == 'Car 1':
            vid = 'video_1.jpg'
        elif self.carName == 'Car 2':
            vid = 'video_2.jpg'
        elif self.carName == 'Car 3':
            vid = 'video_3.jpg'
        elif self.carName == 'Car 4':
            vid = 'video_4.jpg'

        cv2.imwrite(vid,img)
        
    def streaming(self,ip, car1_queue, car2_queue,car3_queue,car4_queue, need_to_stop):
        stream_bytes = b' '
        try:
            self.client_socket.connect((ip, 8000))
            self.connection = self.client_socket.makefile('rb')
        except:
            #print "command port connect failed"
            pass

        #added this
        try:
            self.client_socket2.connect((ip, 6000))
        except:
            #print "command port connect failed"
            pass
        
        while True:
            #added this
            try:
                HEADERSIZE = 10
                full_msg = b''
                new_msg = True
                #print("Step 2")
                msg = self.client_socket2.recv(1024)
                msglen = int(msg[:HEADERSIZE])
                full_msg += msg
                while len(full_msg)-HEADERSIZE < msglen:
                    msg = self.client_socket2.recv(1024)
                    full_msg += msg

                dist_list = pickle.loads(full_msg[HEADERSIZE:])


                ######################ADDED#######################
                ######################ADDED#######################
                ######################ADDED#######################
                if self.carName not in self.my_queue:
                    self.my_queue.append(self.carName)
                    need_to_stop[0] = True
                    for dist in dist_list:
                        car_id = dist[0]
                        detected_car = self.tags[car_id]

                        if detected_car == "Car 1" and self.carName not in car1_queue:
                            car1_queue.append(self.carName)
                        elif detected_car == "Car 2" and self.carName not in car2_queue:
                            car2_queue.append(self.carName)
                        elif detected_car == "Car 3" and self.carName not in car3_queue:
                            car3_queue.append(self.carName)
                        elif detected_car == "Car 4" and self.carName not in car4_queue:
                            car4_queue.append(self.carName)

                        if car_id % 4 == 0:
                            direction = "driving towards me"
                        elif car_id % 4 == 1:
                            direction = "driving east of me"
                        elif car_id % 4 == 2:
                            direction = "driving in front of me"
                        elif car_id % 4 == 3:
                            direction = "driving west of me"

                        print(self.carName + ": detected " + detected_car + " at " + str(dist[1]) + "cm and " + direction)
                        print()
            except Exception as e:
                print("Error with streaming: ")
                print(e)
                break
            
            #try:
                #stream_bytes= self.connection.read(4) 
                #leng=struct.unpack('<L', stream_bytes[:4])
                #jpg=self.connection.read(leng[0])
                #if self.IsValidImage4Bytes(jpg):
                #            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                #            if self.video_Flag:
                #                self.face_detect(image)
                #                self.video_Flag=False
            #except Exception as e:
            #    print (e)
            #    break
                  
    def sendData(self,s):
        if self.connect_Flag:
            self.client_socket1.send(s.encode('utf-8'))

    def recvData(self):
        data=""
        try:
            data=self.client_socket1.recv(1024).decode('utf-8')
        except:
            pass
        return data

    def socket1_connect(self,ip):
        try:
            self.client_socket1.connect((ip, 5000))
            self.connect_Flag=True
            print ("Connecttion Successful !")
        except Exception as e:
            print ("Connect to server Faild!: Server IP is right? Server is opend?")
            self.connect_Flag=False

if __name__ == '__main__':
    pass


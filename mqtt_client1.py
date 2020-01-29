import cv2
import time
import paho.mqtt.client as mqtt
import perception_image2d_pb2
import PerceptionResult_pb2
import numpy as np

HOST = "39.106.157.212"#"39.106.157.212"
MQTT_PORT = 1883
ALIVE = 60
topic_sub1 = "/img/test"
topic_sub2 = "/img/preception_result"

class Mqtt_client1():
    def __init__(self):
        self.client = None
        self.img_str = None
        self.init_client()
    def __del__(self):
        print('delete mqtt_client1')

    def on_connect(self,client, userdata, flags, rc):
	    print("Connected with result code " + str(rc)+" client1")
	    client.subscribe(topic_sub1)

    def on_message(self,client, userdata, msg):
        pimg_2d = perception_image2d_pb2.PerceptionRawImage2D()
        if pimg_2d.ParseFromString(msg.payload):
            self.img_str = pimg_2d.data
        else:
            print("解析失败")

    def init_client(self):
        #声明客户端
        self.client = mqtt.Client()
        #连接
        self.client.connect(HOST, MQTT_PORT, ALIVE)
        #两个回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def get_cvFrame(self):
        np_arr = np.fromstring(self.img_str,np.uint8)
        cv_frame = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)
        return cv_frame

    def drawSth_OnJpgFrame(self,cv_frame,rect_list):
        #获取当前时间
        time_now = int(time.time())
        #转换成localtime
        time_local = time.localtime(time_now)
        #转换成新的时间格式(2016-05-09 18:59:20)
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        cv2.putText(cv_frame,dt,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        if rect_list!=None:
            cv2.rectangle(cv_frame, (rect_list[0], rect_list[1]), (rect_list[0]+rect_list[2], rect_list[1]+rect_list[3]),(255,255,0), 2)
        ret,jpeg = cv2.imencode('.jpg',cv_frame)
        return jpeg.tobytes()

class Mqtt_client2():
    def __init__(self):
        self.client = None
        self.rect_list = None
        self.init_client()

    def __del__(self):
        print('delete mqtt_client2')

    def on_connect(self,client, userdata, flags, rc):
	    print("Connected with result code " + str(rc)+" client2")
	    client.subscribe(topic_sub2)

    def on_message(self,client, userdata, msg):
        pr_msg = PerceptionResult_pb2.PerceptionResult()
        if pr_msg.ParseFromString(msg.payload):
            self.rect_list = [pr_msg.x,pr_msg.y,pr_msg.w,pr_msg.h]
            #print('client2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            
        else:
            print("解析失败")

    def init_client(self):
        #声明客户端
        self.client = mqtt.Client()
        #连接
        self.client.connect(HOST, MQTT_PORT, ALIVE)
        #两个回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()






























        

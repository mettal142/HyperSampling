import tensorflow as tf
import numpy as np
import copy as cp
import serial
import time
import matplotlib.pyplot as plt

Mode=0 #0:TrainData, 1:Test, 2:ReadData, 3:CombineData

MotionIndex=3

def HyperSampling(data,Lable):
    temp1=[]
    temp2=[]
    it= len(data)+2
    for i in range(0,it,2):
        data=np.insert(data,i+1,(np.array(data[i])+np.array(data[i+1]))/2,axis=0)

    for i in range(len(data)):
        temp1.extend(data[i])
    temp2.append(temp1)
    temp2.append(Lable)
    
    return temp2


def GenerateData(Mode,MotionIndex):

    ser = serial.Serial(
    port='COM10',
    baudrate=115200,
)

    FileName=''
    Lable = tf.one_hot([0,1,2,3,4,5,6,7,8,9,10],depth=11).eval(session=tf.Session())
    temp=[]
    save=[]
    data=[]
    IMU=[]
    InitializedData=[]
    Iterator=0
    StateChecker=0
    print("start")
    if Mode==0 or Mode==1:
        while True:
            if ser.readable():
                res = ser.readline()
            if Mode==0:
                FileName="Train"+str(MotionIndex)
                if ser.readable():
                    try:
                        IMU=list(map(float,res.decode()[:].split(',')[:]))
                    except:
                        ser.read_all()
                        continue
                    if StateChecker==0 and IMU[0]==1:
                        ser.read_all()
                        InitializedData=cp.copy(IMU[1:])
                        start=time.time()
                        StateChecker=1
                    elif StateChecker==1 and IMU[0]==1:
                        data.extend(cp.copy(np.array(IMU[1:])-InitializedData))
                    elif StateChecker==1 and IMU[0]==0:
                        if len(data)<=60:
                            data.clear()
                            StateChecker=0
                            continue
                        deltaTime=time.time()-start
                        save.append((np.array(data)))
                        hyperdata=np.array(HyperSampling(np.array(data).reshape(-1,3),[])[0]).reshape(-1,3)
                        hyperdata2=np.array(HyperSampling(hyperdata,[])[0]).reshape(-1,3)
                        print(np.array(data).reshape(-1,3))
                        print(hyperdata)
                        test1=[]
                        test2=[]
                        test3=[]
                        for i in range(len(np.array(data).reshape(-1,3))):
                            test1.append(np.array(data).reshape(-1,3)[i][0])
                        for i in range(len(hyperdata)):
                            test2.append(hyperdata[i][0])
                        for i in range(len(hyperdata2)):
                            test3.append(hyperdata2[i][0])
                        x=range(-180,180)
                        plt.figure(1)
                        plt.plot(test1,'or')
                        plt.figure(2)
                        plt.plot(test2,'og')
                        plt.figure(3)
                        plt.plot(test3,'ob')
                        plt.show()
                        data.clear()
                        print(Iterator)
                        if Iterator>=100:
                            np.save("./Data/"+FileName,save[1:],True)
                            #np.save("./Data/test1",save[1:],True)
                            break
                        Iterator+=1
                        StateChecker=0


    elif Mode==1:
        print("Read Data Mode")
        LoadData=np.load('./Data/600.npy',allow_pickle=True)
        for i in range(len(LoadData)):
            print(np.array(LoadData[i][1]))
        print(len(LoadData[0][0]))
        print(len(LoadData[0][1]))


    elif Mode==2:
        print("Combine Mode")
        savetemp=[]
        Motion1=np.load('./Data/300.npy',allow_pickle=True)
        Motion2=np.load('./Data/300_.npy',allow_pickle=True)
        #Motion3=np.load('./Data/Train3.npy',allow_pickle=True)
        #Motion3=np.load('CombinedMotionDataming45.npy',allow_pickle=True)
        savetemp.extend(Motion1) 
        savetemp.extend(Motion2) 
        #savetemp.extend(Motion3) 
        np.random.shuffle(savetemp)
        np.save("./Data/"+str(len(savetemp)),savetemp,True)
        print(len(savetemp),"Saved")

GenerateData(Mode,MotionIndex)

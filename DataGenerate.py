import tensorflow as tf
import numpy as np
import copy as cp
import random as rd
import serial
import time
import matplotlib.pyplot as plt

Mode=0 #0:TrainData, 1:ReadData, 2:CombineData
MotionIndex=1
hyper=1200
choice=20

#def HyperSampling(data,Lable,time):
#    temp1=[]
#    temp2=[]
#    it= len(data)+2
#    dt=time/len(data)
#    print(it,dt)
#    for i in range(0,it,2):
#        data=np.insert(data,i+1,(np.array(data[i])+np.array(data[i+1]))/2,axis=0)
#    for i in range(len(data)):
#        temp1.extend(data[i])
#    temp2.append(temp1)
#    temp2.append(Lable)
    
#    return temp2

def HyperSampling(data,time,sample):
    temp1=[]
    temp2=[]
    it= len(data)*2
    dt=time/len(data)
    for i in range(0,it-4,2):
        inclination1=(np.array(data[i+1])-np.array(data[i]))/dt
        inclination2=(np.array(data[i+2])-np.array(data[i+1]))/dt
        doubleinc=(inclination2-inclination1)/(2*dt)
        data=np.insert(data,i+1,(inclination1+doubleinc*(dt/2))*(dt/2)+data[i],axis=0)
        if len(data)==sample:
            break

    #for i in range(len(data)):
    #    temp1.extend(data[i])
    #temp2.append(temp1)
    #temp2.append(Lable)
    print(len(data))
    return data

def Choice(data,sample):
    temp1=[]#data
    temp2=[]#lable
    
    print(len(data))
    idx=rd.sample(range(len(data)),sample)
    idx.sort()
    
    for i in idx:
        temp1.append(data[i])
    
    return temp1

def ShowGraph(data,choicedata,hyperdata,fac):
    
    test0=[]
    test1=[]
    test2=[]

    for i in range(len(np.array(data).reshape(-1,3))):
        test0.append(np.array(data).reshape(-1,3)[i][fac])
    for i in range(len(np.array(choicedata).reshape(-1,3))):
        test1.append(np.array(choicedata).reshape(-1,3)[i][fac])
    for i in range(len(np.array(hyperdata).reshape(-1,3))):
        test2.append(np.array(hyperdata).reshape(-1,3)[i][fac])

    plt.figure(1)           
    plt.title('Data')
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.plot(test0,'.r') 
    plt.figure(2)           
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title('ChoiceData')
    plt.plot(test1,'.g') 
    plt.figure(3)       
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title('HyperData')
    plt.plot(test2,'.b') 

    plt.show()
                        
def HyperConvert(save,hyper,deltaTime):
    for data in save[:-1]:


        return hyperdata

        #ShowGraph(data,choicedata,hyperdata)

def ChoiceConvert(save,choice):
    for data in save[:-1]:
        
        choicedata=np.array(Choice(np.array(data).reshape(-1,3),save[-1],choice)[0]).reshape(-1,3)

        return choicedata

        #ShowGraph(data,choicedata,hyperdata)
                        
def GenerateData(Mode,MotionIndex):

    ser = serial.Serial(
    port='COM10',
    baudrate=115200,
)

    FileName=''
    Lable = tf.one_hot([0,1,2,3,4,5,6,7,8,9,10],depth=11).eval(session=tf.Session())
    hypertemp=[]
    save=[]
    data=[]
    hypersave=[]
    choicesave=[]
    IMU=[]
    InitializedData=[]
    Iterator=0
    StateChecker=0
    print("start")
    if Mode==0:
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
                        if len(data)<=choice*3:
                            data.clear()
                            StateChecker=0
                            continue
                        deltaTime=time.time()-start
                        hypertemp=np.array(data).reshape(-1,3)
                        hyperdata=[]
                        temp=[]
                        while 1:
                            hypertemp=np.array(HyperSampling(np.array(hypertemp),deltaTime,hyper))
                            if len(hypertemp)>=hyper:
                                hyperdata=[]
                                for i in range(len(hypertemp)):
                                    temp.extend(hypertemp[i])
                                hyperdata.append(temp)
                                hyperdata.append(Lable[MotionIndex])
                                break
                
                        choicetemp=np.array(Choice(np.array(data).reshape(-1,3),choice))
                        choicedata=[]
                        temp=[]
                        for i in range(len(choicetemp)):
                            temp.extend(choicetemp[i])
                        choicedata.append(temp)
                        choicedata.append(Lable[MotionIndex])
                        #save.append((np.array(data)))
                        ShowGraph(data,choicedata[0],hyperdata[0],0)
                        hypersave.append(np.array(hyperdata))
                        choicesave.append(np.array(choicedata))
                        data.clear()
                        #print(Iterator)
                        if Iterator>=3:
                            #np.save("./Data/"+FileName,save[1:],True)
                            np.save("./Data/ChoiceSample/"+FileName,choicesave,True)
                            np.save("./Data/HyperSample/"+FileName,hypersave,True)
                            #np.save("./Data/test1",save[1:],True)
                            break
                        print(Iterator)
                        Iterator+=1
                        StateChecker=0


    elif Mode==1:
        print("Read Data Mode")
        LoadChoice=np.load('./Data/ChoiceSample/Train1.npy',allow_pickle=True)
        LoadHyper=np.load('./Data/HyperSample/Train1.npy',allow_pickle=True)
        print(LoadChoice[0][1])
        print(LoadHyper[0][1])
        ShowGraph([],LoadChoice[0][0],LoadHyper[0][0],0)
  


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
#l=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
#l2=list(map(float,l))
#print(np.array(l2).reshape(-1,3))
#print(np.array(l2).reshape(-1,3))
#l3=HyperSampling_(np.array(l2).reshape(-1,3),[],256)[0]
#print(np.array(l3).reshape(-1,3))
#l4=HyperSampling_(np.array(l3).reshape(-1,3),[],256)[0]
#print(np.array(l4).reshape(-1,3))

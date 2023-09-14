#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import socket
#Import threads
import logging
import threading
import time

TIME_TO_GROW = 60*15
MAX_TREE_SIZE = 3*TIME_TO_GROW
Tree_Size = 0

GPIO.setmode(GPIO.BOARD)
SNS1_TRIGGER = 16
SNS2_TRIGGER = 18
SNS3_TRIGGER = 22
SNS4_TRIGGER = 24
SNS1_ECHO = 32
SNS2_ECHO = 36
SNS3_ECHO = 38
SNS4_ECHO = 40

LED_PIN = 11

THRESHOLD = 100

GPIO.setup(SNS1_TRIGGER, GPIO.OUT)
GPIO.setup(SNS1_TRIGGER, GPIO.OUT)
GPIO.setup(SNS2_TRIGGER, GPIO.OUT)
GPIO.setup(SNS3_TRIGGER, GPIO.OUT)
GPIO.setup(SNS4_TRIGGER, GPIO.OUT)
GPIO.setup(SNS1_ECHO, GPIO.IN)
GPIO.setup(SNS2_ECHO, GPIO.IN)
GPIO.setup(SNS3_ECHO, GPIO.IN)
GPIO.setup(SNS4_ECHO, GPIO.IN)

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(SNS1_TRIGGER, GPIO.LOW)
GPIO.output(SNS2_TRIGGER, GPIO.LOW)
GPIO.output(SNS3_TRIGGER, GPIO.LOW)
GPIO.output(SNS4_TRIGGER, GPIO.LOW)

print("waiting for sensor to settle")

time.sleep(0.5)

delay_value = 0.025

GPIO.output(LED_PIN, GPIO.LOW)

def server_thread(name):
        #Create UDP Socket

    listensocket = socket.socket() #Creates an instance of socket
    Port = 8000 #Port to host server on
    maxConnections = 10
    hostname = socket.gethostname() #IP address of local machine
    IP=socket.gethostbyname(hostname)

    listensocket.bind(('',Port))

    #Starts server
    listensocket.listen(maxConnections)
    print("Server started at " + IP + " on port " + str(Port))

    
    
    while True:
        #Accepts the incomming connection
        (clientsocket, address) = listensocket.accept()
        print("New connection made!")
        
        message = clientsocket.recv(1024).decode() #Gets the incomming message
        print(message)
        
        value = str(Tree_Size)
        print(value)
        clientsocket.sendall(value.encode("utf-8"))
        #if not message == "":
            #GPIO.output(7,True)
            #time.sleep(5)
            #GPIO.output(7,False)

        

x = threading.Thread(target=server_thread, args=(1,))

logging.info("Main    : before running thread")

x.start()

while True:
    GPIO.output(SNS1_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(SNS1_TRIGGER, GPIO.LOW)

    while GPIO.input(SNS1_ECHO)==0:
        pulse1_start_time = time.time()
    while GPIO.input(SNS1_ECHO)==1:
        pulse1_end_time = time.time()

    pulse1_duration = pulse1_end_time - pulse1_start_time
    distance1 = round(pulse1_duration * 17150, 2)
    print("Sensor 1 Distance",distance1,"cm")
    time.sleep(delay_value)
    
    GPIO.output(SNS2_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(SNS2_TRIGGER, GPIO.LOW)

    while GPIO.input(SNS2_ECHO)==0:
        pulse2_start_time = time.time()
    while GPIO.input(SNS2_ECHO)==1:
        pulse2_end_time = time.time()

    pulse2_duration = pulse2_end_time - pulse2_start_time
    distance2 = round(pulse2_duration * 17150, 2)
    print("Sensor 2 Distance",distance2,"cm")
    time.sleep(delay_value)
    
    GPIO.output(SNS3_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(SNS3_TRIGGER, GPIO.LOW)

    while GPIO.input(SNS3_ECHO)==0:
        pulse3_start_time = time.time()
    while GPIO.input(SNS3_ECHO)==1:
        pulse3_end_time = time.time()

    pulse3_duration = pulse3_end_time - pulse3_start_time
    distance3 = round(pulse3_duration * 17150, 2)
    print("Sensor 3 Distance",distance3,"cm")
    time.sleep(delay_value)
    
    GPIO.output(SNS4_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(SNS4_TRIGGER, GPIO.LOW)

    while GPIO.input(SNS4_ECHO)==0:
        pulse4_start_time = time.time()
    while GPIO.input(SNS4_ECHO)==1:
        pulse4_end_time = time.time()

    pulse4_duration = pulse4_end_time - pulse4_start_time
    distance4 = round(pulse4_duration * 17150, 2)
    print("Sensor 4 Distance",distance4,"cm")
    time.sleep(delay_value)
    
    grow1 = 0
    grow2 = 0
    
    #Quais os sensores que estao juntos?
    if distance1 <= THRESHOLD:
        grow1 = 1
        GPIO.output(LED_PIN, GPIO.HIGH)
    if distance2 <= THRESHOLD:
        grow1 = 1
        GPIO.output(LED_PIN, GPIO.HIGH)
    if distance3 <= THRESHOLD:
        grow2 = 1
        GPIO.output(LED_PIN, GPIO.HIGH)
    if distance4 <= THRESHOLD:
        grow2 = 1
        GPIO.output(LED_PIN, GPIO.HIGH)
    
    #Arvore decresce a um terco da velocidade
    if grow1 or grow2:
        Tree_Size = min(MAX_TREE_SIZE,Tree_Size + grow1*3 + grow2*3)
    else:
        Tree_Size = max(0, Tree_Size - 1)
        GPIO.output(LED_PIN, GPIO.LOW)
        
    print("Tree size:",Tree_Size)
    
    time.sleep(2)

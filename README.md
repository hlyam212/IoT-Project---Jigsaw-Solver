# IoT-Project - Jigsaw-Solver

## Introduction

It's an IoT project that can help people figure out how to solve a physical puzzle problem. Using the recognition and the robotic arm, the user can use a mobile phone to upload a picture of the current piece. Then, the device can pick it up and put it in the right place.

## Hardware Components

1. Raspberry Pi 3 *1
2. MG996R Servo Motor *6
3. 6-DOF Robotic Arm *1
4. PCA9685 (I2C Interface) *1
5. Switching Power Supply *1 (with wires)
6. Dupont Lines *22 (at least)

## Preparation

### Raspberry Pi 4 

You need to install some packages to start this project.

`
pip3 install flask
`

`
pip3 install opencv-python
`

`
pip3 install adafruit-circuitpython-servokit
`

`
pip3 install flask
`

### MG996R Servo Motor

Before you put them onto the robotic arm, you can first test the way they operate by the code. It will first ask you enter a number between 0-180, and you will see the motor operating.
-Test single moter(Test Hardware/TestSingleMotor.py)
-Test 6 motor with PGA9685(Test Hardware/servo_6_test.py)
-Adjust motor on the robot arm operration by commond(Test Hardware/ServoAdjust.py)

### Switched Power Supply

It can provide the power that the motors need by transfer the AC to DC.
Because it connect to the socket directly so <font color="red"> please be careful</font>

![image](https://github.com/hlyam212/IoT-Project---Jigsaw-Solver/blob/master/PowerSupply.jpg?raw=true)

### 6-DOF Robotic Arm

If you got the arm and the servo motors seperately, you can puzzle them up by [this link](https://www.taiwansensor.com.tw/6軸機械手臂組裝教學/).(Remember to double check the direction or you may need to reinstall them if you put them in the wrong directtion.

### Feature Matching - OpenCV

In this project, I'm tring to match a puzzle piece in to a complte picture. I use [OpenCV](https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html) to do feature matching, enable to detect the position of the puzzle piece.

## Connect the components - How it looks like

### STEP 1 : Connect the PCA9685 and your raspberry pi 3

You can check out the picture and you can put the 'vcc' to pinout 1(3v3 power), too.
<font color="red"> Please be careful! Don't insert the wrong pinout or it will easily burn out. </font>

![image](https://www.aranacorp.com/wp-content/uploads/16-channel-pwm-controller-pca9685-raspberry-pi_bb-1080x675.png)


### STEP 2 : Connect the servo motors and your PCA9685

There are sixteen positions that can provide the control of the servo motors. So you can insert the dupont lines one by one from the 0 position.

### STEP 4 : Connect the PCA9685 and the power supply

<font color="red"> Please be careful when you plug into the socket and don't touch the power supply when it's powered. </font>
![image](https://github.com/hlyam212/IoT-Project---Jigsaw-Solver/blob/master/PCA_PowerSupply.jpg?raw=true)

## Test the robotic arm

After connecting all the hardware components. You can now test your robotic arm by insert the init angles.
-Test all 6 motors with PGA9685 to check if it's functional(Test Hardware/servo_6_test.py)
-Adjust motor on the robot arm operration by commond(Test Hardware/ServoAdjust.py)
   *Assign a moter and move to a certen angle : position of servo/target angle(ex: 2/180)
   *Exit : s

Remember to keep your eyes on the devices when it is running. Because when the servo motors are installed onto the robotic arm, there will be some angle restrict to the motors so please be careful.

Remeber to record those angles that each motor can't reach. By this way, you can set up the minimum angles in your main program.

## Flask Web Application

To open web site deploy on raspberry pi, your phone and raspberry pi needs to connect to the same wifi/internet

1.In the folder "pages", is a simple web application for uploading pictures of the puzzle piece with your moblie device. You need to [deploy your web on raspberry pi](https://peppe8o.com/beginners-guide-to-install-a-flask-python-web-server-on-raspberry-pi/).
2.After that, run commend "flask run --host=0:0:0:0:5000" to initiate your web. 
3.Then run "ip address" to find raspberry pi's ip.
4.Once they're all done, open "http://*ipaddress*:5000/" on your phone.

### Robot arm and settings

![image](https://github.com/hlyam212/IoT-Project---Jigsaw-Solver/blob/master/ArmSetting1.jpg?raw=true)
![image](https://github.com/hlyam212/IoT-Project---Jigsaw-Solver/blob/master/ArmSetting2.jpg?raw=true)

### Now, you can try to follow the instruction of the web, and try to put the puzzle piece on the black area, then upload the picture."

After you run the program, go to 127.0.0.1:5000 to see the user interface. If the console came up with some numbers or you see the green box, you can click the let's go button to see the arm moving.


### [My Video](https://youtu.be/dkQ-8wHkPck)

## Reference Link

1.https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/

2.https://ithelp.ithome.com.tw/articles/10258223

3.https://stackoverflow.com/questions/73886870/what-is-the-simplest-way-to-detect-the-angle-of-rotation-between-two-images-of-t

4.https://peppe8o.com/beginners-guide-to-install-a-flask-python-web-server-on-raspberry-pi/

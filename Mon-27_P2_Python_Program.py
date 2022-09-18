## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.
import random
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

#Locations of each bin slot
Large_Red = [-0.4083,0.1718,0.20]
Small_Red = [-0.6096, 0.2443, 0.376]
Large_Blue = [0.0, 0.4064, 0.290]
Small_Blue = [0.0, 0.640, 0.400]
Large_Green = [0.0, -0.4064, 0.290]
Small_Green = [0.0, -0.640, 0.400]

def Autoclave_Bin_Location(x): #Number inputted is assigned to a color and size
    dropoff = [0,0,0]
    if x == 1:
        dropoff = Small_Red
    elif x == 2:
        dropoff = Small_Green
    elif x == 3:
        dropoff = Small_Blue
    elif x == 4:
        dropoff = Large_Red
    elif x == 5:
        dropoff = Large_Green
    elif x == 6:
        dropoff = Large_Blue
    
    return dropoff #returns List of coordinates

def Pickup_Container(): # Moves to the pickup location if the left is greater then 1 and right equals 0
    A = False
    while A == False:
        if arm.emg_left() > 0 and arm.emg_right() == 0:
            time.sleep(2)
            arm.rotate_shoulder(50)
            arm.rotate_elbow(5)
            time.sleep(2)
            Close_Gripper()
            break

def Close_Gripper(): #Closes gripper if the right muscle senser is greater then 0 and left equals 0
    A = False
    while A == False:
        if arm.emg_right() > 0 and arm.emg_left() == 0:
            arm.control_gripper(35)
            time.sleep(2)
            break

def Release_Gripper(): #Open gripper if the right muscle sensor is at 0.0 and left greater then 0
    time.sleep(4)
    A = True
    while A == True:
        if arm.emg_right() == 0 and arm.emg_left() > 0:
            arm.control_gripper(-30)
            time.sleep(2)
            A= False

def Move_to_Location(coords): #Moves to assigned location from "Autoclave_Bin_Location()" function if both muscle
    A = False                 #sensers return 0.0
    while A == False:
        if arm.emg_left() == 0.0 and arm.emg_right() == 0:
            arm.move_arm(coords[0],coords[1],coords[2])
            break
def Open_Autoclave(x): #Opens autoclave if both sensors are at 1.0, unless the Container ID is 1,2, or 3
    A = False
    while A == False:
        if arm.emg_right() == 1.0 and arm.emg_left() == 1.0:
            if x == 4:
                arm.open_red_autoclave(True)
                break
            elif x == 5:
                arm.open_green_autoclave(True)
                break
            elif x == 6:
                arm.open_blue_autoclave(True)
                break
            else:
                break
            
    

def Close_Autoclave(x):#Closes autoclave if both sensors are at 0.0, unless the Container ID is 1,2, or 3
    A = False
    while A == False:
        if arm.emg_right() == 0.0 and arm.emg_left() == 0.0:
            if x == 4:
                arm.open_red_autoclave(False)
                time.sleep(2)
                break
            elif x == 5:
                arm.open_green_autoclave(False)
                time.sleep(2)
                break
            elif x == 6:
                arm.open_blue_autoclave(False)
                time.sleep(2)
                break
            else:
                break
            
    

def Move_End_Effector(Container_ID):#Goes through the process of getting the container to the sterlization unit
    block = Random_Container(Container_ID)
    if block == 9:
        return Container_ID
    Container_ID = Remove_Num(block,Container_ID)
    arm.spawn_cage(block)
    print("The Container's ID is: ", block)
    Pickup_Container()
    arm.move_arm(0.4064, 0.0, 0.4826)
    time.sleep(2)
    if block  == 4 or block  == 5 or block == 6:
        Open_Autoclave(block)
    time.sleep(1)
    Move_to_Location(Autoclave_Bin_Location(block))
    time.sleep(2)
    Release_Gripper()
    time.sleep(2)
    if block == 4 or block  == 5 or block == 6:
        Close_Autoclave(block)
    arm.home()
    return Container_ID

def Random_Container(IDs):
    #Code below randomizes the block or if all blocks have been used then starts to leave code
    Pick = False
    if IDs[0] == 0 and IDs[1] ==0 and IDs[2] ==0 and IDs[3] ==0 and IDs[4] ==0 and IDs[5] ==0:
        Pick == True
        choice = 9
        print("All containers sterilized")
    else:
       while Pick == False:
        R = random.randint(0,5)
        if IDs[R] > 0:
            choice = IDs[R]
            break 
    
    
    return choice

def Remove_Num(num,Id_List):
    #Code below sets the used blocks to an id of 0 so the code knows they have been used
    if num == 1:
        Id_List[0] = 0
    elif num == 2:
        Id_List[1] = 0
    elif num == 3:
        Id_List[2] = 0
    elif num == 4:
        Id_List[3] = 0
    elif num == 5:
        Id_List[4] = 0
    elif num == 6:
        Id_List[5] = 0
    return Id_List
   

def main():#The code below is the main that starts everything
    leave = False
    Container_ID = [1,2,3,4,5,6]
    #Below is the while loop that runs everything
    while leave == False:
        arm.home()
        time.sleep(2)
        Container_ID = Move_End_Effector(Container_ID)
        if Container_ID[0] == 0 and Container_ID[1] ==0 and Container_ID[2] ==0 and Container_ID[3] ==0 and Container_ID[4] ==0 and Container_ID[5] ==0:
            leave = True
            print("All containers are sanitized")
            break
        print("If you would like to continue, flex the left arm, otherwise, stay idle.")
        time.sleep(10)
        if arm.emg_left() > 0: #Repeats the simulation if the left sensor is at all flexed (>0.0)
            print("Continuing simulation!")
            leave = False
        else: #Ends the similation
            leave = True
            print("Ending simulation...")

main()

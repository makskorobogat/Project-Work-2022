from sqlite3 import connect
import dearpygui.dearpygui as dpg
import time
import threading
from randomNumberGenerator import *
from graphsValues import *
from configparser import ConfigParser
from Component import Datatypes as dt
from Device import Device
from Component import Component as cp
import pandas as pd
import numpy as np
from time import sleep
from sklearn.model_selection import train_test_split
from sklearn.svm import NuSVR

global readedValuesfromPLC
global i

#we need global variables that are intialized to zero like this
Rev_global = 0
valve_global =0
time_global_v = 0
time_global_r = 0

#Flags to generate random data
generate_valve=1
generate_rev = 1


# Start Part of Max
data_set = pd.read_csv("DataNeww.txt",
					delimiter = ';',low_memory=False, encoding='latin-1')

data_set.columns = ['A1', 'Q1', 'Volumenstrom', "RotationMotorA", 'Regelventil', 'Motor_A_Elektrische_Leistung',
					"Fuellstand_oberer_Tank", "Fuellstand_unterer_Tank"]

# store dataframe into csv file
data_set.to_csv('Data for Learning.csv',
			index = None)

columns = ['A1', 'Q1', 'Volumenstrom', "RotationMotorA", 'Regelventil', 'Motor_A_Elektrische_Leistung',
					"Fuellstand_oberer_Tank", "Fuellstand_unterer_Tank"]

data_set = data_set.loc[:, columns]
fullstand2 = ['Volumenstrom']
featuresdrop = ['Volumenstrom', 'Motor_A_Elektrische_Leistung', "Fuellstand_oberer_Tank", "Fuellstand_unterer_Tank"]

#featuresdrop = ['A1', "B1", 'Q1', 'Volumenstrom', "RotationMotorA", "RotationMotorB", 'Regelventil', 'Motor_A_Elektrische_Leistung',
#					'Motor_B_Elektrische_Leistung', "Fuellstand_oberer_Tank", "Fuellstand_unterer_Tank"]
global features
global labels
features = data_set.drop(featuresdrop, axis=1)
labels = data_set[fullstand2]

Ydata = data_set[fullstand2]
Ydata2 = (list(map(float, Ydata.values)))

#Line X
rangeY = len(Ydata.values)
rangeY = rangeY * 0.01

Xdata = list (np.arange(0, rangeY, 0.01))

i = 0

#This function will convert data to csv format. After that it will make pd array, but now only csv
def save_csv():
    time.sleep(1)
    print("Saving Data in CSV...")
    #f = open('CSV_FILE.csv', 'a')
    str_data = [str(readedValuesfromPLC[0]), str(readedValuesfromPLC[1], readedValuesfromPLC[2], readedValuesfromPLC[3])]
    str_data_value = ','.join(str_data)
    print (str_data)
    print (str_data_value)
    with open('CSV_FILE.csv', 'a') as f:
        f.write(str_data_value)
        f.write("\n")

# End of Max Part

#Plc to access Data
Plc = Device("Pumpenversuchsstand", "192.168.1.1", 0, 2)


#Components to read out:  cp(Device, Name of Component, Datatype, OffsetByte, OffsetBit, NumberOfDatablock)
EngineA_Power               = cp(Plc, "Engine A Power",                 dt.Real,    228,    0,  33)
EngineB_Power               = cp(Plc, "Engine B Power",                 dt.Real,    424,    0,  33)
MotorA_Drehzahl             = cp(Plc, "MotorA_Drehzahl",                dt.Real,    48,    0,  15)
MotorB_Drehzahl             = cp(Plc, "MotorB_Drehzahl",                dt.Real,    88,    0,  15)
FullstandOber             = cp(Plc, "FullstandOber",                dt.Real,    508,    0,  33)
FullstandUnter             = cp(Plc, "FullstandUnter",                dt.Real,    512,    0,  33)


#Data to write
MotorA_Drehzahl_Soll        = cp(Plc, "MotorA_Drehzahl_Soll",           dt.Real,    0,    0,  13)
EngineB_Power_Act           = cp(Plc, "EngineB_Power_Act",              dt.Real,    4,    0,  13)
Ventil_Stellwert_Soll       = cp(Plc, "Ventil_Power_Act",               dt.Real,    8,    0,  13)   

#Ventil and Volumenstrom
Ventil                      = cp(Plc, "Ventil",                         dt.Real,    168,    0,  15)
Volumenstrom                = cp(Plc, "Volumenstrom",                   dt.Real,    244,    0,  27)

#Drucksensoren
A1                          = cp(Plc, "A1",                             dt.Real,    516,    0,  33)
B1                          = cp(Plc, "B1",                             dt.Real,    524,    0,  33)
R1                          = cp(Plc, "R1",                             dt.Real,    536,    0,  33)

#To start the Readout process, use Value.ReadDB() (Only reading out once)
#To start the automaticprocess, do the following steps:
#   1)  Component.SetAutomatic(True)
#   2)  Device.StartAutomatic(True)
#   3)  To access to the data of the Value: Component.Value (Stored Value of the component, automaticly updated)
#
#   See an exercise below

#PART OF Tomás Araújo


def RandomNumberGenerator():
    RandomNumberRev()
    RandomNumberValve()
    dpg.delete_item("RandomButton")

def RandomNumberRev():
    global Rev_global,time_global_r, r_send, time_limit_rise_r, time_limit_on_r
    global rev
    if(generate_rev==1):
        rev, revTimeOn, revTimeRise = revRandomNumberGenerator()
        #print("Rev: rev: {};; revTimeOn: {};; revTimeRise: {}".format(rev, revTimeOn, revTimeRise))
        r_send = (rev - Rev_global) / (revTimeRise)
        time_limit_rise_r = time_global_r + revTimeRise
        time_limit_on_r = time_limit_rise_r + revTimeOn
        ThreadSendRev = threading.Thread(target=send_rev)
        ThreadSendRev.start()

def RandomNumberValve():
    global valve, valve_global, time_global_v, v_send, time_limit_rise_v, time_limit_on_v
    if(generate_valve==1):
        valve,valveTimeOn,valveTimeRise = valveNumberGenerator()
        #print ("Valve: valve: {};; ValveTimeOn: {};; ValveTimeRise: {}".format(valve,valveTimeOn,valveTimeRise))
        v_send = (valve - valve_global) / (valveTimeRise)
        time_limit_rise_v = time_global_v + valveTimeRise
        time_limit_on_v = time_limit_rise_v + valveTimeOn
        ThreadSendValve = threading.Thread(target=send_valve)
        ThreadSendValve.start()

def send_rev():
    global generate_valve, generate_rev
    global Rev_global,valve_global,time_global_v,time_global_r,rev,r_send,time_limit_rise_r,time_limit_on_r
    #Now check the conditions
    #print(time_limit_on_r)
    #print("--------------------")
    while(time_global_r<time_limit_on_r):
        generate_rev = 0
        if(time_global_r<time_limit_rise_r):
            Rev_global=Rev_global+r_send
            #Write Data into PLC (Part of Ingmar)
            MotorA_Drehzahl_Soll.WriteDB(Rev_global)
            #print(Rev_global)
            #print("---------")
            #print(time_global_r)
            sleep(1)
            time_global_r=time_global_r+1
        elif(time_global_r>=time_limit_rise_r and time_global_r<time_limit_on_r):
            Rev_global=rev
            #Write Data into PLC (Part of Ingmar)
            MotorA_Drehzahl_Soll.WriteDB(Rev_global)
            sleep(1)
            #print(time_global_r)
            #print("-----------")
            time_global_r=time_global_r+1
            #print(Rev_global)
    #print("While is ending here")
    generate_rev=1
    RandomNumberRev()

def send_valve():
    global valve,v_send,time_limit_rise_v,time_limit_on_v,Rev_global,valve_global,time_global_v,time_global_r
    while(time_global_v<time_limit_on_v):
        generate_valve = 0
        if(time_global_v<time_limit_rise_v):
            valve_global=valve_global+v_send
            #Write Data into PLC (Part of Ingmar)
            Ventil_Stellwert_Soll.WriteDB(valve_global)
            sleep(1)
            time_global_v=time_global_v+1
        elif(time_global_v>=time_limit_rise_v and time_global_v<time_limit_on_v):
            valve_global=valve
            #Write Data into PLC (Part of Ingmar)
            Ventil_Stellwert_Soll.WriteDB(valve_global)
            sleep(1)
            time_global_v=time_global_v+1
    generate_valve=1
    RandomNumberValve()

def getvalues():
    x1,y1 = valuesRev()
    x2,y2 = valuesValve()
    return x1,y1,x2,y2

def graphs_main():

    AddToList()

    # creating data
    config = ConfigParser()
    config.read('config.ini')
    yminRev= int(config['rev']['minRev'])
    ymaxRev= int(config['rev']['maxRev'])
    sindatax1 = []
    sindatay1 = []
    sindatax2 = []
    sindatay2 = []
    #sindatax1,sindatay1=valuesRev()
    sindatax1,sindatay1,sindatax2,sindatay2= getvalues()
    with dpg.window(label="Generated Rotation Value", pos=(600, 10)) as graphs1:
        # create plot
        with dpg.plot(height=200, width=430):
            # optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axis1")
            dpg.add_plot_axis(dpg.mvYAxis, label="Rotation, 1/s", tag="y_axis1")
            dpg.set_axis_limits("y_axis1",yminRev,ymaxRev)
            dpg.set_axis_limits("x_axis1", 0, sindatax1[len(sindatax1)-1]+20)
            #print (sindatax1)
            #print(sindatay1)


            # series belong to a y axis
            dpg.add_line_series(sindatax1, sindatay1, parent="y_axis1", tag="rev_plot1")


    yminValve= int(config['valve']['minValve'])
    ymaxValve= int(config['valve']['maxValve'])
    #sindatax2,sindatay2= valuesValve()
    with dpg.window(label="Generated Valve Value", pos=(1065, 10)) as graphs2:
        # create plot
        with dpg.plot(height=200, width=430):
            #optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axis2")
            dpg.add_plot_axis(dpg.mvYAxis, label="Percent, %", tag="y_axis2")
            dpg.set_axis_limits("y_axis2",yminValve,ymaxValve)
            dpg.set_axis_limits("x_axis2", 0, sindatax2[len(sindatax2)-1]+20)

            # series belong to a y axis
            dpg.add_line_series(sindatax2, sindatay2, parent="y_axis2", tag="valve_plot2")

# End of Tomás Araújo's part

    dpg.delete_item("Graphs")
    dpg.bind_item_theme(graphs1, container_theme2)
    dpg.bind_item_theme(graphs2, container_theme2)


#Part from Ingmar and Maksim about graphs

stop = False

def Onactualisationgrafics():
    print("Thread actualisationgrafics started")

    while stop == False:
        
        readedValuesfromPLC = [A1.Value, B1.Value, R1.Value, Volumenstrom.Value,
                               Ventil.Value, EngineA_Power.Value, EngineB_Power.Value,
                               MotorA_Drehzahl.Value,
                               MotorA_Drehzahl.Value, FullstandOber.Value, FullstandUnter.Value]

        sindatax1, sindatay1, sindatax2, sindatay2 = getvalues()

        # Set part for REV
        dpg.set_value('rev_plot1', [sindatax1, sindatay1])
        # Set part for Valve
        dpg.set_value('valve_plot2', [sindatax2, sindatay2])
        dpg.set_axis_limits("x_axis1", 0, sindatax1[len(sindatax1) - 1] + 20)
        dpg.set_axis_limits("x_axis2", 0, sindatax2[len(sindatax2) - 1] + 20)

        # Predictions
        global array1
        newArray = (A1.Value, R1.Value, MotorA_Drehzahl.Value,
                           Ventil.Value)
        array1 = np.asarray(newArray)
        array1 = array1.reshape(1, -1)
        predictions = svr_regressor.predict(array1)

        MainDifference = float (predictions) - float (readedValuesfromPLC[3])

        global i
        XdataGraphs = list(np.arange(0, i, 0.5))

        Vol_Data.append(float(readedValuesfromPLC[3]))
        Vol_Data2.append(float(predictions))
        A1_DataG.append(float(readedValuesfromPLC[0]))
        B1_DataG.append(float(readedValuesfromPLC[1]))
        R1_DataG.append(float(readedValuesfromPLC[2]))
        VEN_DataG.append(float(readedValuesfromPLC[4]))
        MotA_DataG.append(float(readedValuesfromPLC[5]))
        N_DataA.append(float(readedValuesfromPLC[7]))
        Differenz.append(float(abs(MainDifference)))

        # Set part for Vol
        dpg.set_value('rev_plotV', [XdataGraphs, Vol_Data])
        dpg.set_axis_limits("x_axisV", 0, i + 5)
        dpg.set_value('rev_plotV2', [XdataGraphs, Vol_Data2])

        # Set part for A1,B1,R1
        dpg.set_value('rev_plotA1', [XdataGraphs, A1_DataG])
        dpg.set_value('rev_plotB1', [XdataGraphs, B1_DataG])
        dpg.set_value('rev_plotR1', [XdataGraphs, R1_DataG])
        dpg.set_axis_limits("y_axisA1", 0, readedValuesfromPLC[0] + 2)
        dpg.set_axis_limits("x_axisA1", 0, i + 5)

        # Set part for Ventil
        dpg.set_value('rev_plotREG', [XdataGraphs, VEN_DataG])
        dpg.set_axis_limits("y_axisREG", 0, 110)
        dpg.set_axis_limits("x_axisREG", 0, i + 5)

        # Set part for Motor A, Motor B
        dpg.set_value('rev_plotMotorA', [XdataGraphs, MotA_DataG])
        #dpg.set_value('rev_plotMotorB', [XdataGraphs, MotB_DataG])
        dpg.set_axis_limits("y_axisMotorA", 0, 2)
        dpg.set_axis_limits("x_axisMotorA", 0, i + 5)

        # Set part for Speed A, Speed B
        dpg.set_value('rev_plotRotA', [XdataGraphs, N_DataA])
        #dpg.set_value('rev_plotRotB', [XdataGraphs, N_DataB])
        dpg.set_axis_limits("y_axisRot", 0, 3000)
        dpg.set_axis_limits("x_axisRot", 0, i + 5)

        # Set part for Difference
        dpg.set_value('rev_plotDiff', [XdataGraphs, Differenz])
        dpg.set_axis_limits("x_axisDiff", 0, i + 5)
        #print("Grafic updated")

        i += 0.5
        sleep(0.5)

    print("Thread actualisationgrafics endet")

ThreadActualisation = threading.Thread(target=Onactualisationgrafics)


def update_graphs():
    StartAutomatic()
    ThreadActualisation.start()


def update_graphs_stop():
    StopAutomatic()
    global stop
    stop = True
    print("Thread is over")

#End of Part of Ingmar and Maksim about graphs

#Start of Ingmars Part

def ConnectPLC():
    Plc.Connect()

def PlcInfo():
    print(Plc.name)
    print("Stored error: " + Plc.error)
    print(Plc.GetDeviceInformation())
    print("Connection: " + str(Plc.CheckConnection()))
    print(Plc.S7Device)

def ComponentReadData():
    if(A1 != None):
        global readedValuesfromPLC
        readedValuesfromPLC = [A1.Value, B1.Value, R1.Value, Volumenstrom.Value,
                               Ventil.Value, EngineA_Power.Value, EngineB_Power.Value, MotorA_Drehzahl.Value, MotorB_Drehzahl.Value]

    else:
        print("Please create component first!")

def ComponentWriteData():
    if(A1 != None):
        #Test.SetBit()
        #Test2.ResetBit()

        rev,revTimeOn,revTimeRise, valve,valveTimeOn,valveTimeRise = RandomNumberGenerator()

        MotorA_Drehzahl_Soll.WriteDB(rev)
    else:
        print("Please create component first!")
        
def CheckConnection():
    print(Plc.CheckConnection())
    print(type(Plc.CheckConnection()))

def StartAutomatic():
    print("Button Start Automatic pressed")

    #Exercise for automatic function
    #1) Set Value to Automatic
    EngineA_Power.SetAutomatic(True)
    #2) Start automatic update
    Plc.StartAutomatic()
    #3) Access to internal stored value
    #print(EngineA_Power.Value)
    
def StopAutomatic():
    print("Button Start Automatic pressed")
    Plc.StopAutomatic()

def AddToList():
    A1.SetAutomatic(True)
    B1.SetAutomatic(True)
    R1.SetAutomatic(True)
    Volumenstrom.SetAutomatic(True)
    Ventil.SetAutomatic(True)
    EngineA_Power.SetAutomatic(True)
    EngineB_Power.SetAutomatic(True)
    MotorA_Drehzahl.SetAutomatic(True)
    MotorB_Drehzahl.SetAutomatic(True)


def ShowValues():
    Data = (A1.Value, B1.Value, R1.Value, Volumenstrom.Value,
            Ventil.Value, EngineA_Power.Value, EngineB_Power.Value, MotorA_Drehzahl.Value, MotorA_Drehzahl.Value)
    print(Data)

def Reset():
    Plc.CommunicationBusy = False

#End of Ingmars Part


#This part makes GUI Interface and all Buttons
dpg.create_context()

#Fonts
with dpg.font_registry():
    # first argument is the path to the .ttf or .otf file - to the font
    default_font = dpg.add_font("ARIAL.TTF", 19)

with dpg.window(label="Graphs", width=240, height=200, pos=(350,10), tag="wind1") as wind1:
    dpg.bind_font(default_font)
    #deleteFiles()
    dpg.add_button(label="1.Generate Random Values", callback=RandomNumberGenerator, pos=(15, 40), tag = "RandomButton")
    dpg.add_button(label="2.Show generated Graphs", callback=graphs_main, pos=(23, 70), tag='Graphs')
    dpg.add_button(label="3.Update all Graphs", callback=update_graphs, pos=(45, 100))
    dpg.add_button(label="4.Stop updating", callback=update_graphs_stop, pos=(60, 130))

with dpg.window(label="Device and Component", width=330, height=200, pos=(10,10)) as wind2:
    deleteFiles()
    dpg.add_button(label="Device info", callback=PlcInfo, pos=(20, 70))
    dpg.add_button(label="Connect to PLC", callback=ConnectPLC, pos=(20, 40))
    dpg.add_button(label="Read PLC Data", callback=ComponentReadData, pos=(170, 40))
    dpg.add_button(label="Write to PLC", callback=ComponentWriteData, pos=(170, 70))
    dpg.add_button(label="Save in CSV", callback=save_csv, pos=(20, 100))
    dpg.add_button(label="Show values", callback=ShowValues, pos=(170, 100))
    dpg.add_button(label="Start Automatic", callback=StartAutomatic, pos=(20, 130))
    dpg.add_button(label="Stop Automatic", callback=StopAutomatic, pos=(170, 130))
    dpg.add_button(label="Reset PLC", callback=Reset, pos=(20, 160))
    dpg.add_button(label="CheckConnection", callback=CheckConnection, pos=(170, 160))

with dpg.theme() as container_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (85, 85, 93))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7)
        dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (186, 34, 34))

with dpg.theme() as container_theme2:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7)
        dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (186, 34, 34))

#dpg.show_style_editor()
dpg.bind_item_theme(wind1, container_theme)
dpg.bind_item_theme(wind2, container_theme)

dpg.create_viewport(title='GUI Interface', width=1280, height=720, clear_color= (10, 10, 104, 255))

ConnectPLC()

readedValuesfromPLC = [A1.Value, B1.Value, R1.Value, Volumenstrom.Value,
                           Ventil.Value, EngineA_Power.Value, EngineB_Power.Value,
                           MotorA_Drehzahl.Value,
                           MotorB_Drehzahl.Value]

XdataGraphs = list(np.arange(0, i, 0.5))

# creating Volumenstrom graphs
Ydata = data_set[fullstand2]
with dpg.window(label="Volumenstrom", pos=(10, 265)) as graphs3:
    # create plot
    with dpg.plot(height=210, width=565):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisV")
        dpg.add_plot_axis(dpg.mvYAxis, label="Volume, m^3/h", tag="y_axisV")
        dpg.set_axis_limits("y_axisV",0,25)
        dpg.set_axis_limits("x_axisV", 0, i+5)

        global Vol_Data
        Vol_Data = [0, readedValuesfromPLC[3]]
        Vol_Data2 = [0, readedValuesfromPLC[3]]

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, Vol_Data, label="Real Flow", parent="y_axisV", tag="rev_plotV")
        dpg.add_line_series(XdataGraphs, Vol_Data2, label="Predicted Flow", parent="y_axisV", tag="rev_plotV2")


with dpg.window(label="Sensors pressure", pos=(600, 530)) as graphs4:
    # create plot
    with dpg.plot(height=220, width=430):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisA1")
        dpg.add_plot_axis(dpg.mvYAxis, label="Pressure, bar", tag="y_axisA1")
        dpg.set_axis_limits("y_axisA1", 0, readedValuesfromPLC[1] + 2)
        dpg.set_axis_limits("x_axisA1", 0, i + 5)

        global A1_DataG
        global B1_DataG
        global R1_DataG
        A1_DataG = [0, readedValuesfromPLC[0]]
        B1_DataG = [0, readedValuesfromPLC[1]]
        R1_DataG = [0, readedValuesfromPLC[2]]

        #print(XdataGraphs)

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, A1_DataG, label="A1 sensor pressure", parent="y_axisA1", tag="rev_plotA1")
        dpg.add_line_series(XdataGraphs, B1_DataG, label="B1 sensor pressure", parent="y_axisA1", tag="rev_plotB1")
        dpg.add_line_series(XdataGraphs, R1_DataG, label="R1 sensor pressure", parent="y_axisA1", tag="rev_plotR1")
        # dpg.add_line_series(Xdata, V1_Dataset2, label="V1 sensor pressure", parent="y_axisA1", tag="rev_plotV1")

# creating Regelventil graphs
with dpg.window(label="Control valve", pos=(1065, 265)) as graphs5:
    # create plot
    with dpg.plot(height=220, width=430):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisREG")
        dpg.add_plot_axis(dpg.mvYAxis, label="Percent, %", tag="y_axisREG")
        dpg.set_axis_limits("y_axisREG", 0, 110)
        dpg.set_axis_limits("x_axisREG", 0, i + 5)

        global VEN_DataG
        VEN_DataG = [0, readedValuesfromPLC[4]]
        # VENGraphs = (list(map(float, VEN_DataG)))

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, VEN_DataG, parent="y_axisREG", tag="rev_plotREG")

# creating Motor A and Motor B Electrical power
with dpg.window(label="Electrical power of engines", pos=(1065, 530)) as graphs6:
    # create plot
    with dpg.plot(height=220, width=430):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisMotorA")
        dpg.add_plot_axis(dpg.mvYAxis, label="Power, kW", tag="y_axisMotorA")
        dpg.set_axis_limits("y_axisMotorA", 0, 2)
        dpg.set_axis_limits("x_axisMotorA", 0, i + 5)

        global MotA_DataG
        #global MotB_DataG
        MotA_DataG = [0, readedValuesfromPLC[5]]
        #MotB_DataG = [0, readedValuesfromPLC[6]]

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, MotA_DataG, parent="y_axisMotorA", tag="rev_plotMotorA")
        #dpg.add_line_series(XdataGraphs, MotB_DataG, label="Motor B", parent="y_axisMotorA", tag="rev_plotMotorB")

# creating Drehzahl graphs
with dpg.window(label="Rotational speed", pos=(600, 265)) as graphs7:
    # create plot
    with dpg.plot(height=220, width=430):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisRot")
        dpg.add_plot_axis(dpg.mvYAxis, label="Rotation, 1/s", tag="y_axisRot")
        dpg.set_axis_limits("y_axisRot", 0, 3000)
        dpg.set_axis_limits("x_axisRot", 0, i + 5)

        global N_DataA
        #global N_DataB
        N_DataA = [0, readedValuesfromPLC[7]]
        #N_DataB = [0, readedValuesfromPLC[8]]

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, N_DataA, parent="y_axisRot", tag="rev_plotRotA")
        #dpg.add_line_series(XdataGraphs, N_DataB, label="Motor B", parent="y_axisRot", tag="rev_plotRotB")

# creating Difference graphs
with dpg.window(label="Absolute Error between Real and Predicted Flow ", pos=(10, 530)) as graphs8:
    # create plot
    with dpg.plot(height=220, width=565):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time, sec", tag="x_axisDiff")
        dpg.add_plot_axis(dpg.mvYAxis, label="Difference, m^3/h", tag="y_axisDiff")
        dpg.set_axis_limits("y_axisDiff", 0, 15)
        dpg.set_axis_limits("x_axisDiff", 0, i + 5)

        global Differenz
        Differenz = [0, readedValuesfromPLC[4]]

        # series belong to a y axis
        dpg.add_line_series(XdataGraphs, Differenz, parent="y_axisDiff", tag="rev_plotDiff")
# Split our data
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2, random_state=0)

global rf
global svr_regressor
svr_regressor = NuSVR(cache_size=1000).fit(train_features.values, train_labels.values.ravel())

dpg.bind_item_theme(graphs3, container_theme2)
dpg.bind_item_theme(graphs4, container_theme2)
dpg.bind_item_theme(graphs5, container_theme2)
dpg.bind_item_theme(graphs6, container_theme2)
dpg.bind_item_theme(graphs7, container_theme2)
dpg.bind_item_theme(graphs8, container_theme2)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

"""Copyright 2021, Dave Renzo (www.daverenzo.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time
import json


baud = 31250

ports = serial.tools.list_ports.comports()
dropdownList =[]
presetList = []
comPortDictionary={}
ser = serial.Serial()
ser.baudrate = baud

for port in ports:
    #print(port.device + ": "+ port.description)
    dropdownList.append(port.description)
    comPortDictionary[port.description] = port.device

with open('presets.json') as f:
  PresetData = json.load(f)

for preset in PresetData["presets"]:
    presetList.append(preset["preset name"])


def openComPort():
    messagebox.showinfo(message = "Hold down Switch 1 and click OK to put unit into programming mode")
    connectButton["state"] = "disable"
    print ("opening port: "+ comPortDictionary[comPortChoice.get()] )
    ser.port = comPortDictionary[comPortChoice.get()]
    ser.timeout = None
    ser.open()  
    time.sleep(2)
    print("Flushing input buffer")
    ser.flushInput()
    print("Flushing output buffer")
    ser.flushOutput()
    ser.write(b'a')
    s = ser.read(3)
    if (s == b'Ack'):
        print('Ack Recieved, requesting current setup')
        print("Flushing input buffer")
        ser.flushInput()
        print("Flushing output buffer")
        ser.flushOutput()
        ser.write(b'b')
        s = ser.read(18)
        print('Data Recieved:')
        for i in s:
            print(i)
        sw1CcNumChoice.set(str(s[0]))
        sw2CcNumChoice.set(str(s[1]))
        sw3CcNumChoice.set(str(s[2]))
        sw4CcNumChoice.set(str(s[3]))
        sw5CcNumChoice.set(str(s[4]))
        sw6CcNumChoice.set(str(s[5]))

        sw1CcValChoice.set(str(s[6]))
        sw2CcValChoice.set(str(s[7]))
        sw3CcValChoice.set(str(s[8]))
        sw4CcValChoice.set(str(s[9]))
        sw5CcValChoice.set(str(s[10]))
        sw6CcValChoice.set(str(s[11]))

        sw1ChannelChoice.set(str(s[12]))
        sw2ChannelChoice.set(str(s[13]))
        sw3ChannelChoice.set(str(s[14]))
        sw4ChannelChoice.set(str(s[15]))
        sw5ChannelChoice.set(str(s[16]))
        sw6ChannelChoice.set(str(s[17]))
        
        statusLabelText.set("Connected")
    else:
        print("Comunincation error")
        ser.close()

def cleanup():
    print("Closing APP")
    ser.close()
    root.destroy()

def sendSetup():
    txPacket = []
    if (ser.is_open):
        print("Flushing input buffer")
        ser.flushInput()
        print("Flushing output buffer")
        ser.flushOutput()
        ser.write(b'c')
        s = ser.read(3)
        if (s == b'Ack'):
            txPacket.append(int(sw1CcNumChoice.get()))
            txPacket.append(int(sw2CcNumChoice.get()))
            txPacket.append(int(sw3CcNumChoice.get()))
            txPacket.append(int(sw4CcNumChoice.get()))
            txPacket.append(int(sw5CcNumChoice.get()))
            txPacket.append(int(sw6CcNumChoice.get()))

            txPacket.append(int(sw1CcValChoice.get()))
            txPacket.append(int(sw2CcValChoice.get()))
            txPacket.append(int(sw3CcValChoice.get()))
            txPacket.append(int(sw4CcValChoice.get()))
            txPacket.append(int(sw5CcValChoice.get()))
            txPacket.append(int(sw6CcValChoice.get()))

            txPacket.append(int(sw1ChannelChoice.get()))
            txPacket.append(int(sw2ChannelChoice.get()))
            txPacket.append(int(sw3ChannelChoice.get()))
            txPacket.append(int(sw4ChannelChoice.get()))
            txPacket.append(int(sw5ChannelChoice.get()))
            txPacket.append(int(sw6ChannelChoice.get()))

            ser.write(txPacket)
            s = ser.read(3)
            if (s == b'POO'):
                print("Transfer success")
            else:
                print("Fubar")

def loadPreset():
    ### LOAD The preset data from the json file
    ### extract names to a list and sort alphabetically
    with open('presets.json') as f:
        presets = json.load(f)

    presetNames=[]
    for preset in presets["presets"]:
         presetNames.append(preset["preset name"])

    presetNames = sorted(presetNames)

    ### Setup data for use in Listbox
    choiceVar = tk.StringVar(value=presetNames)

    ### Setup window with listbox
    loadPresetWindow = tk.Toplevel()
    loadPresetWindow.grab_set()

    ### create a frame for listbox and scrollbar
    lbFrame = tk.Frame(loadPresetWindow)
    lbFrame.grid(column = 0, row = 0,columnspan =2)

    scrollBar = tk.Scrollbar(lbFrame)
    scrollBar.grid(column =1 , row =0, sticky =(tk.N, tk.S))

    presetListBox = tk.Listbox(lbFrame, height =5, listvariable = choiceVar )
    presetListBox.grid(column =0 , row =0, sticky = (tk.E, tk.W))
    # Attaching Listbox to Scrollbar 
    # Since we need to have a vertical  
    # scroll we use yscrollcommand 
    presetListBox.config(yscrollcommand = scrollBar.set )
    presetListBox.select_set(0)
    # setting scrollbar command parameter  
    # to listbox.yview method its yview because 
    # we need to have a vertical view 
    scrollBar.config(command = presetListBox.yview) 

    loadButton =  tk.Button(loadPresetWindow, text='Load Preset', command = lambda: loadPresetCB(loadPresetWindow,presetListBox.get(presetListBox.curselection())))
    loadButton.grid(row =1, column =0, padx = 10, pady = 5)

    cancelButton =  tk.Button(loadPresetWindow, text='Cancel', command = loadPresetWindow.destroy)
    cancelButton.grid(row =1, column =1, padx = 10, pady = 5)
    loadPresetWindow.mainloop()

def loadPresetCB(widowHandle, presetName):
    with open('presets.json') as f:
        presets = json.load(f)

    print(presetName)

    for data in presets["presets"]:
        if data["preset name"] == presetName:
            #print('\t'+str(data["SW1_CC_NUM"]))
            
            sw1CcNumChoice.set(str(data["SW1_CC_NUM"]))
            sw2CcNumChoice.set(str(data["SW2_CC_NUM"]))
            sw3CcNumChoice.set(str(data["SW3_CC_NUM"]))
            sw4CcNumChoice.set(str(data["SW4_CC_NUM"]))
            sw5CcNumChoice.set(str(data["SW5_CC_NUM"]))
            sw6CcNumChoice.set(str(data["SW6_CC_NUM"]))

            sw1CcValChoice.set(str(data["SW1_CC_VAL"]))
            sw2CcValChoice.set(str(data["SW2_CC_VAL"]))
            sw3CcValChoice.set(str(data["SW3_CC_VAL"]))
            sw4CcValChoice.set(str(data["SW4_CC_VAL"]))
            sw5CcValChoice.set(str(data["SW5_CC_VAL"]))
            sw6CcValChoice.set(str(data["SW6_CC_VAL"]))

            sw1ChannelChoice.set(str(data["SW1_MIDI_CHANNEL"]))
            sw2ChannelChoice.set(str(data["SW2_MIDI_CHANNEL"]))
            sw3ChannelChoice.set(str(data["SW3_MIDI_CHANNEL"]))
            sw4ChannelChoice.set(str(data["SW4_MIDI_CHANNEL"]))
            sw5ChannelChoice.set(str(data["SW5_MIDI_CHANNEL"]))
            sw6ChannelChoice.set(str(data["SW6_MIDI_CHANNEL"]))
    widowHandle.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    root.title('Helix Footswitch Midi Editor')
    root.geometry('800x250')
    root.resizable(False, False)
    root.grid_columnconfigure((0), weight=1)
    root.protocol('WM_DELETE_WINDOW', cleanup)

    comPortChoice = tk.StringVar()
    comPortChoice.set(dropdownList[0])

    presetChoice = tk.StringVar()
    presetChoice.set(presetList[0])

    #channelNums = initMidiChannelList()
    #ccNums = initMidiCClist()

    statusLabelText = tk.StringVar()
    statusLabelText.set("Not Connected")

    sw1ChannelChoice = tk.StringVar()
    sw2ChannelChoice = tk.StringVar()
    sw3ChannelChoice = tk.StringVar()
    sw4ChannelChoice = tk.StringVar()
    sw5ChannelChoice = tk.StringVar()
    sw6ChannelChoice = tk.StringVar()

    sw1CcNumChoice = tk.StringVar()
    sw2CcNumChoice = tk.StringVar()
    sw3CcNumChoice = tk.StringVar()
    sw4CcNumChoice = tk.StringVar()
    sw5CcNumChoice = tk.StringVar()
    sw6CcNumChoice = tk.StringVar()

    sw1CcValChoice = tk.StringVar()
    sw2CcValChoice = tk.StringVar()
    sw3CcValChoice = tk.StringVar()
    sw4CcValChoice = tk.StringVar()
    sw5CcValChoice = tk.StringVar()
    sw6CcValChoice = tk.StringVar()

    

    ################FRAMES#################################
    controlFrame = tk.Frame(root)#bg = 'red'
    controlFrame.grid(column = 0, row =0, pady=2, padx =45, sticky = (tk.E, tk.W))
    controlFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    switchFrame = tk.Frame(root,bg = 'dark green')
    switchFrame.grid(column = 0, row =1)

    sw1Frame = tk.LabelFrame(switchFrame, text="Switch 1")
    sw1Frame.grid(column = 0, row =0)

    sw2Frame = tk.LabelFrame(switchFrame, text="Switch 2")
    sw2Frame.grid(column = 1, row =0)

    sw3Frame = tk.LabelFrame(switchFrame, text="Switch 3")
    sw3Frame.grid(column = 2, row =0)

    sw4Frame = tk.LabelFrame(switchFrame, text="Switch 4")
    sw4Frame.grid(column = 0, row =1)

    sw5Frame = tk.LabelFrame(switchFrame, text="Switch 5")
    sw5Frame.grid(column = 1, row =1)

    sw6Frame = tk.LabelFrame(switchFrame, text="Switch 6")
    sw6Frame.grid(column = 2, row = 1)

    presetFrame = tk.Frame(root)
    presetFrame.grid(column = 0, row =2,padx = 45, pady=10,sticky = (tk.E, tk.W))
    presetFrame.grid_columnconfigure((0, 1), weight=1)


    #####################Control FRAME#############################
    statusLabel = tk.Label(controlFrame,textvariable = statusLabelText, width = 20,bg = 'red')
    statusLabel.grid(column = 0, row =0, padx =2, sticky = (tk.E, tk.W))

    comDropdown = tk.OptionMenu(controlFrame, comPortChoice, *dropdownList)
    comDropdown.grid(column = 1, row =0, padx =2, sticky = (tk.E, tk.W))
    comDropdown.config(width = 30)

    connectButton = tk.Button(controlFrame, text='Connect',command = openComPort)
    connectButton.grid(column = 2, row =0, padx =2, sticky = (tk.E, tk.W))

    uploadButton = tk.Button(controlFrame, text='upload settings',command = sendSetup)
    uploadButton.grid(column = 3, row =0, padx =2, sticky = (tk.E, tk.W))

    presetLoadButton = tk.Button(presetFrame, text='Load Preset', command = loadPreset)
    presetLoadButton.grid(column = 0, row =0, padx =2, sticky = (tk.E, tk.W))

    presetSaveButton = tk.Button(presetFrame, text='Save Preset', command = loadPreset)
    presetSaveButton.grid(column = 1, row =0, padx =2, sticky = (tk.E, tk.W))

    #presetDropdown = tk.OptionMenu(controlFrame, presetChoice, *presetList)
    #presetDropdown.grid(column = 0, row =1, padx =10, pady =10)
    #presetDropdown.config(width = 30)

    #####################SwitchFrame###########################################

    ###############SW 1####################################################
    sw1ChannelLabel = tk.Label(sw1Frame, text='Midi Channel')
    sw1ChannelLabel.grid(column = 0, row =0)
    sw1ChannelSpinBox = tk.Spinbox(sw1Frame, from_=1, to=16, state = 'readonly', textvariable = sw1ChannelChoice )
    sw1ChannelSpinBox.grid(column = 1, row =0)
    

    sw1CcNumLabel = tk.Label(sw1Frame, text='Midi CC Number')
    sw1CcNumLabel.grid(column = 0, row =1)
    sw1CcNumSpinBox = tk.Spinbox(sw1Frame, from_=1, to=127, state = 'readonly', textvariable = sw1CcNumChoice)
    sw1CcNumSpinBox.grid(column = 1, row =1)

    sw1CcValLabel = tk.Label(sw1Frame, text='Midi CC Value')
    sw1CcValLabel.grid(column = 0, row =2)
    sw1CcValpinBox = tk.Spinbox(sw1Frame, from_=1, to=127, state = 'readonly', textvariable = sw1CcValChoice  )
    sw1CcValpinBox.grid(column = 1, row =2)

    ###############SW 2####################################################
    sw2ChannelLabel = tk.Label(sw2Frame, text='Midi Channel')
    sw2ChannelLabel.grid(column = 0, row =0)
    sw2ChannelSpinBox = tk.Spinbox(sw2Frame, from_=1, to=16, state = 'readonly', textvariable = sw2ChannelChoice )
    sw2ChannelSpinBox.grid(column = 1, row =0)

    sw2CcNumLabel = tk.Label(sw2Frame, text='Midi CC Number')
    sw2CcNumLabel.grid(column = 0, row =1)
    sw2CcNumSpinBox = tk.Spinbox(sw2Frame, from_=1, to=127, state = 'readonly', textvariable = sw2CcNumChoice )
    sw2CcNumSpinBox.grid(column = 1, row =1)

    sw2CcValLabel = tk.Label(sw2Frame, text='Midi CC Value')
    sw2CcValLabel.grid(column = 0, row =2)
    sw2CcValpinBox = tk.Spinbox(sw2Frame, from_=1, to=127, state = 'readonly', textvariable = sw2CcValChoice  )
    sw2CcValpinBox.grid(column = 1, row =2)

    ###############SW 3####################################################
    sw3ChannelLabel = tk.Label(sw3Frame, text='Midi Channel')
    sw3ChannelLabel.grid(column = 0, row =0)
    sw3ChannelSpinBox = tk.Spinbox(sw3Frame, from_=1, to=16, state = 'readonly', textvariable = sw3ChannelChoice )
    sw3ChannelSpinBox.grid(column = 1, row =0)

    sw3CcNumLabel = tk.Label(sw3Frame, text='Midi CC Number')
    sw3CcNumLabel.grid(column = 0, row =1)
    sw3CcNumSpinBox = tk.Spinbox(sw3Frame, from_=1, to=127, state = 'readonly', textvariable = sw3CcNumChoice )
    sw3CcNumSpinBox.grid(column = 1, row =1)

    sw3CcValLabel = tk.Label(sw3Frame, text='Midi CC Value')
    sw3CcValLabel.grid(column = 0, row =2)
    sw3CcValpinBox = tk.Spinbox(sw3Frame, from_=1, to=127, state = 'readonly', textvariable = sw3CcValChoice )
    sw3CcValpinBox.grid(column = 1, row =2)

    ###############SW 4####################################################
    sw4ChannelLabel = tk.Label(sw4Frame, text='Midi Channel')
    sw4ChannelLabel.grid(column = 0, row =0)
    sw4ChannelSpinBox = tk.Spinbox(sw4Frame, from_=1, to=16, state = 'readonly', textvariable = sw4ChannelChoice )
    sw4ChannelSpinBox.grid(column = 1, row =0)

    sw4CcNumLabel = tk.Label(sw4Frame, text='Midi CC Number')
    sw4CcNumLabel.grid(column = 0, row =1)
    sw4CcNumSpinBox = tk.Spinbox(sw4Frame, from_=1, to=127, state = 'readonly', textvariable = sw4CcNumChoice )
    sw4CcNumSpinBox.grid(column = 1, row =1)

    sw4CcValLabel = tk.Label(sw4Frame, text='Midi CC Value')
    sw4CcValLabel.grid(column = 0, row =2)
    sw4CcValpinBox = tk.Spinbox(sw4Frame, from_=1, to=127, state = 'readonly', textvariable = sw4CcValChoice )
    sw4CcValpinBox.grid(column = 1, row =2)

    ###############SW 5####################################################
    sw5ChannelLabel = tk.Label(sw5Frame, text='Midi Channel')
    sw5ChannelLabel.grid(column = 0, row =0)
    sw5ChannelSpinBox = tk.Spinbox(sw5Frame, from_=1, to=16, state = 'readonly', textvariable = sw5ChannelChoice )
    sw5ChannelSpinBox.grid(column = 1, row =0)

    sw5CcNumLabel = tk.Label(sw5Frame, text='Midi CC Number')
    sw5CcNumLabel.grid(column = 0, row =1)
    sw5CcNumSpinBox = tk.Spinbox(sw5Frame, from_=1, to=127, state = 'readonly', textvariable = sw5CcNumChoice )
    sw5CcNumSpinBox.grid(column = 1, row =1)

    sw5CcValLabel = tk.Label(sw5Frame, text='Midi CC Value')
    sw5CcValLabel.grid(column = 0, row =2)
    sw5CcValpinBox = tk.Spinbox(sw5Frame, from_=1, to=127, state = 'readonly', textvariable = sw5CcValChoice )
    sw5CcValpinBox.grid(column = 1, row =2)

    ###############SW 6####################################################
    sw6ChannelLabel = tk.Label(sw6Frame, text='Midi Channel')
    sw6ChannelLabel.grid(column = 0, row =0)
    sw6ChannelSpinBox = tk.Spinbox(sw6Frame, from_=1, to=16, state = 'readonly', textvariable = sw6ChannelChoice )
    sw6ChannelSpinBox.grid(column = 1, row =0)

    sw6CcNumLabel = tk.Label(sw6Frame, text='Midi CC Number')
    sw6CcNumLabel.grid(column = 0, row =1)
    sw6CcNumSpinBox = tk.Spinbox(sw6Frame, from_=1, to=127, state = 'readonly', textvariable = sw6CcNumChoice )
    sw6CcNumSpinBox.grid(column = 1, row =1)

    sw6CcValLabel = tk.Label(sw6Frame, text='Midi CC Value')
    sw6CcValLabel.grid(column = 0, row =2)
    sw6CcValpinBox = tk.Spinbox(sw6Frame, from_=1, to=127, state = 'readonly', textvariable = sw6CcValChoice  )
    sw6CcValpinBox.grid(column = 1, row =2)



    root.mainloop()
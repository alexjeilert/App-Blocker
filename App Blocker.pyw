import PySimpleGUI as sg
import datetime
import webbrowser
import playsound
import win32gui
import time

done = []

def checkHandle(hwnd, name):
    global done
    for i in range (2, len(done)):
        if(done[i] in win32gui.GetWindowText(hwnd).lower() and not(win32gui.IsIconic(hwnd))):
            done[0] = True
            done[1] = hwnd
    return True

def checkHandleFromAll(names):
    global done
    done = [False, 0] + names
    win32gui.EnumWindows(checkHandle, done)
    return done[0], done[1]

sg.theme('DarkBrown1')

isOn = False
fileNames = open('names.txt', 'r')
names = fileNames.read().splitlines()

layout = [  [sg.Text('Off', size=(21, 1), justification='center', key='on', font=(30)), sg.Button('Switch', size=(15, 1), key="switch")],
            [sg.InputText(key="newApp"), sg.Button('Add App', size=(7, 1), key="addApp")],
            [sg.Listbox(names, size=(15, 3), key='namesList'), sg.Button('Remove', key="remove")]]

window = sg.Window('App Blocker', layout)

while True:
    #print (names)
    event, values = window.read(timeout=500)
    if(isOn):
        window['on'].update("On")
        result = checkHandleFromAll(names)
        if(result[0]):
            win32gui.CloseWindow(result[1])
    else:
        window['on'].update("Off")

    
    #Add app
    if event == "addApp":
        fileNames.close()
        fileNames = open('names.txt', 'a')
        fileNames.write(values["newApp"].lower()+"\n")
        fileNames.close()
        fileNames = open('names.txt', 'r')
        names = fileNames.read().splitlines()
        window["namesList"].update(names)
    #Turns program on or off
    if event == "switch":
        isOn = not(isOn)
    #To remove an app
    if event == "remove":
        names.remove(values["namesList"][0])
        fileNames.close()
        fileNames = open('names.txt', 'w')
        for name in names:
            fileNames.write(name.lower()+"\n")
        fileNames.close()
        fileNames = open('names.txt', 'r')
        names = fileNames.read().splitlines()
        window["namesList"].update(names)
    #Quit Meny
    if event in (None, 'Quit'):             
        break
    
window.close()





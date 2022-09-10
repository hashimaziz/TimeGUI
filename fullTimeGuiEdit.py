import PySimpleGUI as sg
from discord_webhook import DiscordWebhook
import time
import sys

sg.theme('Black')
done = False
textFont = ('Georgia', 20)
childsName = None
numHours = None
childList = []
tourMessage = ""
url = '' #INSERT DISCORD WEBHOOK HERE

#Basic layout of the screen when the program runs
layout = [[sg.Button('New Signin'), sg.Button('Tour'), sg.Button('Close')]]
mainWindow = sg.Window("Times", layout, font=textFont)

while(not done):
    event, values = mainWindow.read()
    if(event == 'New Signin'):
        #creates a new window where the user can log the students time
        signinWin = [[sg.Text("Type the kids name: "), sg.InputText()], 
                    [sg.Text("Type in the number of hours: "), sg.InputText()], 
                    [sg.Ok(), sg.Cancel()]]
        signinWindow = sg.Window("Sign In", signinWin, font=textFont)

        #reads the content of the window and depending on which button is clicked
        #it will either log the values needed and create a new item in the main window
        #or just close the window
        event, values = signinWindow.read()
        if(event == 'Cancel'):
            signinWindow.close()
        if(event == 'Ok'):
            childsName = values[0]
            childList.append(childsName)
            numHours = values[1]
            timeStruct = time.localtime()
            hour = timeStruct[3]
            minutes = timeStruct[4]
            
            #this just calculates the time when the student is going to leave
            #and start on the next section of the class
            if(minutes < 10):
                minutes = "0" + str(minutes)
            if(int(minutes) + 40 > 60):
                typingMins = minutes + 40 - 60
                typingHour = hour + 1
                if(typingMins < 10):
                    typingMins = "0" + str(typingMins)
            else:
                typingHour = hour
                typingMins = int(minutes) + 40

            signinWindow.close()

            #creates another log in the main window
            newTimer = [sg.Text(childsName), sg.Text("Time In: " + str(hour) + ":" +  str(minutes)), 
                        sg.Text("Typing Time: " + str(typingHour) + ":" + str(typingMins)), 
                        sg.Text("Time Out: " + str(int(hour) + int(numHours)) +  ":" + str(minutes)), 
                        sg.Text("Notes: "), sg.InputText()]#, sg.Checkbox('Typing?'), sg.Checkbox('Stem?')]
    
            mainWindow.extend_layout(mainWindow, [newTimer])
            mainWindow.refresh()
        
    if(event == 'Tour'):
        tourLayout = [[sg.Text("Type in the kids name: "), sg.InputText()], [sg.Text("Evaluation: "), sg.InputText()],
                    [sg.Ok(), sg.Cancel()]]
        tourWin = sg.Window("Tour Evaluation", tourLayout, font=textFont)
        event, values = tourWin.read()
        if(event == "Ok"):
            mainWindow.extend_layout(mainWindow, [[sg.Text("TOUR: " + values[0] + " Evaluation: " + values[1])]])
            mainWindow.refresh()
            tourMessage += values[0] + ": " + "Evaluation: " + values[1] + "\n"
            tourWin.close()
        if(event == "Cancel"):
            tourWin.close()
    
    #when the main window is closed it compiles everything from the main window
    #including the date, the students name and any notes about the student
    #this also helps to keep track of what a student has done in past weeks
    if(event == 'Close' or event == 'WIN_CLOSED'):
        if(values):
            struct = time.localtime()
            month = struct[1]
            day = struct[2]
            year = struct[0]
            date = str(month) + "/" + str(day) + "/" + str(year)
            message = "Kids and Notes for " + str(date) + "\n"
            for i in values:
                message += childList[i] + " Notes: " + values[i] + "\n"
            if(tourMessage != ""):
                message += "\nTour Evaluation\n" + tourMessage
            
            #creates a message to be sent through a discord webhook
            #Will give an error if the url variable at the beginning
            #is empty
            webhook = DiscordWebhook(url, content=message)
            response = webhook.execute()
        done = True
sys.exit()

import PySimpleGUI as sg
from discord_webhook import DiscordWebhook
import time
import sys

sg.theme('Black')
done = False
textFont = ('Georgia', 20)
childsName = None
childList = []
tourMessage = ""
url = '' #needs to be filled in with a discord webhook to send the message or it will end in an error

#creates the layout for the main window
#starts out as just buttons
layout = [[sg.Button('New Signin'), sg.Button('Tour'), sg.Button('Close'), sg.Cancel()]]
mainWindow = sg.Window("Times", layout, font=textFont)

while(not done):
    event, values = mainWindow.read()
    if(event == 'New Signin'):
        #creates a new window where the user can log the students time
        signinWin = [[sg.Text("Type the kids name: "), sg.InputText()], 
                    [sg.Text("Number of hours: "), sg.Checkbox('1'), sg.Checkbox('1.5'), sg.Checkbox('2')], 
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
            timeStruct = time.localtime()
            hour = timeStruct[3]
            minutes = timeStruct[4]
            
            #this calculates the time when the student is going to leave
            #and start on the next section of the class
            for val in values:
                if(values[val] is True):
                    if(val is 1):
                        outTime = str(hour + 1) + ":" + str(minutes)
                    elif(val is 2):
                        if(minutes + 30 > 60):
                            outTime = str(hour + 2) + ":" + str(minutes - 30)
                    elif(val is 3):
                        outTime = str(hour + 2) + ":" + str(minutes)
            
            if(minutes + 40 > 60):
                typingTime = str(hour + 1) + ":" + str(minutes - 20)
            else:
                typingTime = str(hour) + ":" + str(minutes + 40)
            
            #creates another log in the main window
            signinWindow.close()
            newTimer = [sg.Text(childsName), sg.Text("Time In: " + str(hour) + ":" +  str(minutes)), 
                        sg.Text("Typing Time: " + typingTime), 
                        sg.Text("Time Out: " + outTime), 
                        sg.Text("Notes: "), sg.InputText()]
    
            mainWindow.extend_layout(mainWindow, [newTimer])
            mainWindow.refresh()
    
    #different signin window for if a student is being shown the class for the first time
    if(event == 'Tour'):
        tourLayout = [[sg.Text("Type in the kids name: "), sg.InputText()], [sg.Text("Computer Literacy: "), 
                        sg.Checkbox('Great', default=False), sg.Checkbox('Ok', default=False), sg.Checkbox('Needs Work', default=False)], 
                        [sg.Text("Typing Speed: "), sg.InputText()], [sg.Text("Misc: "),sg.InputText()], [sg.Ok(), sg.Cancel()]]

        tourWin = sg.Window("Tour Evaluation", tourLayout, font=textFont)
        event, values = tourWin.read()

        if(event == "Ok"):
            lit = "Computer Literacy: "
            speed = "Typing Speed: "
            misc = "Notes: "
            mainWindow.extend_layout(mainWindow, [[sg.Text("TOUR: " + values[0])]])
            mainWindow.refresh()
            count = 0
            for val in values:
                if(values[val] is True):
                    if(val is 1):
                        lit += "great"
                    elif(val is 2):
                        lit += "Ok"
                    elif(val is 3):
                        lit += "Needs Work"
                    break
            tourMessage += values[0] + ":\n" + lit + '\n' + speed + values[4] + '\n' + misc + values[5]
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
            print(message)
        done = True
        sys.exit()
    
    if(event == 'Cancel'):
        mainWindow.close()
        sys.exit()
sys.exit()

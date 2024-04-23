from datetime import datetime

###########################################################################
### this function will open the log file and append a new line 
### for every action made;
### the line consists of the timestamp of when the function is called
### the user that made the action and
### the action made
###########################################################################
def log (user, action):
    log_file = open("log.txt", "a")
    action_time = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    log_file.write(action_time + " " + user + " " + action)
    log_file.close()

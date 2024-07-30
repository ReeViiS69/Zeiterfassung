import csv
from datetime import datetime
import os

def add_time_to_csv(filename, yn):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if check_exists(filename):
        print('file exists and isnt empty, trying to add entry')
        write_line(filename, current_time, get_lines(filename), yn)
    else:
        print('file is empty or doesnt exist, tring to add time and header')
        write_line(filename, current_time, None, yn)

def check_exists(filename):
    if os.path.isfile(filename) and os.path.getsize(filename) > 0:
        return True

def get_lines(filename):
    with open(filename, mode='r', newline='') as file:
        return file.readlines()
'''
def time_to_write():
    if lines is not None:
        current_line = lines[-1].strip()
    else:
        #workaround for nextline bugfix, so first line of file isnt empty
        current_line='Starttime;Endtime;Pause;'
        file.writelines(current_line)
        
    else:
        #nextline here to prevent bug when current line gets altered manualy and loosing lineend(\n)
        file.writelines('\n'+current_time+';')
        print('added new line with current time')
        
def pause_to_write():
    else:
        file.writelines('pause='+current_time.split(' ',1)[1]+'/')
        print('added pausetime at end of line without date')
'''
def write_line(filename, current_time, lines, yn):
    with open(filename, mode='a', newline='') as file:
        if lines != None:
            current_line = lines[-1].strip()
        else:
            #workaround for nextline bugfix, so first line of file isnt empty, but was kinda still nessesary on its own to make a reasonable representation in excel
            current_line='Starttime;Endtime;Pause;\n'
            file.write(current_line)
        if yn != 'p':
            if  lines == None or '\n' in lines[-1]:
                #fck me...no nextline here to prevent the shit below in else clause...
                #after some idiot edits file and smartly enters nextline so very kindly in last line in his texteditor for next day to be in next line
                file.write(current_time+';')
                print('added IN(!!!)new line with current time')
            elif current_line.count(';') == 1:
                #write current time
                if 'pause' in current_line:
                    #set cursor from current position to start of current line without counting length of each lines
                    #andere methoden die eigentlich straight forward sind, haben nicht funktioniert, mir egal so gehts immer
                    file.seek(file.tell()-len(current_line),os.SEEK_SET)
                    davor=current_line.split(';',1)[0]
                    danach=current_line.split(';',1)[1]
                    i=0
                    current_line = davor+';'+current_time+';'
                    temp=danach.split('/')
                    for danach in temp[:-1]:
                        if i ==1 or i % 2:
                            temp[i]+=';'
                        else:
                            temp[i]+='/'
                        current_line+=temp[i]
                        i+=1
                    file.truncate()
                    file.write(current_line)
                    print('edited last line to include endtime before pausetimes')
                else:
                    file.write(current_time+';')
                    print('added current_time at end of line')
            else:
                #nextline here to prevent bug when current line gets altered manualy and loosing lineend(\n)
                file.write('\n'+current_time+';')
                print('added new line with current time')
        else:
            file.write('pause='+current_time.split(' ',1)[1]+'/')
            print('added pausetime at end of line without date')
def last_happend(file):
    #print(get_lines(file)[-1])
    return get_lines(file)[-1]

def advise_pause_insteadof_time(last_line, yn):
    #do check if pause started without end
    #if true rerun yn input to get user to use time
    try:
        try_time = last_line[-1]
        if try_time[-1]==';':
            print('pause or time set, everthing right')
        else:
            try_pause = last_line.split(';',1)[-1]
            if try_pause.count('/') % 2 == 0:#bei grader anzahl von / ist die pause geschlossen
                print('all pauses closed, enter time is recommended')
            else:
                print('advise to use end pause before end day')
                yn='p'
    except:
        print('other error with pause instead of time?')
    return yn
def advise_time_insteadof_pause(last_line, yn):
    #check for last day ended(2 time entrys) and check for empty file or file with only header line in first line
    try:
        if last_line.count(';')>1 or last_line[-1]=='':
            print('trypause: ', last_line)
            yn=''
            print('set yn=',yn)
        else:
            print('trypause: ', yn)
    except:
        print('other error with time instead of pause?')
    return yn

#def wandel_arbeit_wiederaufnehmen_tag(last_line):
#    return None
def check_last_endday_today(last_line, today_var):
    try:
        last_endtime=datetime.strptime(last_line.split(';')[1], '%Y-%m-%d %H:%M:%S')
        if last_endtime.day == today_var.day:
            print('last endtime day=this day')
            return True
        else:
            print('last endtime not this day')
            return False
    except:
        print('day didnt end jet')
        return False

def reopentoday(filename, last_line, today_var):
    last_entrys=last_line.split(';')
    start= last_entrys[0]
    start_latest_pause=last_entrys[1]#needs date removed
    start_latest_pause=datetime.strptime(start_latest_pause, '%Y-%m-%d %H:%M:%S')
    start_latest_pause='pause='+start_latest_pause.strftime('%H:%M:%S')+'/'
    end_latest_pause='pause='+today_var.strftime('%H:%M:%S')+'/'
    final_pause=start_latest_pause+end_latest_pause
    current_line=start+';'
    try:
        pausen=last_entrys[2:-1]
    except:
        pausen=[]
    print(pausen)
    for pause in pausen:
        current_line+=pause+'/'
    current_line+=final_pause
    with open(filename, mode='a', newline='') as file:
        file.seek(file.tell()-len(last_line),os.SEEK_SET)
        file.truncate()
        file.write(current_line)
        print('edited last line to convert endtime to pause start and end it with current time, ready for next pause or endtime')
    
if __name__ == "__main__":
    today_var=datetime.now()
    try:
        csv_filename = today_var.strftime('%Y-%m''_'+os.getlogin()+'_time_log.csv')
        last_line=last_happend(csv_filename)
        print(last_line)
        yn=input('default file found, enter for timestamp, p for pause:')
    except:
        last_line=['']
        yn=input('Use default filename Year-Month_USERNAME_time_log.csv (enter for default/p: pause in default/name: own name=only time,no pause):')
    endedday_today_bool = check_last_endday_today(last_line, today_var)
    if endedday_today_bool == False:
        if yn=='p':
            yn=advise_time_insteadof_pause(last_line, yn)
            print('check t io p result: ', yn)
        else:
            yn=advise_pause_insteadof_time(last_line, yn)
            print('check p io t result: ', yn)
        if '' != yn and yn != 'p':
            #for custom filename, no pause feature planned, as its targeted usecase is to log times for singletasks bundled in one place to check how much workday was used to work
            csv_filename=yn+'.csv'
        add_time_to_csv(csv_filename, yn)
    else:
        print('heute schon abgeschlossen')
        reenterday=input('tag wieder aufmachen? enter=ja, was anderes=nein')
        if reenterday != '':
            print('ok, bye')
        else:
            reopentoday(csv_filename, last_line, today_var)
    #input('finished, anykey to exit')

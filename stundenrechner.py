import csv
import configparser
from os import getlogin, path
from datetime import datetime as dt, timedelta as td

def create_config_ini(filename, config):#stundenrechner.ini
    config['DEFAULT']={'soll_zeit':'6',
                       'start_uhrzeit':'9'}
    with open(filename, 'w')as configfile:
        config.write(configfile)
        return config

def get_config_ini(filename):
    config = configparser.RawConfigParser()
    if check_exists(filename):
        with open(filename, 'r')as configfile:
            config.read(filename)
            
    else:
        config=create_config_ini(filename, config)
    details_dict = dict(config.items('DEFAULT'))
        
    return details_dict

def check_exists(filename):
    if path.isfile(filename) and path.getsize(filename) > 0:
        
        return True

def read_file(filename):
    with open(filename, mode='r', newline='') as file:
        
        return file.readlines()

def write_output(csv_filename, abweichung, ist_pause, days, weknd, error):
    with open('testoutput.csv', mode='a', newline='') as file:
        file.write(csv_filename+';' +str(abweichung)+';' +str(ist_pause)+';' +str(days)+';' +str(weknd)+';' +error+'\n')
        
def calc_pause_line(line, last_workend, error):
    pause_tag = td()
    current_pauses = line.split(';')[2:]
    if current_pauses:
    #if '\n' != current_pauses[0] != '': #falls man nicht mit startswith arbeiten möchte
        if current_pauses[0].startswith('pause'):
            for pause in current_pauses:
                parts = pause.split('/')                    
                if parts[0].startswith('pause'):
                    pause_start = dt.strptime(f"{last_workend.date()} "+parts[0].split('=')[1], '%Y-%m-%d %H:%M:%S')
                    try:#if parts[1].startswith('pause'):
                        pause_end = dt.strptime(f"{last_workend.date()} "+parts[1].split('=')[1], '%Y-%m-%d %H:%M:%S')
                        if pause_end < pause_start:
                            pause_end=pause_start
                            error += 'pause ends before it starts'+str(pause_start)
                    except:#else:
                        pause_end = pause_start
                    if pause_start <= last_workend:
                        pause_tag += min(pause_end, last_workend) - pause_start
                    
    return pause_tag, error

def calc_time_line(line, last_time, start_uhrzeit, error):
    cur_day_bool = False
    current_times  = line.split(';')
    try:
        cur_datetime  = dt.strptime(current_times[0], '%Y-%m-%d %H:%M:%S')
        if cur_datetime.hour <start_uhrzeit:
            cur_datetime = cur_datetime.replace(hour=9,minute=0,second=0)
        try:
            current_time_dt =dt.strptime(current_times[1], '%Y-%m-%d %H:%M:%S')
        except:
            if current_times[1].startswith('pause'):
                current_time_dt  = dt.strptime(f"{cur_datetime.date()} "+current_times[1].split('=')[1].split('/')[0], '%Y-%m-%d %H:%M:%S')
            else:
                current_time_dt = cur_datetime
            cur_day_bool = True
        if current_time_dt < cur_datetime:
            current_time_dt = cur_datetime
            error += 'endtime before start time:'+str(cur_datetime)
            cur_day_bool = True
        time_tag      = current_time_dt-cur_datetime
    except ValueError:
        time_tag=td()
        current_time_dt=last_time

    return time_tag, current_time_dt, cur_day_bool,error

def calculator(lines, soll_zeit, start_uhrzeit):
    error = ''
    ist_zeit, ist_pause = td(), td()
    last_time=dt.today()
    days, weknd = 0, 0
    for line in lines[1:]:
        time_tag, last_time, cur_day_bool, error = calc_time_line(line, last_time, start_uhrzeit, error)
        if cur_day_bool and last_time.weekday() > 4:
            print('test:curday weekend')
        elif cur_day_bool:
            #print(time_tag)
            #print('test:only curday')
            if time_tag == td():
                days-=1
            #todo:test ob cur day 2 zeit eintrag hat dann nix sonst days-1
        if last_time.weekday() < 5:
            days += 1
        else:
            weknd += 1
        pause_tag, error = calc_pause_line(line, last_time, error)
        #print(ist_zeit, time_tag, pause_tag)
        ist_zeit += time_tag - pause_tag
        ist_pause += pause_tag

    abweichung = ist_zeit - (td(hours=soll_zeit) * days)
    #return str(abweichung), str(ist_pause), days, weknd, error
    return abweichung, ist_pause, days, weknd, error

#def additor(von, bis):
    #von bis angeben um monate zu addieren
    #
def werktage_im_monat(cal_month):
    delta = td(days=1)
    jahr, monat = cal_month.year, cal_month.month
    anfang = cal_month.replace(year=jahr, month=monat, day=1)
    anfang_naechster_monat = anfang.replace(year=jahr + monat // 12, month=(monat % 12) + 1, day=1)
    ende = anfang_naechster_monat - delta
    werktage = 0
    weekend=0
    aktuelles_datum = anfang
    while aktuelles_datum <= ende:
        if aktuelles_datum.weekday() < 5:
            werktage += 1
        else:
            weekend+=1
        aktuelles_datum += delta
    
    return werktage, weekend

def stundenrechner():
    config=get_config_ini('stundenrechner.ini')
    modus       = input('einzeln(1) oder bulk(2)?')
    heute=dt.today()
    soll_zeit      = int(config['soll_zeit'])
    start_uhrzeit  = int(config['start_uhrzeit'])
    target=input('enter=eigener Nutzer, other=username:')
    if target=='':
        username=getlogin()
    else:
        username=target
    abweichung, ist_pause, days, weknd, error=td(),td(),0,0,''
    if int(modus) == 1:
        monate_back = int(input('wie viele monate zurück?0für diesen monat(zwischenrechnung) bis x für januar letztes jahr: '))
        if heute.month-monate_back<=0:
            target_name= heute.replace(month=12-monate_back+heute.month, year=heute.year - 1)
        else:
            target_name= heute.replace(month=heute.month - monate_back)    
        csv_filename   = target_name.strftime('%Y-%m'+'_'+username+'_time_log.csv')
        print(werktage_im_monat(target_name))
        abweichung, ist_pause, days, weknd, error= calculator(read_file(csv_filename), soll_zeit, start_uhrzeit)
        write_output(csv_filename, abweichung, ist_pause, days, weknd, error)
    else:
        monthly=0
        monate_back = int(input('wie viele monate zurück? bis januar letztes jahr: '))
        mitohnediesemmonat=input('mit oder ohne diesen monat:y/n')
        if mitohnediesemmonat=='y':
            monthly=-1
        while monthly < monate_back:
            if heute.month-monate_back<=0:
                target_name= heute.replace(month=12-monate_back+heute.month, year=heute.year - 1)
            else:
                target_name= heute.replace(month=heute.month - monate_back)
            print(werktage_im_monat(target_name))
            csv_filename   = target_name.strftime('%Y-%m'+'_'+getlogin()+'_time_log.csv')
            abweichung_t, ist_pause_t, days_t, weknd_t, error= calculator(read_file(csv_filename), soll_zeit, start_uhrzeit)
            abweichung+=abweichung_t
            ist_pause+=ist_pause_t
            days+=days_t
            weknd+=weknd_t
            error+=error
            monate_back-=1
            write_output(csv_filename, abweichung_t, ist_pause_t, days_t, weknd_t, error)
    return abweichung, ist_pause, days, weknd, error

if __name__ == "__main__":
    #csv_filename = input('enter filename(dont enter .csv at the end):')+'.csv'
    abweichung, ist_pause, days, weknd, error=stundenrechner()
    print('abweichung:',str(abweichung),'schon abgezogene pausezeit:',str(ist_pause),'gearbeitete tage:',days,'gearbeitete tage am we:',weknd,'errors:',error)
    input()

import csv
import configparser
from os import getlogin, path
from datetime import datetime as dt, timedelta as td

def read_file(filename):
    with open(filename, mode='r', newline='') as file:
        
        return file.readlines()[1:]

def write_file(filename, content):
    with open(filename, mode='w', newline='') as file:
        file.write(content)

def converter(excel_filename):
    excelfile=read_file(excel_filename)
    templines=''
    for line in excelfile:
        line_elements=line.split(';')
        starttime_old=dt.strptime(line_elements[0], '%d.%m.%Y %H:%M')
        endtime_old=dt.strptime(line_elements[1], '%d.%m.%Y %H:%M')
        starttime=dt.strftime(starttime_old, '%Y-%m-%d %H:%M:%S')
        endtime=dt.strftime(endtime_old, '%Y-%m-%d %H:%M:%S')
        pauses=''
        for pause in line_elements[2:]:
            if pause!='\r\n':
                pauses+=pause[:29]+';'
        convertedline=starttime+';'+endtime+';'+pauses+'\n'
        templines+=convertedline
    default_csvfile='Starttime;Endtime;Pause;\n'+templines
    return default_csvfile

if __name__ == "__main__":
    today_var=dt.now()
    monthtoconvert=int(input('enter month(MM):'))
    today_var=today_var.replace(month=monthtoconvert)
    csv_filename = today_var.strftime('%Y-%m''_'+getlogin()+'_time_log.csv')
    outputname=input('enterfilename, empty=overwrite')
    if outputname=='':
        outputname=csv_filename
    
    
    
    write_file(outputname,converter(csv_filename))
    

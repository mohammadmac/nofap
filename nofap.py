import calendar
import datetime
import os
import re
import readline

def main():
    print('type \'help\' or \'h\' for more information')
    action = input('[NoFap]>')

    if action in ['nr', 'new record']:
        new_record()
    elif action in ['nd', 'nofap days']:
        nofap_days()
    elif action in ['nc', 'nofap calendar']:
        nofap_calendar()
    elif action in ['q', 'quit', 'exit']:
        exit_program()
    elif action in ['help', 'h']:
        print('\nnr, new record           Set a new record',
        '\nnd, nofap days           Number of days from last fap',
        '\nnc, nofap calendar       Open nofap data file with less',
        '\nh, help                  Display this help',
        '\nq, quit, exit            exit program')
        main()
    else:
        print('Invalid command')
        main()

def new_record():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print('\nYesterday date is: ' + str(yesterday))
    print('Today date is: ' + str(today))
    question = input('Did you fap yesterday?(yes, no) ').lower()
    
    if question == 'yes':
        status = '✖'
        write_new_record(str(yesterday), status)
    elif question == 'no':
        status = '✔'
        write_new_record(str(yesterday), status)
    else:
        print('Invalid command')
        main()

def write_new_record(date, status):
    data_file_path = os.path.dirname(__file__) + '/nofap_data.txt'
    with open(data_file_path, 'r') as f:
        data = f.read().split('*')
        f.close()

    year = date[:4]
    month = datetime.datetime.strptime(date[5:7], "%m").strftime("%B")
    day = date[8:]

    for i in data:
        if month + ' ' + year in i:
            day = re.sub('^0+(?!$)', "", day)
            data[data.index(i)] = i.replace(' ' + day + ' ', ' ' + day + status)
            break
    
    data = '*'.join(data)

    with open(data_file_path, 'w') as f:
        f.write(data)
        f.close()

    main()

def nofap_days():
    read_data()
    
    reverse_data = data[::-1]
    nofap_days = 0
    for i in reverse_data:
        if i == '✔':
            nofap_days += 1
        elif i == '✖':
            break

    print(nofap_days)
    main()

def nofap_calendar():
    data_file_path = os.path.dirname(__file__) + '/nofap_data.txt'
    os.system(f'less {data_file_path}')
    main()

def write_data_file(year, path):
    main_text = ''
    for i in range(1, 13):
        month = i
        month_calendar = calendar.month(int(year), month)
        lines = month_calendar.split('\n')
        main_text += '*\n   ' + lines[0] + '\n'
        for i in lines[1:]: 
            line = i[0:2] + '  ' + i[3:5] + '  ' + i[6:8] + '  ' + i[9:11] + '  ' + i[12:14] + '  ' + i[15:17] + '  ' + i[18:20] + '  '

            main_text += line + '\n'

    with open(path, 'a') as file:
        file.write(main_text)

    return main_text

def read_data():
    global data

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    current_year = date.strftime("%Y")

    file_path = os.path.dirname(__file__) + '/nofap_data.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
    else:
        data = write_data_file(current_year, file_path)

def exit_program():
    print('Exiting program...')
    exit()

def check_year():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    current_year = date.strftime("%Y")

    file_path = os.path.dirname(__file__) + '/nofap_data.txt'
    if current_year in data:
        pass 
    else:
        write_data_file(current_year, file_path)

read_data()
check_year()

main()
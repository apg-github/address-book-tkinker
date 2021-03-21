# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox as msb
import tkinter.font as globalFont


global defaultAddressList
# default address list is used when problem with loading data from file occurs
defaultAddressList = [['Chris', 'Meyers', '241-343-4349'],
                      ['Robert', 'Smith', '202-689-1234'],
                      ['Janet', 'Jones', '609-483-5432'],
                      ['5QWQ', '5', '215-683-2341'],
                      ['Eric', 'Nelson', '571-485-2689'],
                      ['Ford', 'Prefect', '703-987-6543'],
                      ['Mary', 'Zigler', '812-567-8901'],
                      ['Ciupa', 'Smith', '856-689-1234'],
                      ['Drake', 'Smidth', '856-689-1234'],
                      ['Movement', 'Szyn', '856-689-1234'],
                      ['Bob', 'Ukol', '856-689-1234']]


# Chris, Meyers, 241-343-4349
# Robert, Smith, 202-689-1234
def save_data_to_file():
    f = open("address-list.txt", "w")
    temp_arr = defaultAddressList
    for arr in temp_arr:
        f.write(arr[0].strip() + ', ' + arr[1].strip() + ', ' + arr[2].strip() + '\n')


def prepare_data():
    try:
        file = open('address-list.txt', 'r')
        file_read = file.readlines()
        array_of_read_lines_from_file = []
        nested_array = []

        # convert array of string to array of array of string
        # eg. ['Chris, Meyers, 241-343-4349', 'Robert, Smith, 202-689-1234'] convert to:
        # [['Chris', ' Meyers', ' 241-343-4349'], ['Robert', ' Smith', ' 202-689-1234']]
        for line in file_read:
            array_of_read_lines_from_file.append(line.replace('\n', ''))
        for newline in array_of_read_lines_from_file:
            nested_array.append(newline.split(','))

        globals()['defaultAddressList'] = nested_array
        file.close()
    except Exception:
        print('Coś poszło nie tak z odczytem danych z pliku.')
        file.close()
        pass


def which_selected():
    return int(select.curselection()[0])


def clear_inputs():
    fnamevar.set('')
    fname.focus()
    lnamevar.set('')
    phonevar.set('')


# parametr self=None jest konieczny w związku z bindowaniem entera do odpalenia tej funkcji, zgodnie z wątkiem w linku
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def add_entry(self=None):
    try:
        if len(fnamevar.get()) == 0:
            raise ValueError
        elif len(lnamevar.get()) == 0:
            raise ValueError
        elif len(phonevar.get()) == 0:
            raise ValueError
        defaultAddressList.append([fnamevar.get(), lnamevar.get(), phonevar.get()])
        set_select()
        clear_inputs()
    except ValueError:
        msb.showinfo(title='Dodawanie wpisu', message='Wypełnij wszystkie pola aby dodać wpis do listy.')
        pass


def update_entry():
    try:
        if len(fnamevar.get()) == 0:
            raise ValueError
        elif len(lnamevar.get()) == 0:
            raise ValueError
        elif len(phonevar.get()) == 0:
            raise ValueError
        elif which_selected() < 0:
            raise ValueError
        defaultAddressList[which_selected()] = [fnamevar.get(), lnamevar.get(), phonevar.get()]
        set_select()
        clear_inputs()
    except ValueError:
        msb.showinfo(title='Aktualizowanie wpisu', message='Zaznacz wpis oraz uzupełnij wszystkie pola aby zaktualizować wpis.')
        pass


# parametr self=None jest konieczny w związku z bindowaniem entera do odpalenia tej funkcji, zgodnie z wątkiem w linku
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def delete_entry(self=None):
    try:
        if which_selected() < 0:
            raise Exception
        del defaultAddressList[which_selected()]
        set_select()
    except Exception:
        msb.showinfo(title='Usuwanie wpisu', message='Musisz zaznaczyć wpis aby go usunąć.')
        pass


def load_entry():
    try:
        if which_selected() < 0:
            raise Exception
        fname, lname, phone = defaultAddressList[which_selected()]
        fnamevar.set(fname)
        lnamevar.set(lname)
        phonevar.set(phone)
    except Exception:
        msb.showinfo(title='Załadowanie wpisu', message='Musisz zaznaczyć wpis aby go załadować do inputów.')
        pass


def make_window():
    global fnamevar, lnamevar, phonevar, select, fname

    win = Tk()
    win.title('Prosta książka adresowa')
    frame1 = Frame(win)
    frame1.pack(padx=30, pady=30)

    Label(frame1, text="Imię", width=20).grid(row=0, column=0, sticky=W, padx=5)
    fnamevar = StringVar()
    fname = Entry(frame1, textvariable=fnamevar, width=50)
    fname.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    Label(frame1, text="Nazwisko", width=20).grid(row=1, column=0, sticky=W, padx=5)
    lnamevar = StringVar()
    lname = Entry(frame1, textvariable=lnamevar, width=50)
    lname.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    Label(frame1, text="Telefon", width=20).grid(row=2, column=0, sticky=W, padx=5)
    phonevar = StringVar()
    phone = Entry(frame1, textvariable=phonevar, width=50)
    phone.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    frame2 = Frame(win)
    font = globalFont.Font(family='Helvetica', size=10, weight='bold')
    frame2.pack(padx=30, pady=30)
    b1 = Button(frame2, text="Dodaj nowy ", command=add_entry, fg='blue')
    b1['font'] = font
    b2 = Button(frame2, text="Zaktualizuj wybrany", command=update_entry)
    b2['font'] = font
    b3 = Button(frame2, text="Usuń wybrany", command=delete_entry, fg='red')
    b3['font'] = font
    b4 = Button(frame2, text="Załaduj wybrany", command=load_entry)
    b4['font'] = font
    b5 = Button(frame2, text="Odśwież listę i usuń zaznaczenie", command=set_select)
    b5['font'] = font
    b1.pack(side=LEFT, padx=5, pady=5)
    b2.pack(side=LEFT, padx=5, pady=5)
    b3.pack(side=LEFT, padx=5, pady=5)
    b4.pack(side=LEFT, padx=5, pady=5)
    b5.pack(side=LEFT, padx=5, pady=5)

    frame3 = Frame(win)
    frame3.pack(padx=30, pady=30)
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=10, width=100)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)
    return win


def set_select():
    defaultAddressList.sort(key=lambda record: record[1])
    select.delete(0, END)
    clear_inputs()
    for fname, lname, phone in defaultAddressList:
        select.insert(END, "{0}, {1}, {2}".format(fname.strip(), lname.strip(), phone.strip()))
    save_data_to_file()
    defaultAddressList.sort(key=lambda record: record[1])


prepare_data()
win = make_window()
set_select()
win.geometry('900x600')
win.configure(background='white')
win.eval('tk::PlaceWindow . center')
win.bind('<Return>', add_entry)
win.bind('<Delete>', delete_entry)
win.mainloop()

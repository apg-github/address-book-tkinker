# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox as msb
import tkinter.font as globalFont
import copy
import tkinter as tk

# default address list is used when problem with loading data from file occurs
# new data file is filled with default data
defaultAddressList = []


def save_data_to_file():
    f = open("address-list.txt", "w")

    # used deepcopy because array is nested
    temp_arr = copy.deepcopy(defaultAddressList)

    for arr in temp_arr:
        f.write(arr[0].strip() + ', ' + arr[1].strip() + ', ' + arr[2].strip() + '\n')

    f.close()

    print('Data saved successfully.')


def check_duplicate(name, surname, addressorphone):
    for contact_line in defaultAddressList:
        if name.strip() == contact_line[0].strip() and surname.strip() == contact_line[1].strip() and addressorphone.strip() == contact_line[2].strip():
            raise NameError


def prepare_data():
     try:
        file = open('address-list.txt', 'r')
        file_read = file.readlines()

        print('Saved data file found.')

        array_of_read_lines_from_file = []
        nested_array = []

        # convert array of string to array of array of string
        # eg. ['Chris, Meyers, 241-343-4349', 'Robert, Smith, 202-689-1234'] converts to:
        # [['Chris', ' Meyers', ' 241-343-4349'], ['Robert', ' Smith', ' 202-689-1234']]
        for line in file_read:
            array_of_read_lines_from_file.append(line.replace('\n', ''))
        for newline in array_of_read_lines_from_file:
            nested_array.append(newline.split(','))

        # overwrite global address list with new list read from a file
        globals()['defaultAddressList'] = nested_array
        file.close()
     except FileNotFoundError:
         print('Saved data file cannot be found or opened. Creating new one...')
         f = open("address-list.txt", "w+")
         f.close()
     except:
         print("Unhandled exception occurs. Please consider letting know to administrator or app developer.")


def which_selected():
        selection_decider = int(select.curselection()[0])

        if selection_decider >= 0:
            return selection_decider
        else:
            raise IndexError


def clear_inputs():
    firstnamevar.set('')

    fname.focus()

    lastnamevar.set('')

    phoneoraddressvar.set('')

# self=None parameter is obligatory due to binding key to function
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def add_entry(self=None):
    try:
        if len(firstnamevar.get().strip()) == 0 or len(lastnamevar.get().strip()) == 0 or len(phoneoraddressvar.get().strip()) == 0:
            raise ValueError
        elif firstnamevar.get().find(',') >= 0 or lastnamevar.get().find(',') >= 0 or phoneoraddressvar.get().find(',') >= 0:
            raise AssertionError

        check_duplicate(firstnamevar.get().strip().title(), lastnamevar.get().strip().title(), phoneoraddressvar.get().strip().title())

        defaultAddressList.append([firstnamevar.get().title(), lastnamevar.get().title(), phoneoraddressvar.get().title()])

        reset_set_save_select()

        clear_inputs()
    except ValueError:
        msb.showinfo(title='Entry addition', message='Fill all inputs to perform entry addition.')
        pass
    except AssertionError:
        msb.showinfo(title='Entry addition', message='Input cannot contain illegal characters like commas.')
        pass
    except NameError:
        msb.showinfo(title='Entry addition', message='Identical entry already exists.')
        pass


def update_entry():
    try:
        if len(firstnamevar.get().strip()) == 0 and len(lastnamevar.get().strip()) == 0 and len(phoneoraddressvar.get().strip()) == 0:
            raise ValueError
        elif firstnamevar.get().find(',') >= 0 or lastnamevar.get().find(',') >= 0 or phoneoraddressvar.get().find(',') >= 0:
            raise AssertionError
        elif type(which_selected()) != int:
            raise IndexError

        check_duplicate(firstnamevar.get().strip(), lastnamevar.get().strip(), phoneoraddressvar.get().strip())

        defaultAddressList[which_selected()] = [
            firstnamevar.get().capitalize() or defaultAddressList[which_selected()][0],
            lastnamevar.get().capitalize() or defaultAddressList[which_selected()][1],
            phoneoraddressvar.get().capitalize() or defaultAddressList[which_selected()][2]
        ]

        reset_set_save_select()

        clear_inputs()
    except ValueError:
        msb.showinfo(title='Entry update', message='Fill any of input to update overwritten data.')
        pass
    except AssertionError:
        msb.showinfo(title='Entry update', message='Input cannot contain illegal characters like commas.')
        pass
    except IndexError:
        msb.showinfo(title='Entry update', message='Select an entry to perform update.')
        pass
    except NameError:
        msb.showinfo(title='Entry update', message='Identical entry already exists.')
        pass

# self=None parameter is obligatory due to binding key to function
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def delete_entry(self=None):
    try:
        if type(which_selected()) != int:
            raise IndexError

        del defaultAddressList[which_selected()]

        reset_set_save_select(False)
    except IndexError:
        msb.showinfo(title='Entry deletion', message='Select an entry to perform deletion.')
        pass


def load_entry_to_inputs():
    try:
        if which_selected() < 0:
            raise Exception

        fname, lname, phone = defaultAddressList[which_selected()]

        firstnamevar.set(fname)

        lastnamevar.set(lname)

        phoneoraddressvar.set(phone)
    except Exception:
        msb.showinfo(title='Load entry to input', message='Select an entry to load data to inputs.')
        pass


def prepare_window():
    global firstnamevar, lastnamevar, phoneoraddressvar, select, fname

    root = Tk()
    root.title('Simple Contact Book')
    root.option_add('*Font', 'Calibri 12')

    frame1 = tk.Frame(root, bg='#ede4da')
    frame1.pack(padx=30, pady=20)
    Label(frame1, text="Name", width=20, height=4).grid(row=0, column=0, sticky=W )
    firstnamevar = StringVar()
    fname = Entry(frame1, textvariable=firstnamevar, width=50, font='Calibri')
    fname.grid(row=0, column=1, sticky=W, padx=20, pady=5)

    Label(frame1, text="Surname", width=20, height=4).grid(row=1, column=0, sticky=W)
    lastnamevar = StringVar()
    lname = Entry(frame1, textvariable=lastnamevar, width=50, font='Calibri')
    lname.grid(row=1, column=1, sticky=W, padx=20, pady=5)

    Label(frame1, text="Phone or Address", width=20, height=4).grid(row=2, column=0, sticky=W)
    phoneoraddressvar = StringVar()
    phone = Entry(frame1, textvariable=phoneoraddressvar, width=50, font='Calibri')
    phone.grid(row=2, column=1, sticky=W, padx=20, pady=5)

    frame2 = tk.Frame(root, bg='#ede4da', padx=15, pady=20)
    font = globalFont.Font(family='Calibri', size=12)
    frame2.pack()
    b1 = Button(frame2, text="Add new entry", command=add_entry, fg='#388c31', padx=10, pady=10, font=font, bg='white')
    b2 = Button(frame2, text="Update entry", command=update_entry, padx=10, pady=10, font=font, bg='white')
    b3 = Button(frame2, text="Delete entry", command=delete_entry, fg='red', padx=10, pady=10, font=font, bg='white')
    b4 = Button(frame2, text="Load entry", command=load_entry_to_inputs, padx=10, pady=10, font=font, bg='white')
    b5 = Button(frame2, text="Refresh list and uncheck", command=reset_set_save_select, padx=10, pady=10, bg='white', font=font)
    b1.pack(side=LEFT, padx=5, pady=5)
    b2.pack(side=LEFT, padx=5, pady=5)
    b3.pack(side=LEFT, padx=5, pady=5)
    b4.pack(side=LEFT, padx=5, pady=5)
    b5.pack(side=LEFT, padx=5, pady=5)

    frame3 = Frame(root)
    frame3.pack(padx=30, pady=20)
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=10, width=100, activestyle="dotbox", bg='#ede4da',
                     borderwidth=20, relief='flat', font='Calibri', selectbackground='#ca522a')
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)
    return root


def reset_set_save_select(clear: bool = True):
    try:
        defaultAddressList.sort(key=lambda record: record[0])

        select.delete(0, END)

        clear : clear_inputs()

        for fname, lname, phone in defaultAddressList:
            select.insert(END, "{0}, {1}, {2}".format(fname.strip().capitalize(), lname.strip().capitalize(), phone.strip().capitalize()))

        defaultAddressList.sort(key=lambda record: record[0])

        save_data_to_file()
    except ValueError:
        print('Data file parsing error. Consider creating new file, check error on your own. Consider letting know to administrator or app developer.')
        quit()


prepare_data()

window = prepare_window()

reset_set_save_select()

window.geometry('900x700')

window.configure(background='white')

window.eval('tk::PlaceWindow . center')

window.bind('<Return>', add_entry)
window.bind('<Delete>', delete_entry)

window.mainloop()

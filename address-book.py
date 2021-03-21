# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox as msb
import tkinter.font as globalFont

# default address list is used when problem with loading data from file occurs
# new data file is filled with default data
global defaultAddressList
defaultAddressList = [['Charles', 'McGill', '321-6435-4349'],
                      ['Robert', 'Smithers', '202-345-1234'],
                      ['Janet', 'Jones', '543-483-2342'],
                      ['James', 'Ziegler', '432-543-2341'],
                      ['Werner', 'Ziegler', '571-485-2689'],
                      ['Ford', 'Prefect', '5234-4535-6543'],
                      ['Mary', 'Zigler', '812-5435-324'],
                      ['Ciupa', 'Smith', '856-689-56253'],
                      ['Drake', 'Smidth', '342-534-1234'],
                      ['Movement', 'Szymon', '856-689-1234'],
                      ['Bob', 'Ukol', '532-689-3425']]


def save_data_to_file():
    f = open("address-list.txt", "w")
    temp_arr = defaultAddressList
    for arr in temp_arr:
        f.write(arr[0].strip() + ', ' + arr[1].strip() + ', ' + arr[2].strip() + '\n')


def prepare_data():
    try:
        file = open('address-list.txt', 'r')
        file_read = file.readlines()
        print('Saved data file opened successfully.')
        array_of_read_lines_from_file = []
        nested_array = []

        # convert array of string to array of array of string
        # eg. ['Chris, Meyers, 241-343-4349', 'Robert, Smith, 202-689-1234'] converts to:
        # [['Chris', ' Meyers', ' 241-343-4349'], ['Robert', ' Smith', ' 202-689-1234']]
        for line in file_read:
            array_of_read_lines_from_file.append(line.replace('\n', ''))
        for newline in array_of_read_lines_from_file:
            nested_array.append(newline.split(','))

        globals()['defaultAddressList'] = nested_array
        file.close()
    except Exception:
        print('Saved data file cannot be found or opened. Creating new one...')
        f = open("address-list.txt", "w+")
        f.close()



def which_selected():
    # try:
        selection_decider = int(select.curselection()[0])
        if selection_decider >= 0:
            return selection_decider
    # except:
    #     return None

def clear_inputs():
    fnamevar.set('')
    fname.focus()
    lnamevar.set('')
    phoneoraddressvar.set('')

# self=None parameter is obligatory due to binding key to function
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def add_entry(self=None):
    try:
        if len(fnamevar.get()) == 0:
            raise ValueError
        elif len(lnamevar.get()) == 0:
            raise ValueError
        elif len(phoneoraddressvar.get()) == 0:
            raise ValueError
        elif fnamevar.get().find(',') or lnamevar.get().find(',') or phoneoraddressvar.get().find(','):
            raise AssertionError
        defaultAddressList.append([fnamevar.get(), lnamevar.get(), phoneoraddressvar.get()])
        reset_set_save_select()
        clear_inputs()
    except ValueError:
        msb.showinfo(title='Entry addition', message='Fill all inputs to perform entry addition.')
        pass
    except AssertionError:
        msb.showinfo(title='Entry addition', message='Input cannot contain illegal characters like commas.')
        pass


def update_entry():
    try:
        if len(fnamevar.get()) == 0:
            raise ValueError
        elif len(lnamevar.get()) == 0:
            raise ValueError
        elif len(phoneoraddressvar.get()) == 0:
            raise ValueError
        elif type(which_selected()) == int:
            raise ValueError
        elif fnamevar.get().find(',') or lnamevar.get().find(',') or phoneoraddressvar.get().find(','):
            raise AssertionError
        defaultAddressList[which_selected()] = [fnamevar.get(), lnamevar.get(), phoneoraddressvar.get()]
        reset_set_save_select()
        clear_inputs()
    except ValueError:
        msb.showinfo(title='Entry update', message='Select an entry and fill inputs to perform update.')
        pass
    except AssertionError:
        msb.showinfo(title='Entry update', message='Input cannot contain illegal characters like commas.')
        pass
    except IndexError:
        msb.showinfo(title='Entry update', message='Select an entry to perform update.')
        pass


# self=None parameter is obligatory due to binding key to function
# https://stackoverflow.com/questions/43839536/typeerror-generatecode-takes-0-positional-arguments-but-1-was-given/43839602
def delete_entry(self=None):
    try:
        if which_selected() < 0:
            raise Exception
        del defaultAddressList[which_selected()]
        reset_set_save_select()
    except Exception:
        msb.showinfo(title='Entry deletion', message='Select an entry to perform deletion.')
        pass


def load_entry_to_inputs():
    try:
        if which_selected() < 0:
            raise Exception
        fname, lname, phone = defaultAddressList[which_selected()]
        fnamevar.set(fname)
        lnamevar.set(lname)
        phoneoraddressvar.set(phone)
    except Exception:
        msb.showinfo(title='Load entry to input', message='Select an entry to load data to inputs.')
        pass


def prepare_window():
    global fnamevar, lnamevar, phoneoraddressvar, select, fname

    root = Tk()
    root.title('Simple Contact Book')
    frame1 = Frame(root)
    frame1.pack(padx=30, pady=30)

    Label(frame1, text="Name", width=20).grid(row=0, column=0, sticky=W, padx=5)
    fnamevar = StringVar()
    fname = Entry(frame1, textvariable=fnamevar, width=50)
    fname.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    Label(frame1, text="Surname", width=20).grid(row=1, column=0, sticky=W, padx=5)
    lnamevar = StringVar()
    lname = Entry(frame1, textvariable=lnamevar, width=50)
    lname.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    Label(frame1, text="Phone or Address", width=20).grid(row=2, column=0, sticky=W, padx=5)
    phoneoraddressvar = StringVar()
    phone = Entry(frame1, textvariable=phoneoraddressvar, width=50)
    phone.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    frame2 = Frame(root)
    font = globalFont.Font(family='Helvetica', size=10, weight='bold')
    frame2.pack(padx=30, pady=30)
    b1 = Button(frame2, text="Add new entry", command=add_entry, fg='blue')
    b1['font'] = font
    b2 = Button(frame2, text="Update entry", command=update_entry)
    b2['font'] = font
    b3 = Button(frame2, text="Delete entry", command=delete_entry, fg='red')
    b3['font'] = font
    b4 = Button(frame2, text="Load entry", command=load_entry_to_inputs)
    b4['font'] = font
    b5 = Button(frame2, text="Refresh list and uncheck", command=reset_set_save_select)
    b5['font'] = font
    b1.pack(side=LEFT, padx=5, pady=5)
    b2.pack(side=LEFT, padx=5, pady=5)
    b3.pack(side=LEFT, padx=5, pady=5)
    b4.pack(side=LEFT, padx=5, pady=5)
    b5.pack(side=LEFT, padx=5, pady=5)

    frame3 = Frame(root)
    frame3.pack(padx=30, pady=30)
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=10, width=100)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)
    return root


def reset_set_save_select():
    defaultAddressList.sort(key=lambda record: record[1])
    select.delete(0, END)
    clear_inputs()
    for fname, lname, phone in defaultAddressList:
        select.insert(END, "{0}, {1}, {2}".format(fname.strip(), lname.strip(), phone.strip()))
    save_data_to_file()
    defaultAddressList.sort(key=lambda record: record[1])


prepare_data()
window = prepare_window()
reset_set_save_select()
window.geometry('900x600')
window.configure(background='white')
window.eval('tk::PlaceWindow . center')
window.bind('<Return>', add_entry)
window.bind('<Delete>', delete_entry)
window.mainloop()

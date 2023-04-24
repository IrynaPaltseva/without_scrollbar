import datetime
from tkinter import *
import tkinter as t
from tkinter import ttk, messagebox
import datetime as dt
from tkcalendar import DateEntry
import csv
import json



def main():
    status = ["Didn't even started", "In progress", "Yay,Done!"]
    date = dt.datetime.now()

    window = t.Tk()
    window.config(background='#94B39A')
    window.title("The Best To Do List Ever!")
    window.geometry("1550x1500")

    title_entry = None
    description_entry = None
    time_entry = None
    edit_status_combobox = None
    etime_entry = None

    task_list = []
    tasks_counter = 0
    initial_form_data = {
        "title": "",
        "description": "",
        "status": status[0],
        "end_time": datetime.datetime.today(),
        'index': -1
    }
    form_data = {
        "title": "",
        "description": "",
        "status": status[0],
        "end_time": datetime.datetime.today(),
        'index': -1
    }
    # bg = PhotoImage(file="bg.png")

    # canvas = Canvas(window, scrollregion=(0, 0, 900, 900))
    # canvas.create_image(0, 0, image=bg,
    #                     anchor="nw")
    # canvas.grid(row=0, column=0)

    # bg_label = t.Label(window, image=bg)
    # bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = t.Frame(window, background='#94B39A', padx=20)  # frame inside window
    frame.grid()

    # vsb = Scrollbar(frame, orient="vertical", command=canvas.yview)
    # vsb.grid(row=0, column=1, sticky='ns')
    # canvas.configure(yscrollcommand=vsb.set)

    # frame.config(width=950, height=550)
    # canvas.config(scrollregion=(0, 0, 500, 800))  # canvas.bbox("all"))

    frame_all_tasks = t.LabelFrame(frame, background='#94B39A', font=("Times", 10, "bold"), padx=20, pady=10, )
    frame_all_tasks.grid(row=1, column=1)
    label1 = t.Label(frame, background='#94B39A', text="ALL YOUR TASKS IN ONE PLACE:", font=("Times", 13), padx=5, pady=5)
    label1.grid(row=0, column=1)

    frame_beginning = t.LabelFrame(frame_all_tasks, text='To Do', font=("Times", 10, "bold"), background='#94B39A', width=500, padx=5, pady=5)
    frame_beginning.config(width=450)
    frame_beginning.grid(row=2, column=0, sticky='nw', ipadx=0, ipady=0)

    frame_in_progress = t.LabelFrame(frame_all_tasks, text='In Progress', font=("Times", 10, "bold"), background='#94B39A', width=500, padx=5, pady=5)
    frame_in_progress.grid(row=2, column=1, sticky='nw')

    frame_done = t.LabelFrame(frame_all_tasks, text='Done!', font=("Times", 10, "bold"), background='#94B39A',width=500, padx=5, pady=5)
    frame_done.grid(row=2, column=2, sticky='nw')

    def openNewWindow(is_update=False):

        global new_window
        new_window = Toplevel(window, background='#EEA579', padx=20, pady=10)
        new_window.title("Needs to be done ASAP")
        new_window.geometry("470x350")
        new_window.focus()

        frame_Info = t.LabelFrame(new_window, text="New task", background='#EEA579', font=("Times", 10, 'bold'), padx=20, pady=10)
        frame_Info.grid()

        title_label = t.Label(frame_Info, text='Title: ', background='#EEA579',  font=("Times", 13), padx=5, pady=5)
        title_label.grid(row=0, column=0, sticky='w')
        nonlocal title_entry
        title_entry = t.Entry(frame_Info, width=40, font=("Times", 10, "bold"))
        title_entry.insert(END, form_data['title'])
        title_entry.grid(row=0, column=1, sticky='w')

        description_label = t.Label(frame_Info, text='Description: ', background='#EEA579', font=("Times", 13), padx=5, pady=5)
        description_label.grid(row=1, column=0, sticky='w')

        nonlocal description_entry
        description_entry = t.Text(frame_Info, width=35, height=3)
        description_entry.insert(END, form_data['description'])
        description_entry.grid(row=1, column=1, ipady=60, sticky='w')

        if is_update:
            description_label = t.Label(frame_Info, text='Status: ', background='#EEA579', font=("Times", 13), padx=5, pady=5)
            description_label.grid(row=2, column=0, sticky='w')
            nonlocal edit_status_combobox
            edit_status_combobox = ttk.Combobox(frame_Info, values=status, state='readonly')
            edit_status_combobox.current(status.index(form_data['status']))
            edit_status_combobox.grid(row=2, column=1)

        time_label = t.Label(frame_Info,background='#EEA579', text='Due date: ', font=("Times", 13), padx=5, pady=5)
        time_label.grid(row=3, column=0, sticky='w')
        nonlocal time_entry
        today = date.today()
        year = form_data['end_time'].year
        month = form_data['end_time'].month
        day = form_data['end_time'].day
        time_entry = DateEntry(frame_Info, selectmode='day', year=year, month=month,
                       day=day, width=44, background='darkblue',
                       foreground='white', borderwidth=2, mindate=today)
        time_entry.grid(row=3, column=1, sticky='w')

        # button
        button_text = "Update task" if is_update else "Create task"
        button_command = update_single_task if is_update else create_task
        button_new = t.Button(frame_Info, background='#c96115', text=button_text,
                              font=("Times", 13, "bold"), borderwidth=0, command=button_command)
        button_new.grid(row=5, columnspan=2)

    #*********************************************************************************************** form

    def add_task_to_list():
        nonlocal tasks_counter
        tasks_counter += 1
        new_task_dict = {
            'id': tasks_counter,
            'title': title_entry.get(),
            'description': description_entry.get("1.0", 'end-1c'),
            'status': status[0],
            'end_time': time_entry.get_date()
        }
        task_list.append(new_task_dict)

    def clear_new_task_form_data():
        nonlocal form_data
        form_data = initial_form_data

    def display_task(task):
        task_id = task['id']
        title = task['title']
        description = task['description']
        end_date = task['end_time']
        task_status = task['status']

        parent = get_task_parent(task_status)

        single_task_frame = t.LabelFrame(
            parent,
            font=("Times", 10, "bold"),
            padx=5,
            pady=5,
            background='#94B39A'
        )
        # nonlocal single_task_frame
        single_task_frame.grid(padx=(5, 0), sticky='w') # 400

        create_label(parent=single_task_frame, text='Task Title: ', row=0, column=0, sticky='w')
        # create_label(single_task_frame, title, 0, 1, 'w')
        title2_entry = t.Label(single_task_frame, text=title, font=("Times", 13, 'bold'), background='#94B39A')
        title2_entry.grid(row=0, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Task Description: ', row=1, column=0, sticky='w')
        # create_label(parent=single_task_frame, text=description,  row=1, column=1, sticky='w')

        description_label = t.Label(single_task_frame, background='#94B39A', text=description, width=30, wraplength=280,
                                    justify=LEFT, font=("Times", 13), padx=5, pady=5)
        description_label.grid(row=1, column=1, sticky='news')

        create_label(parent=single_task_frame, text='Task was set on: ', row=2, column=0, sticky='w')
        create_label(parent=single_task_frame, text=f"{date:%A, %B %d, %Y}", row=2, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Due date: ', row=3, column=0, sticky='w')
        create_label(parent=single_task_frame, text=end_date.strftime("%A, %B %d, %Y"), row=3, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Status: ', row=4, column=0, sticky='w')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="gray", background="gray")

        status_combobox = ttk.Combobox(single_task_frame, values=status, state='readonly')
        status_combobox.bind("<<ComboboxSelected>>", lambda event: change_status(event, task_id))
        status_combobox.current(status.index(task_status))
        status_combobox.grid(row=4, column=1, sticky='w')

        # buttons
        button_edit = t.Button(single_task_frame, text='Edit', font=("Times", 12), background='#1A5653', command=lambda: edit_task(task_id))
        button_edit.grid(row=5, column=1)
        button_delete = t.Button(single_task_frame, background='#1A5653', text='Del', font=("Times", 12),
                                 command=lambda: delete_task(task_id))
        button_delete.grid(row=5, column=1, sticky='w')

        # clear_frame(selected_frame)

    def get_task_parent(task_status):
        parent = frame_beginning

        if task_status == status[1]:
            parent = frame_in_progress
        elif task_status == status[2]:
            parent = frame_done

        return parent

    def show_all_tasks():
        read_from_file()
        for task in task_list:
            display_task(task)

    def write_in_file():
        print("The list of dictionaries is:")
        print(task_list)
        myFile = open('demo_file.csv', 'w')
        writer = csv.DictWriter(myFile, fieldnames=['id', 'title', 'description', 'status', 'end_time'])
        writer.writeheader()
        writer.writerows(task_list)
        myFile.close()

    def read_from_file():
        myFile = open('demo_file.csv', 'r')
        reader = csv.DictReader(myFile)
        csvList = list()
        for dictionary in reader:
            csvList.append(dictionary)
        print("The list of dictionaries is:")
        print(csvList)
        task_list=csvList
        print('eee', task_list)
        for dict in csvList:
            print(dict['status'])

    def create_label(parent, text, row, column,  sticky):
        new_label = t.Label(parent, background='#94B39A', text=text, font=("Times", 13), padx=5, pady=5)
        new_label.grid(row=row, column=column, sticky=sticky)

    def clear_screen():
        clear_frame(frame_done)
        clear_frame(frame_in_progress)
        clear_frame(frame_beginning)

    def clear_frame(selected_frame):
        if selected_frame != None:
            for child in selected_frame.winfo_children():
                child.destroy()

    def create_task():
        add_task_to_list()
        update_tasks()
        clear_new_task_form_data()
        new_window.destroy()


    def update_tasks():
        clear_screen()
        show_all_tasks()

    def update_single_task():
        get_form_data()
        update_task_dictionary()
        update_tasks()
        new_window.destroy()

    def get_form_data():
        nonlocal form_data
        updated_form_data = {
            'id': form_data['id'],
            'title': title_entry.get(),
            'description': description_entry.get("1.0", 'end-1c'),
            'status': edit_status_combobox.get(),
            'end_time': time_entry.get_date(),
            'index': form_data['index']
        }
        form_data = updated_form_data

    def update_task_dictionary():
        updated_task = {
            "id": form_data['id'],
            "title": form_data['title'],
            "description": form_data['description'],
            "end_time": form_data['end_time'],
            "status": form_data['status']
        }
        task_list[form_data['index']] = updated_task

    def change_status(event, task_id):
        selected_box = event.widget
        value = selected_box.get()

        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                task_list[i]['status'] = value
                break

        update_tasks()

    def delete_task(task_id):
        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                del task_list[i]
                break
        update_tasks()

    def edit_task(task_id):
        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                nonlocal form_data
                form_data = task_list[i]
                form_data['index'] = i
                break
        openNewWindow(True)


    # button

    buttonAddTask = t.Button(frame, text='+ Add task', background='#1A5653', font=("Times", 12), command=openNewWindow)
    buttonAddTask.grid(row=2, column=1, padx=10, pady=10, sticky='es')

    buttonSave = t.Button(frame, text='Save', background='#1A5653', font=("Times", 12), command=write_in_file)
    buttonSave.grid(row=3, column=1, padx=10, pady=10, sticky='es')

    buttonRead = t.Button(frame, text='Open', background='#1A5653', font=("Times", 12), command=show_all_tasks)
    buttonRead.grid(row=4, column=1, padx=10, pady=10, sticky='es')

    window.mainloop()

main()

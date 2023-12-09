# Library Import
import pandas as pd
import sys
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re

# Variables
data = None
saving_goals = None
username_entry = None
password_entry = None
root = None

# username and password file
def create_credentials_file():
    if not os.path.exists('users.txt'):
        with open('users.txt', 'w') as f:
            f.write('username:password\n')

# GUI create account
def create_account():
    global username_entry, password_entry, username, password
    username = username_entry.get()
    password = password_entry.get()
    filename = f"{username}_transactions.xlsx"
    with open('users.txt', 'a') as file:
        file.write(f'{username}:{password}\n')
    if re.fullmatch(r'^[A-Za-z0-9]*$', username) and re.fullmatch(r'^[A-Za-z0-9]*$', password):
        messagebox.showinfo("Success", "Account created successfully!")
        data = pd.DataFrame(columns=['date', 'value', 'operation','catagory', 'saving_goal', 'goal_value', 'goal_start_date', 'goal_end_date'])
        data.to_excel(filename, index=False)
    else:
        messagebox.showerror("Error", "Invalid username or password. Only alphanumeric characters are allowed.")

# GUI sign in
def sign_in():
    global username_entry, password_entry, username, password
    username = username_entry.get()
    password = password_entry.get()
    with open('users.txt', 'r') as file:
        for line in file:
            data = line.strip().split(':')
            if data[0] == username and data[1] == password:
                return True
    return False

# GUI sign in message
def sign_in_command():
    username = username_entry.get()
    password = password_entry.get()
    with open('users.txt', 'r') as file:
        for line in file:
            login_info = line.strip().split(':')
            if login_info[0] == username and login_info[1] == password:
                messagebox.showinfo("Login Successful", "Welcome back, " + username)
                root.destroy()
                start_cmd(username)
                break
            elif username == "" or password == "":
                messagebox.showerror("Error", "Username or Password cannot be empty")
                break
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

# GUI reset password
def reset_password():
    username = username_entry.get()
    try:
        with open('users.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if line.strip().startswith(username + ':'):
                password = line.strip().split(':')[1]
                Label(root, text=f"Your password is: {password}").grid(row=4, column=0)
                break
        else:
            Label(root, text="User not found!").grid(row=4, column=0)
    except FileNotFoundError:
        Label(root, text="User not found!").grid(row=4, column=0)

# CMD I/O
def add_transaction(username):
    global data, goal_value, value, date
    try:
        date = datetime.strptime(input("\nEnter transaction date (DD/MM/YYYY): "), '%d/%m/%Y')
    except ValueError:
        print("Incorrect date format, please try again!")
        return
    try:
        value = float(input("Enter transaction value: "))
        if value <= 0:
            raise ValueError
    except ValueError:
        print("You must enter a value larger than 0")
        return
    while True:
        operation = input("Enter operation ('deposit' or 'withdrawal'): ").lower()
        if operation in ['deposit', 'withdrawal']:
            break
        else:
            print("Please enter either deposit or withdrawal")
    category = input("Enter the category of the transaction: ")
    saving_goal = input("Enter 'Y' if you want to set a goal, else enter 'N': ").upper()
    if saving_goal in ['Y', 'N']:
        if saving_goal == 'Y':
            goal_value = float(input("Enter saving goal value: "))
            try:
                goal_start_date = datetime.strptime(input("\nEnter goal start date (DD/MM/YYYY): "), '%d/%m/%Y')
            except ValueError:
                print("Incorrect date format, please try again!")
                return
            try:
                goal_end_date = datetime.strptime(input("\nEnter goal end date (DD/MM/YYYY): "), '%d/%m/%Y')
            except ValueError:
                print("Incorrect date format, please try again!")
                return
        if saving_goal == 'N':
            goal_value = np.nan
            goal_start_date = np.nan
            goal_end_date = np.nan
    else:
        print("Please enter either Y or N")
        return
    new_transaction = pd.Series([date, value, operation, category, saving_goal, goal_value, goal_start_date, goal_end_date],
                                 index=['date', 'value', 'operation','category', 'saving_goal', 'goal_value', 'goal_start_date', 'goal_end_date'])
    data = data.append(new_transaction, ignore_index=True)
    data.to_excel(f'{username}_transactions.xlsx', index=False, columns=['date', 'value', 'operation','category', 'saving_goal', 'goal_value', 'goal_start_date', 'goal_end_date'])
    
# Graph plot 
def generate_dates(transactions):
    return [mdates.date2num(pd.to_datetime(date, dayfirst=True, format='%d/%m/%Y')) for date in transactions['date']]

def show_line_graph():
    deposits = data[data['operation'] == 'deposit']
    withdrawals = data[data['operation'] == 'withdrawal']

    fig, ax = plt.subplots()
    ax.plot(deposits['date'], deposits['value'], 'ro', markersize=10, label='Deposits', linestyle='')
    ax.plot(withdrawals['date'], withdrawals['value'], 'go', markersize=10, label='Withdrawals', linestyle='')

    total_deposits = deposits.groupby('date')['value'].sum().reset_index()
    total_withdrawals = withdrawals.groupby('date')['value'].sum().reset_index()

    ax.plot(total_deposits['date'], total_deposits['value'], 'bo', markersize=10, label='Total Deposits', linestyle='-')
    ax.plot(total_withdrawals['date'], total_withdrawals['value'], 'mo', markersize=10, label='Total Withdrawals', linestyle='-')

    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title('Saving')
    ax.legend()

    plt.show()

def show_dot_graph():
    daily_transactions = data.groupby(data['Date'].dt.date)['value'].sum().reset_index(name='Total')

    plt.figure(figsize=(10,5))

    plt.plot(daily_transactions['Date'], daily_transactions['Total'], marker='o', linestyle='-')

    plt.title('Total Deposit and Withdrawal by Day')
    plt.xlabel('Date')
    plt.ylabel('Total')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# CMD
def start_cmd(username):
    global data, saving_goals
    file_exists = os.path.isfile(f'{username}_transactions.xlsx')
    if file_exists:
        data = pd.read_excel(fr'{username}_transactions.xlsx')
        data['Date'] = pd.to_datetime(data['date'], dayfirst=True, format='%d/%m/%Y')
    else:
        data = pd.DataFrame(columns=['date', 'value', 'operation','catagory', 'saving_goal', 'goal_value', 'goal_start_date', 'goal_end_date'])
        data.to_excel(f'{username}_transactions.xlsx', index=False)
    saving_goals = data['saving_goal'].apply(lambda x: x != 'N')
    data['Total Saving Deposit'] = data['value'][data['operation'] == 'deposit']
    data['Total Saving Withdrawal'] = data['value'][data['operation'] == 'withdrawal']
    while True:
        print("1. Add transaction")
        print("2. Show line/dot graph")
        print("3. Sign out")
        print("4. Exit application")
        choice = input("\nEnter choice: ")
        valid_choices = all('1' <= c <= '4' for c in choice)
        if valid_choices and len(choice) == 1:
            for c in choice:
                if c == '1':
                    add_transaction(username)
                elif c == '2':
                    print("Please close the line graph to view the dot graph!")
                    show_line_graph()
                    show_dot_graph()
                elif c == '3':
                    create_login_screen()
                elif c == '4':
                    sys.exit()
                else:
                    print("Please enter number from 1-4!")
                    return
        else:
            print("Please enter number 1-4!")
            return

# GUI create
def create_login_screen():
    global username_entry, password_entry, root, usernames
    root = tk.Tk()
    root.title("Money Management App")
    root.geometry("300x200")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))
    mainframe = ttk.Frame(root, padding="3 3 3 3")

    mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    Label(mainframe, text="Username").grid(row=0, column=0, sticky=tk.W)
    Label(mainframe, text="Password").grid(row=1, column=0, sticky=tk.W)

    username_entry = ttk.Entry(mainframe, width=20)
    password_entry = ttk.Entry(mainframe, width=20, show='*')
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    ttk.Button(mainframe, text="Create Account", command=create_account).grid(row=2, column=0, sticky=tk.W)
    ttk.Button(mainframe, text="Sign In", command=sign_in_command).grid(row=2, column=1, sticky=tk.E)
    ttk.Button(mainframe, text="Forget Password", command=reset_password).grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E)

    root.protocol("WM_DELETE_WINDOW", lambda: (sys.exit(0), root.destroy()))

    root.mainloop()

# Function Run
create_login_screen()
start_cmd()
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
import csv
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# todo Set the style for the graphs
sns.set_theme(style="dark")
np.set_printoptions(legacy='1.25')

#todo Create the main menu, to see full balance and add income and expenses
def display_balance():
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancetransactions.csv")
    df = pd.read_csv(dir_df)
    balance = df["balance_after_transation"].values[-1]
    print(f"Your balance is £{balance}\n") #Print the last recorded balance
    return balance

def write_new_transaction(new_id,new_balance,entity,amount,type,notes=''):
    with open("personalfinancetransactions.csv", mode="a") as transactions:
        writer = csv.DictWriter(transactions, fieldnames=["transaction_id","entity","amount","type","notes","balance_after_transation"])
        writer.writerow({
            "transaction_id":new_id, #? PK
            "entity":entity,
            "amount":amount,
            "type":type,
            "notes":notes,
            "balance_after_transation":new_balance
        })

def write_time(new_id,amount):
    #todo Get the time unit
    print("How would you like to record this time?\n1) hours   2) days   3) weeks")
    accept_unit = False
    #Ensure data integrity
    while not accept_unit:
        try:
            time_unit = int(input("   >> "))
            if time_unit < 1 or time_unit > 3:
                print("Sorry, invalid unit. Try again")
            else:
                accept_unit = True
        except:
            print("Sorry, invalid unit. Try again")
    #todo Get time value
    time_units = ["hours","days","weeks"]
    print(f"How many {time_units[time_unit-1]} did it take you to earn these £{amount}?")
    accept_time = False
    #Data integrity
    if time_unit == 1: #? hours
        accept_hours = False
        print("Type separately the number of hours and minutes")
        print("Hours")
        while not accept_hours:
            hours = input("   >> ")
            try:
                hours = int(hours)
                if hours < 24:
                    accept_hours = True
                else:
                    print("Sorry, invalid time. Try again")
            except:
                print("Sorry, invalid time. Try again")
        print("Minutes")
        while not accept_time:
            mins = input("   >> ")
            try:
                mins = int(mins)
                if hours < 60:
                    accept_time = True
                else:
                    print("Sorry, invalid time. Try again")
            except:
                print("Sorry, invalid time. Try again")
        print(pd.Timedelta(hours=hours, minutes=mins))
        time_value = pd.Timedelta(hours=hours, minutes=mins)
    elif time_unit == 2: #? days
        print("You may type it as a decimal number")
        print("Short guide: 12 hours = 0.5 days| 8 hours = 0.33 days| 6 hours = 0.25 days| 4 hours = 0.2 days")
        while not accept_time:
            days = input("   >> ")
            try:
                days = float(days)
                accept_time = True
            except:
                print("Sorry, invalid time. Try again")
        print(pd.Timedelta(days=days))
        time_value = pd.Timedelta(days=days)
    else: #? weeks
        print("Type separately the number of weeks and days. You may leave the later blank")
        print("Weeks")
        accept_weeks = False
        while not accept_weeks:
            weeks = input("   >> ")
            try:
                weeks = int(weeks)
                accept_weeks = True
            except:
                print("Sorry, invalid time. Try again")
        days = 0
        print("Days")
        while not accept_time:
            days_input = input("   >> ")
            if not days_input:
                accept_time = True
            else:
                try:
                    days = int(days_input)
                    accept_time = True
                except:
                    print("Sorry, invalid time. Try again")
        print(pd.Timedelta(weeks=weeks, days=days))
        time_value = pd.Timedelta(weeks=weeks, days=days)
    #todo Write on the time records table
    with open("personalfinancetimerecords.csv", mode="a") as tr:
        writer = csv.DictWriter(tr, fieldnames=["transaction_id","time"])
        writer.writerow({
            "transaction_id":new_id, #? PK
            "time":time_value
        })

def new_transaction(type):
    #todo Enter the function with the transaction type already 
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancetransactions.csv")
    df = pd.read_csv(dir_df)

    #todo Get the amount of the transaction TB
    print("Amount")
    accept_amount = False
    while not accept_amount:
        try:
            amount = float(input("   >> £"))
            amount = round(amount,2)
            accept_amount = True
        except:
            print("Sorry, invaid amount. Try again")
    #todo Get the entity T
    if type == "in":
        print(f"What's the source of these £{amount}?")
    else:
        print(f"What organisation did you spend these £{amount} on?")
    entity = input("   >> ")
    #todo Calculate the new transaction_id TB
    last_id = df["transaction_id"].max()
    new_id = last_id + 1
    #todo Calculate the new balance B
    if df["balance_after_transation"].size == 0:
        last_balance = 1
    else:
        last_balance = df["balance_after_transation"].values[-1]

    if type == "in":
        new_balance = last_balance + amount
    else:
        new_balance = last_balance - amount
    new_balance = round(new_balance,2)
    #todo Get any notes about the transaction that the user might want to record
    print("Any notes to add")
    notes = input("   >> ")

    #todo Now, write the data on the tables
    write_new_transaction(new_id,new_balance,entity,amount,type,notes)

    #todo Add time
    if type == "in":
        print("Add the time it took you to earn this money?\nType Y to proceed, or anything else to ignore")
        time_action = input("   >> ").lower()
        if time_action == "y":
            write_time(new_id,amount)

#todo Add wage 
def add_wage():
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancewages.csv")
    df = pd.read_csv(dir_df)
    #todo Get a name for the wage
    print("Give a name to this wage")
    accept_name = False
    past_name = ""
    while not accept_name:
        name = input("   >> ")
        if name in df["wage_name"].values:
            print("Sorry, a wage with that name already exists. Type @ to review it, or enter a different name")
            past_name = name
        elif name == "@":
            print(df[df["wage_name"] == past_name])
            print("Type another name")
        else:
            accept_name = True
    #todo Get hourly rate
    print("How much do you earn per hour?")
    accept_rate = False
    while not accept_rate:
        try:
            hourly_rate = float(input("   >> £"))
            hourly_rate = round(hourly_rate,2)
            accept_rate = True
        except:
            print("Sorry, invalid rate. Try again")
    #todo Get hours per week
    print("How many hours do you work per week?")
    accept_hours_week = False
    while not accept_hours_week:
        try:
            hours_week = int(input("   >> "))
            accept_hours_week = True
        except:
            print("Sorry, invalid input. Try again")
    #todo Write info on the csv file
    with open("personalfinancewages.csv",mode="a") as wg:
        writer = csv.DictWriter(wg, fieldnames=["wage_name","hourly_rate","hours_per_week"])
        writer.writerow({
            "wage_name":name, #? PK
            "hourly_rate":hourly_rate,
            "hours_per_week":hours_week
        })

#todo Add recurring incomes and expenses
def recurrings(type):
    #Check whether this is a wage
    if type == "in":
        print("Is this a wage?\nInput Y if it is, or anything else if it is not")
        is_wage = input("   >> ").lower()
        if is_wage == "y":
            add_wage()
            sys.exit()
    #todo Enter function knowing the type
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancerecurrings.csv")
    df = pd.read_csv(dir_df)
    #todo Give the recurring a name
    print("Name this recurring. You CANNOT change this later")
    # Check whether there's a recurring with that name already
    accept_name = False
    while not accept_name:
        name = input("   >> ")
        if name in df["recurring_name"].values:
            print("Sorry, you already have a recurring with that name. Try again")
        else:
            accept_name = True
    #todo Get the amount
    print("Regular amount")
    accept_amount = False
    while not accept_amount:
        try:
            amount = float(input("   >> £"))
            amount = round(amount,2)
            accept_amount = True
        except:
            print("Sorry, invalid amunt format. Try again")
    #todo Get the entity
    if type == "in":
        print(f"Who is giving you these £{amount}")
    else:
        print(f"To whom must you pay these £{amount}")
    entity = input("   >> ")
    #todo Get the frequency
    if type == "in":
        print("How often will you get this money?")
    else:
        print("How often must you pay this money?")
    print("1) Weekly\n2) Monthly\n3) Yearly")
    accept_frequency = False
    # Check that the inputted frequency is of valid format
    while not accept_frequency:
        frequency = int(input("   >> "))
        if frequency < 1 or frequency > 3:
            print("Sorry, frequency not recognised. Try again")
        else:
            accept_frequency = True
    #todo Get the reminder
    print("When would you like to be reminded of this recurring?")
    accept_reminder = False
    # Create a function to check the validity of user input
    def check_reminder_validity(reminder,max):
        valid = False
        if reminder < 1 or reminder > max:
            print("Sorry, invalid reminder. Try again")
        else:
            valid = True
        return valid

    if frequency == 1:
        print("1) Sunday\n2) Monday\n3) Tuesday\n4) Wednesday\n5) Thursday\n6) Friday\n7) Saturday")
        # Check that it's a valid reminder
        while not accept_reminder:
            reminder = int(input("   >> "))
            accept_reminder = check_reminder_validity(reminder,7)
    elif frequency == 2:
        print("Type the date of the month (1-28)")
        while not accept_reminder:
            reminder = int(input("   > "))
            accept_reminder = check_reminder_validity(reminder,28)
    else:
        print("1) January 01\n2) February 01\n3) March 01\n4) April 01\n5) May 01\n6) June 01\n7) July 01")
        print("8) August 01\n9) September 01\n10) October 01\n11) Novermber\n12) December")
        while not accept_reminder:
            reminder = int(input("   >> "))
            accept_reminder = check_reminder_validity(reminder,12)     
    #todo Write this in the recurrings table
    with open("personalfinancerecurrings.csv", mode="a") as recurrings:
        writer = csv.DictWriter(recurrings, fieldnames=["recurring_name","amount","type","entity","frequency","reminder"])
        writer.writerow({
            "recurring_name":name, #? PK
            "amount":amount,
            "type":type,
            "entity":entity,
            "frequency":frequency,
            "reminder":reminder
        })

#todo Create a savings folder
def create_savings_folder():
    #todo Fields: name (what you're saving for), amount

    #todo Get the name
    print("Name this folder. What are you saving for?")
    name = input("   >> ")
    #todo Get the amount
    print(f"How much money do you want to set as your goal for {name}?")
    #Ensure data integrity
    accept_amount = False
    while not accept_amount:
        try:
            amount = float(input("   >> £"))
            amount = round(amount,2)
            accept_amount = True
        except:
            print("Sorry, invalid amount. Try again")
    #todo Write this in the folders file
    with open("personalfinancesavingsfolders.csv", mode="a") as sf:
        writer = csv.DictWriter(sf, fieldnames=["folder_name","amount","saved"])
        writer.writerow({
            "folder_name":name,
            "amount":amount,
            "saved":0
        })

#todo View pie chart of full balance against savings folders
#todo The pie is divided into the value of the balance that's left after paying all folders (balance - sum(amount))
#todo If there is not enough balance to pay all folders, the whole of the pie chart becomes the sum of the folders
#todo The balance, then, becomes a slice of the pie
def view_balance_vs_folders_chart():
    #todo Get the total balance
    #! Open file
    dir_df_balance = os.path.join(BASE_DIR, "personalfinancetransactions.csv")
    df_balance = pd.read_csv(dir_df_balance)
    balance = df_balance["balance_after_transation"].values[-1]
    #todo Get the folders
    #! Open file
    dir_df_folders = os.path.join(BASE_DIR, "personalfinancesavingsfolders.csv")
    df_folders = pd.read_csv(dir_df_folders)
    # Get a list of the names
    folder_names = list(df_folders["folder_name"].values) #? ["PSP","Phone case"] 316.84
    print(folder_names)
    # Get a list of the values in the same order
    #* Make a list of the saved column
    folder_saved = list(df_folders["saved"].values) #? [80.99,0]
    #* Make a list of the totals of each folder
    folder_totals = list(df_folders["amount"].values) #? [180.99,15]
    print("folder_totals", folder_totals)
    #* Make a list of how much is left from each folder
    folder_remaining = []
    for i in range(len(folder_totals)):
        rem = round(folder_totals[i] - folder_saved[i],2)
        folder_remaining.append(rem) #? [100.0,15.0] Here, no remaining of totals yet
    # Get the balance that is left over
    total_in_folders = df_folders["amount"].sum()
    remainder = round(balance - total_in_folders,2)
    # Create the new folders for divided values
    new_names_folder = []
    new_data_folder = []
    for i in folder_names:
        new_names_folder.append(f"{i}_remaining")
        new_names_folder.append(f"{i}_saved_up")
    for i in range(len(folder_remaining)):
        new_data_folder.append(folder_remaining[i])
        new_data_folder.append(folder_saved[i])
    #todo Make slices for recurring costs, telling whether they are monthly or weekly (include yearly costs as monthly)
    #! Open files
    dir_df_recurrings = os.path.join(BASE_DIR, "personalfinancerecurrings.csv")
    df_recurrings = pd.read_csv(dir_df_recurrings)
    #* Make a list of the names of the recurring expenses
    list_recurrings_names = list(df_recurrings[df_recurrings["type"] == "out"]["recurring_name"].values)
    #? ["Gym membership","Microsoft subscription"]
    #* Create a list of the frequencies
    list_frequency = list(df_recurrings[df_recurrings["type"] == "out"]["frequency"].values)
    #* Create a list of the costs
    list_recurrings_data = list(df_recurrings[df_recurrings["type"] == "out"]["amount"])
    #* Add the frequency of that expence to the name
    for recurring in range(len(list_recurrings_names)):
        frequency_num = list_frequency[recurring]
        if frequency_num == 1:
            weekly_cost = list_recurrings_data[recurring]
            frequency_lbl = f"_£{weekly_cost}_weekly"
        elif frequency_num == 3:
            yearly_cost = list_recurrings_data[recurring]
            frequency_lbl = f"_£{yearly_cost}_yearly"
        else:
            frequency_lbl = "_monthly"
        list_recurrings_names[recurring] += frequency_lbl
    #* Equalise all numeric values to be monthly
    for i in range(len(list_frequency)):
        if list_frequency[i] == 3:
            list_recurrings_data[i] = round(list_recurrings_data[i]/12,2)
        elif list_frequency[i] == 1:
            list_recurrings_data[i] = list_recurrings_data[i]*4

    new_names_folder += list_recurrings_names
    new_data_folder += list_recurrings_data

    #* Calculate the total monthly in recurring costs

    total_from_recurrings = 0
    for i in list_recurrings_data:
        total_from_recurrings += i
    remainder = round(remainder - total_from_recurrings,2)

    #todo Get the data for when the sum of the folders is less than the balance
    def ready_data_normal():
        new_names_folder.append("Remainder")
        new_data_folder.append(remainder)
        total = balance
        title = f"Total: £{balance}"
        return [total,title,new_data_folder,new_names_folder]
    #todo Get the data for when the sum of the folders is greater than the balance
    def ready_data_overflowing():
        total = total_in_folders+total_from_recurrings
        remaining = round(total-balance,2)
        title = f"Balance: £{balance}\nTotal folders + recrring costs: £{total}\nStill needs to be saved up: £{remaining}"
        return [total,title,new_data_folder,new_names_folder]
    #todo Draw the chart with the data already calculated
    def draw_chart(total,title,folder_amounts,folder_names):
        n_slices = len(folder_amounts)          # or whatever your data list is
        colours = sns.color_palette("rocket_r", n_colors=n_slices)
        labels = []
        for price in folder_amounts:
            labels.append(f"£{price}")
        plt.pie(folder_amounts, labels=labels,colors=colours,startangle=90,explode=explode)
        plt.legend(
            folder_names,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )
        plt.title(title)
        plt.show()
    explode = [0] * len(new_data_folder)
    if remainder > 0:
        total,title,folder_amounts,folder_names = ready_data_normal()
        explode.append(0.1)
    else:
        total,title,folder_amounts,folder_names = ready_data_overflowing()
        
    draw_chart(total,title,folder_amounts,folder_names)

#todo Edit savings folders
def edit_folders():
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancesavingsfolders.csv")
    df = pd.read_csv(dir_df)
    print(df)
    #todo Get an index to edit
    print("Write the index of the folder you wish to edit")
    index = int(input("   >> "))
    #todo Get the action to perform
    print("1) Change folder_name   2) Change amount   3) Add money   4) Take money out of this folder   5) Delete folder")
    accept_change = False
    while not accept_change:
        change = int(input("   >> "))
        if change < 1 or change > 5:
            print("Sorry, invalid input. Try again")
        else:
            accept_change = True
    changes = [
        "Type the new name",
        "Type the new amount",
        "How much money do you wish to add to this folder?",
        "How much money do you wish to remove from this folder?",
        "This action cannot be undone. Are you sure you want to continue? (Y/N)"
    ]
    print(changes[change-1])
    #* create functions for editing the numeric variables
    def edit_amount(new_value):
        df.loc[index,"amount"] = new_value
    def edit_savings(new_value):
        df.loc[index,"saved"] += new_value
        return df.loc[index,"saved"]
    #todo Get the folder name
    folder_name = df.loc[index,"folder_name"]
    asker = "  >> "
    if change == 3 or change == 4:
        asker += "£"
    new_value = input(asker)
    #* if the value is numeric
    if change == 2 or change == 3:
        accept_new_value = False
        while not accept_new_value:
            try:
                new_value = float(new_value)
                new_value = round(new_value,2)
                accept_new_value = True
            except:
                print("Sorry, invalid value. Try again")
                new_value = input(asker)
        if change == 2:
            edit_amount(new_value)
        elif change == 3: #? Add money
            new_saved = edit_savings(new_value)
            balance = df.loc[index,"amount"]
            if new_saved >= balance:
                print("Folder paid off")
                folder_deleted = True
                if new_saved > balance:
                    to_give_back = new_saved - balance
                    new_value -= to_give_back
                    print(f"£{new_value} paid into the {df.loc[index,"folder_name"]} folder")
                df = df.drop([index])

    #* if the user wished to take money out
    elif change == 4:
        #todo Get the money to be taken out and ensure data integrity
        accept_money_out = False
        while not accept_money_out:
            try:
                new_value = float(new_value)
                accept_money_out = True
            except:
                print("Sorry, invalid amount. Try again")
                new_value = input(asker)
        #todo Get the amount saved in the folder and substract the amount to be removed
        money_available = df.loc[index,"saved"]
        folder_title = df.loc[index,"folder_name"]
        new_saved = round(money_available-new_value,2)
        df.loc[index, "saved"] = new_saved
    #* if the user wishes to delete a folder
    elif change == 5:
        accept_del = False
        while not accept_del:
            if new_value == "y" or new_value == "n":
                accept_del = True
            else:
                print("Sorry, invalid value. Try again")
                new_value = input(asker)
        if new_value == "y":
            #todo Calculate amount for later transaction back into the main account
            new_value = df.loc[index,"saved"]
            #todo Calculate entity
            folder_name = df.loc[index,"folder_name"]
            #todo Delete folder
            df = df.drop([index])
            print(df)
    #* if the value is a string
    else:
        df.loc[index,"folder_name"] = new_value
    #todo Write back in the savings folders csv file
    df.to_csv("personalfinancesavingsfolders.csv", index=False)

#todo Edit recurrents
def edit_recurrents():
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancerecurrings.csv")
    df = pd.read_csv(dir_df)

    df["frequency"].replace(1,"weekly",inplace=True)
    df["frequency"].replace(2,"monthly",inplace=True)
    df["frequency"].replace(3,"yearly",inplace=True)
    print(df)
    print("Type the index of the recurring you wish to edit")
    accept_index = False
    while not accept_index:
    #todo Choose the recurring to edit
        index = int(input("   >> "))
        if index <= df.shape[0]:
            try:
                index = float(index)
                index = round(index,2)
                accept_index = True
            except:
                print("Sorry, invalid index. Try again")
        else:
            print("Sorry, invalid index. Try again")
    #todo Get the change to be made
    print("What modification would you like to make to this recurring?")
    print("1) Change the amount   2) Change the frequency   3) Change the reminder   4) Delete recurring")
    change = int(input("   >> "))
    #todo Change amount
    if change == 1:
        print("What is the new amount?")
        accept_new_amount = False
        while not accept_new_amount:
            new_amount = input("   >> £")
            try:
                new_amount = float(new_amount)
                new_amount = round(new_amount,2)
                accept_new_amount = True
            except:
                print("Sorry, invalid amount. Try again")
        df.loc[index,"amount"] = new_amount
    #todo Change frequency
    elif change == 2:
        print("What is the new frequency of this recurring?")
        print("1) Weekly\n2) Monthly\n3) Yearly")
        accept_new_freq = False
        while not accept_new_freq:
            new_freq = input("   >> ")
            try:
                new_freq = int(new_freq)
                if new_freq <= 3:
                    accept_new_freq = True
                else:
                    print("Sorry, invalid input. Try again")
            except:
                print("Sorry, invalid input. Try again")
        df.loc[index,"frequency"] = new_freq
    #todo Change reminder
    elif change == 3:
        frequency = df.loc[index,"frequency"]
        #* Get a maximum for data integrity linked to frequency
        max = 7
        list_index = 0
        if frequency == "monthly":
            max = 28
            list_index = 1
        else:
            frequency = 12
            list_index = 2
        freqs = [
            ["1) Sunday","2) Monday","3) Tuesday","4) Wednesday","5) Thursday","6) Friday","7) Saturday"],
            ["Type the date numerically (1-28)"],
            ["1) January","2) February","3) March","4) April","5) May","6) June","7) July",
             "8) August","9) September","10) October","11) November","12) December"]
        ]
        for i in freqs[list_index]:
            print(i)
        #* Get the new reminder
        print("What is the new frequency you would like for this recurring?")
        accept_reminder = False
        while not accept_reminder:
            reminder = input("   >> ")
            try:
                reminder = int(reminder)
                if reminder < 1 or reminder > max:
                    print("Sorry, invalid reminder. Try again")
                else:
                    accept_reminder = True
            except:
                print("Sorry, invalid reminder. Try again")
        #* Write the new reminder
        df.loc[index,"reminder"] = reminder
    elif change == 4:
        df = df.drop([index])
    #* Turn frequencies back to numerical form
    df["frequency"].replace("weekly",1,inplace=True)
    df["frequency"].replace("monthly",2,inplace=True)
    df["frequency"].replace("yearly",3,inplace=True)
    #* Write back in the recurrings table
    df.to_csv("personalfinancerecurrings.csv", index=False)

#todo View savings folders
def view_folders():
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancesavingfolders.csv")
    df = pd.read_csv(dir_df)
    #todo Calculate how many hours of work would be needed to afford each savings folder, based on recurring income sources
    #! Open file
    dir_df_wages = os.path.join(BASE_DIR, "personalfinancewages.csv")
    df_wages = pd.read_csv(dir_df_wages)
    #todo Calculate how much is left
    df["remaining"] = df["amount"] - df["saved"]
    #* Calculate variables to calculate how many hours of the main income source are needed to earn that money
    max_hours_week = df_wages["hours_per_week"].max()
    main_wage_name = df_wages[df_wages["hours_per_week"] == max_hours_week][["wage_name"]].values[0][0]
    main_wage_value = df_wages[df_wages["hours_per_week"] == max_hours_week][["hourly_rate"]].values[0][0]
    #* Create column for hours that need to be worked
    column_name = f"hours_to_work_with_{main_wage_name}"
    df[column_name] = round(df["remaining"]/main_wage_value,2)
    times = list(df[column_name].values)
    total_time_dec = df[column_name].sum()
    time_str = []
    total_hours = 0
    total_minutes = 0
    for time_dec in times:
        hours = int(time_dec)
        minutes = int((time_dec - hours) * 60)
        new_time = f"{hours}:{minutes}"
        time_str.append(new_time)
    df[column_name] = time_str
    #* Calculate total time to pay all folders with total_time_dec
    hours = int(total_time_dec)
    minutes = f"{int((total_time_dec - hours) * 60)}".zfill(2)
    full_time = f"{hours}:{minutes}"
    #todo Display percentage of completion
    df["percentage_complete_%"] = round(df["saved"]/df["amount"]*100,2)
    #todo Display
    print(df)
    print(f"Your total balance is £{balance}")
    print(f"With your {main_wage_name}, you must work {full_time} hours to pay off all your folders")
    print()
    total_in_folders = df["amount"].sum()
    if total_in_folders <= balance:
        print(f"You can afford all your savings folders. You'll have £{round(balance - total_in_folders,2)} left after paying them")
    else:
        print(f"You still need £{round(total_in_folders - balance,2)} to afford all your folders")
    print()

    #todo Edit folders
    print("Press @ to edit folders, or leave blank to skip")
    edit = input("   >> ")
    if edit == "@":
        edit_folders()
#todo View recurrings
def view_recurrings():
    #todo Wages
    #! Open file
    dir_df_wages = os.path.join(BASE_DIR, "personalfinancewages.csv")
    df_wages = pd.read_csv(dir_df_wages)
    df_wages["weekly_earnings"] = df_wages["hourly_rate"] * df_wages["hours_per_week"]
    print("Wages")
    print(df_wages)
    #* total per wages
    weekly_wages = df_wages["weekly_earnings"].sum()
    print(f"Total weekly earning from wage(s): £{weekly_wages} ~ roughly £{weekly_wages*4} a month")
    print()
    #todo Other incomes
    #! Open file
    dir_df = os.path.join(BASE_DIR, "personalfinancerecurrings.csv")
    df = pd.read_csv(dir_df)
    df["frequency"] = df["frequency"].replace(1,"weekly")
    df["frequency"] = df["frequency"].replace(2,"monthly")
    df["frequency"] = df["frequency"].replace(3,"yearly")
    #* equalise frequency to monthly
    df["monthly_amount"] = np.nan
    mask_weekly = df["frequency"] == "weekly"
    df.loc[mask_weekly,"monthly_amount"] = round(df["amount"] * 4,2)
    mask_yearly = df["frequency"] == "yearly"
    df.loc[mask_yearly,"monthly_amount"] = round(df["amount"] / 12,2)
    df["monthly_amount"] = df["monthly_amount"].fillna(df["amount"])

    df_in = df.loc[df["type"] == "in"]
    #todo Expenses
    df_out = df.loc[df["type"] == "out"]
    print("Recurring incomes")
    print(df_in)
    #* total per other incomes
    total_incomes = df_in["monthly_amount"].sum()
    print(f"From your other income sources, you make £{total_incomes} a month")
    print()
    print("Recurring expenses")
    print(df_out)
    #* total per expenses
    total_expenses = df_out["monthly_amount"].sum()
    print(f"You are spending £{total_expenses} a month for your recurring expenses")
    print()
    #todo Wages + OtherIncomes - Expenses
    overall = (weekly_wages*4)+total_incomes-total_expenses
    total_hours = df_wages["hours_per_week"].sum()
    print(f"Your recurring income sources together minus your recurring expenses leave you with £{overall} a month")
    print(f"Working {total_hours} hours per week")
    if overall <= 10:
        print("You need to take urgent measures to remedy your financial situation")
    elif overall < 200:
        print("You have a comfortable balance between income and expenses")
    else:
        print("Congratulations! You have an excellent balance between income and expenses. You may treat yourself to a whim!")

#todo Recurrings chart
def recurrings_vs_chart():
    #todo Read and filter .csv file to only expenditure
    #! Open file
    dir_df_recurrings = os.path.join(BASE_DIR, "personalfinancerecurrings.csv")
    df_recurrings = pd.read_csv(dir_df_recurrings)
    df_recurrings = df_recurrings.loc[df_recurrings["type"] == "out"].reset_index()
    #todo Equalise price to monthly
    df_recurrings["monthly_price"] = np.nan
    mask_weekly = df_recurrings["frequency"] == 1
    mask_yearly = df_recurrings["frequency"] == 3
    df_recurrings.loc[mask_weekly,"monthly_price"] = round(df_recurrings["amount"] * 4,2)
    df_recurrings.loc[mask_yearly,"monthly_price"] = round(df_recurrings["amount"] / 12,2)
    df_recurrings["monthly_price"] = df_recurrings["monthly_price"].fillna(df_recurrings["amount"])
    print(df_recurrings)
    #todo Create a list with the labels
    list_names = list(df_recurrings["recurring_name"].values)
    #* Create a list of the frequencies to edit the names in the name list
    list_freqs = list(df_recurrings["frequency"].values)
    for i in range(len(list_freqs)):
        if list_freqs[i] == 1:
            list_names[i] += f" (£{df_recurrings.loc[[i],"amount"].values[0]} paid weekly)"
        elif list_freqs[i] == 3:
            list_names[i] += f" (£{df_recurrings.loc[[i],"amount"].values[0]} paid yearly)"
    #todo Create a list with the values
    list_data = list(df_recurrings["monthly_price"].values)
    #todo Create a value for the remaining balance after paying the recurring expenses
    remaining = balance
    for expense in list_data:
        remaining -= expense
    remaining = round(remaining,2)
    
    if remaining > 0:
        list_names.append("Remaining")
        list_data.append(remaining)
        total = balance
        title = f"Total: {total}"
    else:
        total = df_recurrings["monthly_price"].sum()
        diff = round(total-balance,2)
        title = f"Total expenditures: £{total}\nYour balance: £{balance}\nDifference: £{diff}"
    # Now list_data is final → create explode with matching length
    explode = [0] * len(list_data)
    if remaining > 0:
        explode[-1] = 0.1   # last slice is "Remaining"
    n_slices = len(list_data)          # or whatever your data list is
    colours = sns.color_palette("rocket_r", n_colors=n_slices)
    labels = []
    for price in list_data:
        labels.append(f"£{price}")
    plt.pie(
        list_data, 
        labels=labels,
        colors = colours, 
        startangle=90, 
        counterclock=True,
        explode=explode,
        wedgeprops=dict(width=0.6)
    )
    plt.legend(
        list_names,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.title(title)
    plt.show()
    
balance = display_balance()
print("1) Add income   2) Add expense   3) Add a recurring income source (e.g wage)   4) Add a recurring expense")
print("5) Create a savings folder   6) View savings folders vs balance chart   7) View savings folders")
print("8) Add wage   9) Edit savings folders   10) Edit recurrings   11) View recurring income and expenses")
print("12) View recurrings vs balance chart")
action = input("   >> ")

if action == "1":
    new_transaction("in")
elif action == "2":
    new_transaction("out")
elif action == "3":
    recurrings("in")
elif action == "4":
    recurrings("out")
elif action == "5":
    create_savings_folder()
elif action == "6":
    view_balance_vs_folders_chart()
elif action == "7":
    view_folders()
elif action == "8":
    add_wage()
elif action == "9":
    edit_folders()
elif action == "10":
    edit_recurrents()
elif action == "11":
    view_recurrings()
elif action == "12":
    recurrings_vs_chart()
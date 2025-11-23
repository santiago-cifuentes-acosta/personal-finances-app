# personal-finances-app
Idea for including time meassures into a banking app reflecting Pepe Mujica's quote "when you buy something you don't buy it with money but with the time of your life it took you to earn that money". The app also allows the user to record recurring expenses like gym memberships and savings folders, and to visualise how much money is not compromised

# Personal Finance CLI
A simple command-line personal finance tracker written in Python.  
It lets you record transactions, recurring incomes/expenses, savings folders, and view summary charts using `pandas`, `matplotlib`, and `seaborn`.

## Features
- 💰 **Track transactions**
  - Add income and expenses
  - Records entity, amount, type, notes and running balance

- ⏱ **Optionally track time to earn income**
  - Record how many hours/days/weeks it took to earn a given income
  - Stored as `Timedelta` in a separate CSV

- 🔁 **Recurring incomes & expenses**
  - Define recurring items (weekly / monthly / yearly)
  - Handles wages separately (hourly rate + hours per week)
  - Converts all recurring amounts to monthly equivalents for analysis

- 🎯 **Savings folders**
  - Create named savings “folders” with a target amount
  - Track how much is already saved and how much remains
  - See how many hours of your main wage you need to work to fully fund each folder

- 📊 **Charts**
  - Pie chart of **savings folders + recurring costs vs current balance**
  - Pie chart of **recurring expenses vs balance**
  - Uses `seaborn`’s `rocket_r` palette and some styling

- 🛠 **Editing tools**
  - Edit or delete savings folders
  - Edit recurring items (amount, frequency, reminder, delete)
  - View summaries of recurring incomes/expenses and wages

## How it works
All data is stored in CSV files in the same folder as the .py file:

- `personalfinancetransactions.csv` – all one-off transactions, with running balance  
- `personalfinancesavingsfolders.csv` – savings folders (name, goal amount, saved so far)  
- `personalfinancerecurrings.csv` – recurring incomes/expenses  
- `personalfinancewages.csv` – wages (name, hourly rate, hours per week)  
- `personalfinancetimerecords.csv` – optional time records linked to transactions through the transaction id

The main script, `personalfinance.py`, presents a text menu and executes the selected action.

## Installation
1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/personal-finance-cli.git
   cd personal-finance-cli

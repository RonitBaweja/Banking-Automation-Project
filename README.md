# Banking Automation System

## Overview

The Banking Automation System is a Python-based application that allows users to manage their banking activities, including account creation, balance checking, deposits, withdrawals, transfers, and transaction history. The application uses a graphical user interface (GUI) built with Tkinter and stores user data in an SQLite database.

## Features

- User account creation with unique email, mobile number, and Adhar number.
- User login for both regular users and admin.
- Admin functionalities to create, view, update, and delete user accounts.
- User functionalities to check balance, deposit, withdraw, and transfer funds.
- Transaction history tracking for each user.
- Password recovery feature for users.
- Email notifications for account creation and transactions.

## Technologies Used

- Python 3.12.4
- Tkinter (for GUI)
- SQLite (for database management)
- PIL (Pillow) for image handling
- Gmail API for sending emails
- Regular expressions (re) for input validation

## Installation

    1. Clone the repository:
    
    git clone https://github.com/RonitBaweja/Banking-Automation-Project.git

    2. Install the required packages:
        pip install pillow
        pip install gmail

    3. Ensure you have Python 3.12.4 installed on your machine.


## Usage
    1. Run the application:
        python main.py

    2. Follow the on-screen instructions to create an account or log in.

    3. For admin users, you can manage user accounts through the admin panel.

    4. For regular users, you can perform banking operations such as 
    checking balance, depositing, withdrawing, and transferring funds.

## Database Setup
    The application uses an SQLite database (bank.sqlite) to store user information 
    and transaction records. The database will be created automatically when the 
    application is run for the first time.

## Table Structure
    users: Stores user information including account number, password, name,
    mobile number, email, balance, Adhar number, and account open date.
    
    txn: Stores transaction details including transaction ID, 
    account number, transaction type, date, amount, and updated balance.

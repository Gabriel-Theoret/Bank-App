# Banque ARGA

## Description

Banque ARGA is a bank application simulation developed in Python. The project allows users to interact with a virtual banking system through a graphical interface built with Tkinter or a console interface.

The application uses an SQLite database to store account information, passwords, account balances, and transaction counts.

It also includes an administration interface for managing bank accounts.

## Features

### Client Interface
- Client login using an account number and password
- Account balance display
- Automatic account number assignment
- Initial balance provided when creating an account
- Money transfers between existing accounts
- Transaction counter
- Password recovery using a security phrase

### Administrator Interface
- Administrator login
- View existing bank accounts
- Display account balances
- Delete existing accounts
- Manage available account numbers

### Database
- SQLite database integration
- Automatic database and table creation
- Persistent storage of account information
- Automatic updates to balances after transfers

### Console Interface
- Create a new bank account
- Generate a random account number
- Set and confirm a password
- Choose a security phrase
- Access the login interface

## Technologies Used

- **Python**: Main programming language
- **Tkinter**: Graphical user interface
- **SQLite**: Database management
- **Random**: Account number and initial balance generation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repository
   ```

3. Run the application:

   ```bash
   python bnq121.py
   ```

The SQLite database file `base.db` is automatically created when the application runs.

## Account Information

The application uses predefined account numbers ranging from 101 to 110.

New accounts are assigned an available account number and receive an initial balance generated randomly between $100 and $500.

The administrator login credentials are currently defined in the source code.

## Project Structure

```text
Banque-ARGA/
│
├── bnq121.py
├── base.db
└── README.md
```

## Purpose

This project was developed as a collaborative programming project to practice Python programming, graphical interface development, database integration, and SQL queries.

It provides practical experience with Tkinter and SQLite through the simulation of a basic banking system.

## Disclaimer

This application is an educational simulation. It is not intended for real banking operations or the management of actual financial information.

# Banking App

A simple command-line banking application built with Python and MySQL.

## Features

- User registration and login
- Deposit and withdraw money
- Check account balance
- View transaction history
- Secure database storage

## Prerequisites

- Python 3.7+
- MySQL Server 8.0+
- MySQL Connector/Python

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bank_pj.git
   cd bank_pj
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database:
   - Create a database named `banking_app`
   - Update the `.env` file with your database credentials:
     ```
     DB_HOST=localhost
     DB_USER=your_username
     DB_PASSWORD=your_password
     DB_NAME=banking_app
     DB_PORT=3306
     ```

## Usage

Run the application:
```bash
python bank_app.py
```

Follow the on-screen prompts to:
1. Create a new account or login
2. Deposit/withdraw money
3. Check balance
4. View transaction history

## Database Schema

The app creates two tables:
- `accounts`: Stores user information and balance
- `transactions`: Records all deposit/withdraw operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
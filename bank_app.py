from db_connection import get_db_connection, execute_query, execute_update
from datetime import datetime
import os

class BankingApp:
    def __init__(self):
        self.conn = None
        self.user_id = None
        self.user_name = None
        self.balance = 0.0
        
    def setup_database(self):
        """Initialize database tables for banking app"""
        try:
            # Create tables only if they do not already exist.
            accounts_table = """
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(100) NOT NULL UNIQUE,
                balance DECIMAL(10, 2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            execute_update(self.conn, accounts_table, verbose=False)
            
            transactions_table = """
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_id INT NOT NULL,
                transaction_type VARCHAR(20),
                amount DECIMAL(10, 2),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
            """
            execute_update(self.conn, transactions_table, verbose=False)
        except Exception as e:
            print(f"Error setting up database: {e}")
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        """Display the app title and welcome message"""
        self.clear_screen()
        print("=" * 41)
        print(" " * 14 + "Banking App")
        print("=" * 41)
        print(f"Welcome, {self.user_name}\n")
        print("What would you like to do today?\n")

    
    def display_main_menu(self):
        """Display the main menu"""
        self.display_title()
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Exit")
        print()
    
    def deposit_money(self):
        """Handle deposit transaction"""
        self.display_title()
        try:
            amount = float(input("Enter amount to deposit: $"))
            
            if amount <= 0:
                print("Amount must be greater than 0")
                input("\nPress Enter to continue...")
                return
            
            # Update balance
            new_balance = self.balance + amount
            update_query = "UPDATE accounts SET balance = %s WHERE id = %s"
            execute_update(self.conn, update_query, (new_balance, self.user_id), verbose=False)
            
            # Record transaction
            transaction_query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)"
            execute_update(self.conn, transaction_query, (self.user_id, "DEPOSIT", amount), verbose=False)
            
            self.balance = new_balance
            print(f"\n Successfully deposited ${amount:.2f}")
            print(f"New Balance: ${self.balance:.2f}")
        except ValueError:
            print(" Invalid amount. Please enter a valid number.")
        
        input("\nPress Enter to continue...")
    
    def withdraw_money(self):
        """Handle withdrawal transaction"""
        self.display_title()
        try:
            amount = float(input("Enter amount to withdraw: $"))
            
            if amount <= 0:
                print("Amount must be greater than 0")
                input("\nPress Enter to continue...")
                return
            
            if amount > self.balance:
                print(f"Insufficient balance. Current balance: ${self.balance:.2f}")
                input("\nPress Enter to continue...")
                return
            
            # Update balance
            new_balance = self.balance - amount
            update_query = "UPDATE accounts SET balance = %s WHERE id = %s"
            execute_update(self.conn, update_query, (new_balance, self.user_id), verbose=False)
            
            # Record transaction
            transaction_query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)"
            execute_update(self.conn, transaction_query, (self.user_id, "WITHDRAWAL", amount), verbose=False)
            
            self.balance = new_balance
            print(f"\nSuccessfully withdrew ${amount:.2f}")
            print(f"Remaining Balance: ${self.balance:.2f}")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        
        input("\nPress Enter to continue...")
    
    def check_balance(self):
        """Display current balance"""
        self.display_title()
        print(f"Your current balance is: ${self.balance:.2f}\n")
        input("Press Enter to continue...")
    
    def transaction_history(self):
        """Display transaction history"""
        self.display_title()
        print("Transaction History:")
        print("-" * 60)
        
        query = """
        SELECT transaction_type, amount, transaction_date 
        FROM transactions 
        WHERE account_id = %s 
        ORDER BY transaction_date DESC
        """
        results = execute_query(self.conn, query, (self.user_id,))
        
        if results:
            for row in results:
                trans_type, amount, trans_date = row
                print(f"{trans_type:12} | ${amount:>8.2f} | {trans_date}")
        else:
            print("No transactions found.")
        
        print("-" * 60)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        self.conn = get_db_connection()
        
        if not self.conn:
            print("Failed to connect to database")
            return
        
        # Setup database
        self.setup_database()
        
        # Login or Register
        if not self.login_or_register():
            self.conn.close()
            return
        
        # Main menu loop
        while True:
            self.display_main_menu()
            
            try:
                choice = input("Choose an option: ").strip()
                
                if choice == "1":
                    self.deposit_money()
                elif choice == "2":
                    self.withdraw_money()
                elif choice == "3":
                    self.check_balance()
                elif choice == "4":
                    self.transaction_history()
                elif choice == "5":
                    self.clear_screen()
                    print("=" * 41)
                    print(" " * 10 + "Thank you for using Banking App!")
                    print("=" * 41)
                    break
                else:
                    print("✗ Invalid choice. Please select 1-5.")
                    input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n\n Application interrupted")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("\nPress Enter to continue...")
        
        # Close connection
        self.conn.close()
        print("\nConnection closed")
    
    def login_or_register(self):
        #login or register user
        while True:
            self.clear_screen()
            print("=" * 41)
            print(" " * 14 + "Banking App")
            print("=" * 41)
            print("\n1. Login")
            print("2. Create New Account")
            print("3. Exit")
            print()
            
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                if self.login():
                    return True
            elif choice == "2":
                if self.register():
                    return True
            elif choice == "3":
                self.clear_screen()
                print("Thank you for using Banking App!")
                return False
            else:
                print("Invalid choice. Please select 1-3.")
                input("\nPress Enter to continue...")
    
    def login(self):
        #user login
        self.clear_screen()
        print("=" * 41)
        print(" " * 14 + "Login")
        print("=" * 41)
        print()
        
        username = input("Enter your username: ").strip()
        
        if not username:
            print("Username cannot be empty")
            input("\nPress Enter to continue...")
            return False
        
        # Check if account exists
        query = "SELECT id, balance FROM accounts WHERE user_name = %s"
        result = execute_query(self.conn, query, (username,))
        
        if result:
            self.user_name = username
            self.user_id = result[0][0]
            self.balance = float(result[0][1])
            print(f"\nLogin successful! Welcome, {self.user_name}")
            input("\nPress Enter to continue...")
            return True
        else:
            print("Account not found. Please try again or create a new account.")
            input("\nPress Enter to continue...")
            return False
    
    def register(self):
        #Handle new account registration
        self.clear_screen()
        print("=" * 41)
        print(" " * 14 + "Create New Account")
        print("=" * 41)
        print()
        
        username = input("Enter a username: ").strip()
        
        if not username:
            print("Username cannot be empty")
            input("\nPress Enter to continue...")
            return False
        
        # Check if username already exists
        query = "SELECT id FROM accounts WHERE user_name = %s"
        result = execute_query(self.conn, query, (username,))
        
        if result:
            print("Username already exists. Please choose a different username.")
            input("\nPress Enter to continue...")
            return False
        
        # Create new account with initial balance
        insert_query = "INSERT INTO accounts (user_name, balance) VALUES (%s, %s)"
        success = execute_update(self.conn, insert_query, (username, 0.00), verbose=False)
        
        if success:
            # Fetch the new account
            result = execute_query(self.conn, query, (username,))
            if result:
                self.user_name = username
                self.user_id = result[0][0]
                self.balance = 0.00
                self.clear_screen()
                print("=" * 41)
                print(" " * 14 + "Account Created!")
                print("=" * 41)
                print(f"\n✓ Welcome, {self.user_name}!")
                print(f"Initial Balance: ${self.balance:.2f}")
                input("\nPress Enter to continue...")
                return True
        
        print("Failed to create account. Please try again.")
        input("\nPress Enter to continue...")
        return False


if __name__ == "__main__":
    app = BankingApp()
    app.run()

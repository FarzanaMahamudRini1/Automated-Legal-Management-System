"""
JudgmentCalcNV - Complete Nevada Judgment Management System
Integrates interest calculations with database operations and menu system
"""

import mysql.connector
from datetime import date, datetime
import decimal
import matplotlib.pyplot as plt


DEFAULT_ADDITIONAL_POINTS = 0.0

# Database Connection Functions
def get_database_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def get_database_cursor():
    """Get database cursor"""
    connection = get_database_connection()
    if connection:
        return connection.cursor(), connection
    return None, None

# Interest Calculation Functions
def get_interest_rates():
    """Get predefined interest rates for different liability types"""
    interest_rates = {
        'liability1': 0.05,
        'liability2': 0.08,
        'damages': 0.06,
        'fees': 0.07,
        'costs': 0.05,
        # Add more liability-item interest rates as needed
    }
    return interest_rates

def calculate_total_interest(principal_amount, applicable_interest_rate, start_of_segment, end_of_segment, compounding=True):
    """Calculate total interest for a given period"""
    days_in_segment = (end_of_segment - start_of_segment).days
    
    if compounding:
        total_interest = principal_amount * (1 + applicable_interest_rate / 365) ** days_in_segment - principal_amount
    else:
        total_interest = principal_amount * applicable_interest_rate * (days_in_segment / 365)

    return total_interest

def calculate_simple_interest(principal_amount, interest_rate, start_date, end_date):
    """Calculate simple interest"""
    days_in_period = (end_date - start_date).days
    return principal_amount * interest_rate * (days_in_period / 365)

def calculate_compounding_interest(principal_amount, interest_rate, start_date, end_date, compounding_period):
    """Calculate compound interest"""
    days_in_period = (end_date - start_date).days
    compounding_periods = days_in_period // compounding_period
    total_interest = principal_amount * (1 + interest_rate / 365 / 100) ** compounding_periods - principal_amount
    return total_interest

def update_case_details(case_number, liability_name, principal_amount, start_of_segment, end_of_segment, total_interest, compounding=True):
    """Display calculated interest details"""
    print("\n" + "="*70)
    print(f"INTEREST CALCULATION RESULTS - Case {case_number}")
    print("="*70)
    print(f"Liability: {liability_name}")
    print(f"Principal Amount: ${principal_amount:,.2f}")
    print(f"Interest Rate: {get_interest_rates().get(liability_name, 0.0):.2%}")
    print(f"Start Date: {start_of_segment}")
    print(f"End Date: {end_of_segment}")
    print(f"Days in Period: {(end_of_segment - start_of_segment).days}")
    print(f"Total {'Compounding' if compounding else 'Simple'} Interest: ${total_interest:,.2f}")
    print(f"Total Amount Due: ${principal_amount + total_interest:,.2f}")
    print("="*70)

def save_calculation_to_database(case_number, liability_name, principal_amount, interest_amount, calculation_date):
    """Save interest calculation results to database"""
    cursor, connection = get_database_cursor()
    
    if cursor:
        try:
            # Get case ID
            cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
            case_result = cursor.fetchone()
            
            if case_result:
                case_id = case_result[0]
                
                # Insert calculation record (you might need to create a CALCULATIONS table)
                insert_query = """
                INSERT INTO CALCULATIONS (caseID, liability_name, principal_amount, 
                interest_amount, calculation_date) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (case_id, liability_name, principal_amount, 
                                            interest_amount, calculation_date))
                connection.commit()
                print("Calculation saved to database successfully.")
            else:
                print(f"Case {case_number} not found in database.")
                
        except mysql.connector.Error as err:
            print(f"Error saving calculation: {err}")
        finally:
            cursor.close()
            connection.close()

def calculate_contractual_interest(case_number):
    """Calculate contractual interest with database integration"""
    print(f"\n--- CONTRACTUAL INTEREST CALCULATION FOR CASE {case_number} ---")
    
    # Check if case exists in database
    if not verify_case_exists(case_number):
        print(f"Warning: Case {case_number} not found in database.")
        create_new = input("Would you like to create this case? (yes/no): ").lower()
        if create_new == 'yes':
            create_case_simple(case_number)
        else:
            return
    
    # Collect user input for judgment details
    judgment_date_input = input("Has a judgment been entered? (yes/no): ").lower()
    
    if judgment_date_input == 'yes':
        judgment_date = date.fromisoformat(input("Enter the judgment date (YYYY-MM-DD): "))
    else:
        judgment_date = None

    # Collect additional user input
    interest_type = input("Enter interest type (simple/compounding): ").lower()

    if interest_type not in {'simple', 'compounding'}:
        print("Invalid interest type. Please enter either 'simple' or 'compounding'.")
        return

    try:
        principal_amount = float(input("Enter the principal amount: "))
        start_date = date.fromisoformat(input("Enter the start date (YYYY-MM-DD): "))
        end_date = date.fromisoformat(input("Enter the end date (YYYY-MM-DD): "))
        interest_rate = float(input("Enter the interest rate (as decimal, e.g., 0.08 for 8%): "))
    except ValueError:
        print("Error: Invalid input. Please enter valid numbers and dates.")
        return

    if start_date >= end_date:
        print("Error: Start date must be before end date.")
        return

    # Calculate interest based on user input
    if interest_type == 'compounding':
        compounding_period = int(input("Enter the compounding period (in days): "))
        total_interest = calculate_compounding_interest(principal_amount, interest_rate, start_date, end_date, compounding_period)
    else:
        total_interest = calculate_simple_interest(principal_amount, interest_rate, start_date, end_date)

    # Display the result
    print("\n" + "="*70)
    print("CONTRACTUAL INTEREST CALCULATION RESULTS")
    print("="*70)
    print(f"Case Number: {case_number}")
    print(f"Principal Amount: ${principal_amount:,.2f}")
    print(f"Interest Rate: {interest_rate:.2%}")
    print(f"Interest Type: {interest_type.capitalize()}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Days in Period: {(end_date - start_date).days}")
    print(f"Total Interest: ${total_interest:,.2f}")
    print(f"Total Amount Due: ${principal_amount + total_interest:,.2f}")
    
    if judgment_date:
        print(f"Judgment Date: {judgment_date}")
    
    print("="*70)

    # Ask if user wants to save to database
    save_to_db = input("\nWould you like to save this calculation to the database? (yes/no): ").lower()
    if save_to_db == 'yes':
        save_calculation_to_database(case_number, "contractual", principal_amount, total_interest, datetime.now())
    
    # Ask if user wants visualization
    show_chart = input("Would you like to see a pie chart visualization? (yes/no): ").lower()
    if show_chart == 'yes':
        create_interest_visualization(principal_amount, total_interest, f"Contractual Interest - Case {case_number}")

def calculate_statutory_interest(case_number):
    """Calculate statutory interest with database integration"""
    print(f"\n--- STATUTORY INTEREST CALCULATION FOR CASE {case_number} ---")
    
    # Check if case exists in database
    if not verify_case_exists(case_number):
        print(f"Warning: Case {case_number} not found in database.")
        create_new = input("Would you like to create this case? (yes/no): ").lower()
        if create_new == 'yes':
            create_case_simple(case_number)
        else:
            return
    
    while True:
        # Strip leading and trailing spaces from the entered liability name
        liability_name = input("Enter the name of the liability (or type 'exit' to finish): ").strip().lower()

        if liability_name == 'exit':
            break

        try:
            principal_amount = float(input("Enter the principal amount: "))
            start_of_segment = date.fromisoformat(input("Enter the start date of the segment (YYYY-MM-DD): "))
            end_of_segment = date.fromisoformat(input("Enter the end date of the segment (YYYY-MM-DD): "))
        except ValueError:
            print("Error: Invalid input. Please enter numeric values for the principal amount and valid dates.")
            continue

        if end_of_segment <= start_of_segment:
            print("Error: End date must be after the start date.")
            continue

        interest_rates = get_interest_rates()

        # Check if liability name is valid
        if liability_name not in interest_rates:
            print(f"Available liability types: {', '.join(interest_rates.keys())}")
            print("Error: Invalid liability name. Please enter a valid liability name.")
            continue

        applicable_interest_rate = interest_rates[liability_name]

        additional_points = float(input(f"Enter additional points above the base rate for {liability_name} (default is {DEFAULT_ADDITIONAL_POINTS}): ") or DEFAULT_ADDITIONAL_POINTS)

        compounding_option = input("Choose interest calculation type (C for Compound, S for Simple, default is Compound): ").upper()
        compounding = compounding_option != 'S'  # Default to compound unless 'S' is explicitly chosen

        total_interest = calculate_total_interest(principal_amount, applicable_interest_rate + (additional_points/100), start_of_segment, end_of_segment, compounding)

        update_case_details(case_number, liability_name, principal_amount, start_of_segment, end_of_segment, total_interest, compounding)
        
        # Ask if user wants to save to database
        save_to_db = input("Would you like to save this calculation to the database? (yes/no): ").lower()
        if save_to_db == 'yes':
            save_calculation_to_database(case_number, liability_name, principal_amount, total_interest, datetime.now())
        
        # Ask if user wants visualization
        show_chart = input("Would you like to see a pie chart visualization? (yes/no): ").lower()
        if show_chart == 'yes':
            create_interest_visualization(principal_amount, total_interest, f"Statutory Interest - Case {case_number} - {liability_name}")

def create_interest_visualization(principal_amount, interest_amount, title):
    """Create pie chart visualization of principal vs interest"""
    try:
        labels = ['Principal Amount', 'Interest Amount']
        amounts = [float(principal_amount), float(interest_amount)]
        colors = ['lightblue', 'lightcoral']
        explode = (0, 0.1)  # "explode" the interest slice
        
        plt.figure(figsize=(10, 8))
        plt.pie(amounts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', 
                shadow=True, startangle=90)
        plt.axis('equal')
        plt.title(title, fontsize=14, fontweight='bold')
        
        # Add text box with amounts
        textstr = f'Principal: ${principal_amount:,.2f}\nInterest: ${interest_amount:,.2f}\nTotal: ${principal_amount + interest_amount:,.2f}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error creating visualization: {e}")

# Database Helper Functions
def verify_case_exists(case_number):
    """Check if a case exists in the database"""
    cursor, connection = get_database_cursor()
    
    if cursor:
        try:
            cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error checking case: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    return False

def create_case_simple(case_number):
    """Create a simple case entry"""
    cursor, connection = get_database_cursor()
    
    if cursor:
        try:
            create_date = datetime.now()
            cursor.execute("INSERT INTO CASES (caseNumber, createDate, updateDate) VALUES (%s, %s, %s)", 
                          (case_number, create_date, create_date))
            connection.commit()
            print(f"Case '{case_number}' created successfully.")
            return True
        except mysql.connector.Error as err:
            print(f"Error creating case: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    return False

# Main Application
def main_menu():
    """Display the main menu and handle user choices"""
    
    while True:
        print("\n" + "="*60)
        print("          JUDGMENT MANAGEMENT SYSTEM FOR NEVADA")
        print("="*60)
        print("1.  Calculate Interest")
        print("2.  View Interest Rates")
        print("3.  Database Status Check")
        print("4.  Quit")
        print("="*60)
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                calculate_interest_menu()
            elif choice == '2':
                display_interest_rates()
            elif choice == '3':
                check_database_status()
            elif choice == '4':
                print("Thank you for using Judgment Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def calculate_interest_menu():
    """Interest calculation menu"""
    print("\n--- INTEREST CALCULATION ---")
    case_number = input("Enter the case number: ").strip()
    
    if not case_number:
        print("Case number cannot be empty.")
        return
    
    has_interest = input("Is there interest associated with the liability item? (yes/no): ").lower().strip()
    
    if has_interest == 'yes':
        interest_type = input("Choose interest type (contractual/statutory): ").lower().strip()
        
        if interest_type == 'contractual':
            calculate_contractual_interest(case_number)
        elif interest_type == 'statutory':
            calculate_statutory_interest(case_number)
        else:
            print("Invalid interest type. Please enter either 'contractual' or 'statutory'.")
    else:
        print("No interest associated with the liability item.")

def display_interest_rates():
    """Display available interest rates"""
    print("\n--- AVAILABLE INTEREST RATES ---")
    rates = get_interest_rates()
    
    for liability_type, rate in rates.items():
        print(f"{liability_type.capitalize()}: {rate:.2%}")
    
    print(f"\nDefault additional points: {DEFAULT_ADDITIONAL_POINTS}")

def check_database_status():
    """Check database connection and basic info"""
    print("\n--- DATABASE STATUS CHECK ---")
    
    cursor, connection = get_database_cursor()
    
    if cursor:
        try:
            # Check connection
            cursor.execute("SELECT 1")
            print("✓ Database connection successful")
            
            # Check tables exist
            tables = ['CASES', 'CLIENTS', 'ACCOUNTING', 'INTEREST']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✓ {table} table: {count} records")
                
        except mysql.connector.Error as err:
            print(f"✗ Database error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("✗ Could not connect to database")

# Run the application
if __name__ == "__main__":
    print("Starting Judgment Management System for Nevada...")
    try:
        main_menu()
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Program terminated.")

JudgmentCalcNV - Main Application 
"""

import sys
import os
from datetime import date, datetime

# Simple import since database_config.py is in the same directory
from database_config import get_database_cursor
from interest_calculator import calculate_contractual_interest, calculate_statutory_interest
# ... other imports for your functions


# Import local modules
from config.database_config import get_database_cursor
from interest_calculator import calculate_contractual_interest, calculate_statutory_interest
from case_management import create_case, search_case, update_case, remove_case
from party_management import manage_parties, search_parties
from liability_management import manage_liabilities
from visualization import visualize_case

def main_menu():
    """Display the main menu and handle user choices"""
    
    while True:
        print("\n" + "="*60)
        print("          JUDGMENT MANAGEMENT SYSTEM FOR NEVADA")
        print("="*60)
        print("1.  Create New Case")
        print("2.  Search Case")
        print("3.  Update Case")
        print("4.  Remove Case")
        print("5.  Calculate Interest")
        print("6.  Manage Parties")
        print("7.  Search Parties")
        print("8.  Check Orphaned Entries")
        print("9.  Manage Liabilities")
        print("10. Case Visualization")
        print("11. Quit")
        print("="*60)
        
        try:
            choice = input("Enter your choice (1-11): ").strip()
            
            if choice == '1':
                create_new_case()
            elif choice == '2':
                search_existing_case()
            elif choice == '3':
                update_existing_case()
            elif choice == '4':
                remove_existing_case()
            elif choice == '5':
                calculate_interest_menu()
            elif choice == '6':
                manage_case_parties()
            elif choice == '7':
                search_all_parties()
            elif choice == '8':
                check_orphaned_entries()
            elif choice == '9':
                manage_case_liabilities()
            elif choice == '10':
                visualize_case_data()
            elif choice == '11':
                print("Thank you for using Judgment Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 11.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def create_new_case():
    """Create a new case"""
    print("\n--- CREATE NEW CASE ---")
    case_number = input("Enter case number: ").strip()
    
    if case_number:
        create_case(case_number)
    else:
        print("Case number cannot be empty.")

def search_existing_case():
    """Search for an existing case"""
    print("\n--- SEARCH CASE ---")
    case_number = input("Enter case number to search: ").strip()
    
    if case_number:
        search_case(case_number)
    else:
        print("Case number cannot be empty.")

def update_existing_case():
    """Update an existing case"""
    print("\n--- UPDATE CASE ---")
    case_number = input("Enter case number to update: ").strip()
    
    if case_number:
        update_case(case_number)
    else:
        print("Case number cannot be empty.")

def remove_existing_case():
    """Remove an existing case"""
    print("\n--- REMOVE CASE ---")
    case_number = input("Enter case number to remove: ").strip()
    
    if case_number:
        confirmation = input(f"Are you sure you want to remove case '{case_number}'? (yes/no): ").lower()
        if confirmation == 'yes':
            remove_case(case_number)
        else:
            print("Case removal cancelled.")
    else:
        print("Case number cannot be empty.")

def calculate_interest_menu():
    """Interest calculation menu"""
    print("\n--- CALCULATE INTEREST ---")
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

def manage_case_parties():
    """Manage parties for a case"""
    print("\n--- MANAGE PARTIES ---")
    case_number = input("Enter case number: ").strip()
    
    if case_number:
        manage_parties(case_number)
    else:
        print("Case number cannot be empty.")

def search_all_parties():
    """Search for parties across all cases"""
    print("\n--- SEARCH PARTIES ---")
    first_name = input("Enter first name (or press enter to skip): ").strip()
    last_name = input("Enter last name (or press enter to skip): ").strip()
    
    if first_name or last_name:
        search_parties(first_name, last_name)
    else:
        print("Please provide at least first name or last name for search.")

def check_orphaned_entries():
    """Check for orphaned entries in the database"""
    print("\n--- CHECK ORPHANED ENTRIES ---")
    print("This feature will identify records not linked to any case.")
    
    # Placeholder for orphaned entries functionality
    cursor, connection = get_database_cursor()
    
    if cursor:
        try:
            # Check for orphaned clients
            cursor.execute("""
                SELECT c.* FROM CLIENTS c 
                LEFT JOIN CASES ca ON c.caseID = ca.caseID 
                WHERE ca.caseID IS NULL
            """)
            orphaned_clients = cursor.fetchall()
            
            # Check for orphaned accounting entries
            cursor.execute("""
                SELECT a.* FROM ACCOUNTING a 
                LEFT JOIN CASES ca ON a.caseID = ca.caseID 
                WHERE ca.caseID IS NULL
            """)
            orphaned_accounting = cursor.fetchall()
            
            if orphaned_clients:
                print(f"Found {len(orphaned_clients)} orphaned client entries.")
            if orphaned_accounting:
                print(f"Found {len(orphaned_accounting)} orphaned accounting entries.")
            
            if not orphaned_clients and not orphaned_accounting:
                print("No orphaned entries found.")
                
        except Exception as e:
            print(f"Error checking orphaned entries: {e}")
        finally:
            cursor.close()
            connection.close()

def manage_case_liabilities():
    """Manage liabilities for a case"""
    print("\n--- MANAGE LIABILITIES ---")
    case_number = input("Enter case number: ").strip()
    
    if case_number:
        manage_liabilities(case_number)
    else:
        print("Case number cannot be empty.")

def visualize_case_data():
    """Create visualizations for a case"""
    print("\n--- CASE VISUALIZATION ---")
    case_number = input("Enter case number for visualization: ").strip()
    
    if case_number:
        visualize_case(case_number)
    else:
        print("Case number cannot be empty.")

if __name__ == "__main__":
    print("Starting Judgment Management System for Nevada...")
    try:
        main_menu()
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Program terminated.")

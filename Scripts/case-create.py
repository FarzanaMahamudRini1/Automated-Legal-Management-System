def case_create():
    """Create a new case with party and liability information"""
    print("\n--- CREATE NEW CASE ---")
    
    # Get case number with validation
    while True:
        case_number = input('Enter case number (2 letters, 8-10 characters): ').strip()
        
        if not case_number:
            print("Case number cannot be empty.")
            continue
            
        if not (len(case_number) >= 8 and len(case_number) <= 10 and case_number[:2].isalpha()):
            print("Case number must begin with 2 letters and have 8-10 characters total.")
            continue
        break
    
    # Check if case already exists
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return False
    
    try:
        cursor.execute("SELECT caseNumber FROM CASES WHERE caseNumber = %s", (case_number,))
        existing_case = cursor.fetchone()
        
        if existing_case:
            print(f"Case '{case_number}' already exists.")
            return False
        
        # Add a record to the CASES table
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO CASES (caseNumber, createDate, updateDate) VALUES (%s, %s, %s)",
                       (case_number, current_date, current_date))
        connection.commit()
        print(f"Case '{case_number}' created successfully.")
        
        # Get the last inserted caseID
        cursor.execute("SELECT LAST_INSERT_ID()")
        case_id = cursor.fetchone()[0]
        
        # Ask to add party information
        add_party_info = input('Would you like to add party information? (yes/no): ').lower().strip()
        
        if add_party_info == 'yes':
            while True:
                print("\n--- Adding Party Information ---")
                
                # Get party details
                first_name = input('Enter first name: ').strip()
                if not first_name:
                    print("First name cannot be empty.")
                    continue
                
                last_name = input('Enter last name: ').strip()
                if not last_name:
                    print("Last name cannot be empty.")
                    continue
                
                while True:
                    client_type = input('Enter type (defendant or plaintiff) [default: defendant]: ').strip().lower()
                    if not client_type:
                        client_type = 'defendant'
                    
                    if client_type in ('defendant', 'plaintiff'):
                        break
                    else:
                        print("Type can only be 'defendant' or 'plaintiff'.")
                
                # Insert party into database
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO CLIENTS (firstName, lastName, type, caseID, createDate, updateDate) VALUES (%s, %s, %s, %s, %s, %s)",
                               (first_name, last_name, client_type, case_id, current_date, current_date))
                connection.commit()
                print(f"{client_type.capitalize()} '{first_name} {last_name}' added to the case.")
                
                # Ask to add more parties
                add_more = input('Add another party? (yes/no): ').lower().strip()
                if add_more != 'yes':
                    break
        
        # Ask if they want to add a liability associated with the case
        add_liability = input('\nWould you like to add a liability associated with this case? (yes/no): ').lower().strip()
        
        if add_liability == 'yes':
            while True:
                print("\n--- Adding Liability Information ---")
                
                # Get incurred date with validation
                while True:
                    incurred_date = input('Enter incurred date (YYYY-MM-DD): ').strip()
                    try:
                        datetime.strptime(incurred_date, '%Y-%m-%d')
                        break
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD format.")
                
                # Get amount with validation
                while True:
                    try:
                        amount = float(input('Enter amount: $').strip())
                        if amount <= 0:
                            print("Amount must be greater than 0.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number for the amount.")
                
                description = input('Enter description: ').strip()
                if not description:
                    description = "No description provided"
                
                # Get interest type with validation
                while True:
                    interest_type = input('Enter interest type (contractual or statutory) [default: contractual]: ').strip().lower()
                    if not interest_type:
                        interest_type = 'contractual'
                    
                    if interest_type in ('contractual', 'statutory'):
                        break
                    else:
                        print("Interest type can only be 'contractual' or 'statutory'.")
                
                contractual_interest = None
                
                # Get contractual interest rate if needed
                if interest_type == 'contractual':
                    while True:
                        try:
                            contractual_interest = float(input('Enter contractual interest rate (between 0 and 1, e.g., 0.08 for 8%): ').strip())
                            if 0 <= contractual_interest <= 1:
                                break
                            else:
                                print("Contractual interest should be between 0 and 1.")
                        except ValueError:
                            print("Please enter a valid number for the interest rate.")
                
                # Ask about judgment
                has_judgment = input('Is there a judgment for this liability? (yes/no): ').lower().strip()
                judgment_date = None
                
                if has_judgment == 'yes':
                    while True:
                        judgment_date_input = input('Enter judgment date (YYYY-MM-DD): ').strip()
                        try:
                            judgment_date = datetime.strptime(judgment_date_input, '%Y-%m-%d').date()
                            break
                        except ValueError:
                            print("Invalid date format. Please use YYYY-MM-DD format.")
                
                # Insert liability into database
                cursor.execute("INSERT INTO ACCOUNTING (caseID, type, incurredDate, amount, description, interestType, interest, judgmentDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (case_id, 'liability', incurred_date, amount, description, interest_type, contractual_interest, judgment_date))
                connection.commit()
                print("Liability added to the case successfully.")
                
                # Ask to add another liability
                add_another_liability = input('Add another liability? (yes/no): ').lower().strip()
                if add_another_liability != 'yes':
                    break
        
        print(f"\nCase '{case_number}' creation completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating case: {e}")
        connection.rollback()
        return False
    
    finally:
        cursor.close()
        connection.close()

def search_case():
    """Search for cases by case number"""
    print("\n--- SEARCH CASE ---")
    
    case_number = input('Enter case number (or partial case number) to search: ').strip()
    if not case_number:
        print("Please enter a case number to search.")
        return
    
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return
    
    try:
        # Search for cases using LIKE operator for partial matches
        search_pattern = f"%{case_number}%"
        cursor.execute("SELECT caseID, caseNumber, createDate, updateDate FROM CASES WHERE caseNumber LIKE %s", (search_pattern,))
        cases = cursor.fetchall()
        
        if cases:
            print(f"\nFound {len(cases)} matching case(s):")
            print("-" * 80)
            print(f"{'Case ID':<10} {'Case Number':<15} {'Created':<20} {'Updated':<20}")
            print("-" * 80)
            
            for case in cases:
                case_id, case_num, create_date, update_date = case
                print(f"{case_id:<10} {case_num:<15} {str(create_date):<20} {str(update_date):<20}")
            
            print("-" * 80)
            
            # Ask if user wants to see details for a specific case
            show_details = input('\nWould you like to see details for a specific case? (yes/no): ').lower().strip()
            if show_details == 'yes':
                while True:
                    try:
                        selected_case_id = int(input('Enter the Case ID to view details: ').strip())
                        show_case_details(selected_case_id)
                        break
                    except ValueError:
                        print("Please enter a valid Case ID number.")
        else:
            print(f"No cases found matching '{case_number}'.")
    
    except Exception as e:
        print(f"Error searching cases: {e}")
    
    finally:
        cursor.close()
        connection.close()

def show_case_details(case_id):
    """Show detailed information for a specific case"""
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return
    
    try:
        # Get case information
        cursor.execute("SELECT * FROM CASES WHERE caseID = %s", (case_id,))
        case_info = cursor.fetchone()
        
        if not case_info:
            print(f"Case ID {case_id} not found.")
            return
        
        print(f"\n--- CASE DETAILS FOR CASE ID: {case_id} ---")
        print(f"Case Number: {case_info[1]}")
        print(f"Created: {case_info[2]}")
        print(f"Updated: {case_info[3]}")
        
        # Get parties associated with this case
        cursor.execute("SELECT firstName, lastName, type FROM CLIENTS WHERE caseID = %s", (case_id,))
        parties = cursor.fetchall()
        
        if parties:
            print(f"\nParties ({len(parties)}):")
            for party in parties:
                print(f"  - {party[0]} {party[1]} ({party[2]})")
        else:
            print("\nNo parties associated with this case.")
        
        # Get liabilities associated with this case
        cursor.execute("SELECT incurredDate, amount, description, interestType, interest, judgmentDate FROM ACCOUNTING WHERE caseID = %s", (case_id,))
        liabilities = cursor.fetchall()
        
        if liabilities:
            print(f"\nLiabilities ({len(liabilities)}):")
            for liability in liabilities:
                incurred_date, amount, description, interest_type, interest_rate, judgment_date = liability
                print(f"  - Amount: ${amount:,.2f}")
                print(f"    Description: {description}")
                print(f"    Incurred Date: {incurred_date}")
                print(f"    Interest Type: {interest_type}")
                if interest_rate:
                    print(f"    Interest Rate: {interest_rate:.2%}")
                if judgment_date:
                    print(f"    Judgment Date: {judgment_date}")
                print()
        else:
            print("\nNo liabilities associated with this case.")
    
    except Exception as e:
        print(f"Error retrieving case details: {e}")
    
    finally:
        cursor.close()
        connection.close()

def update_main_menu():
    """Enhanced main menu with case creation and search"""
    while True:
        print("\n" + "="*60)
        print("          JUDGMENT MANAGEMENT SYSTEM FOR NEVADA")
        print("="*60)
        print("1.  Create New Case")
        print("2.  Search Case")
        print("3.  Calculate Interest")
        print("4.  View Interest Rates")
        print("5.  Database Status Check")
        print("6.  Quit")
        print("="*60)
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                case_create()
            elif choice == '2':
                search_case()
            elif choice == '3':
                calculate_interest_menu()
            elif choice == '4':
                display_interest_rates()
            elif choice == '5':
                check_database_status()
            elif choice == '6':
                print("Thank you for using Judgment Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

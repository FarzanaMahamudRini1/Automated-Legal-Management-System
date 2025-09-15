def parties():
    """Manage party information for a case (add, remove, or view)"""
    print("\n--- MANAGE PARTIES ---")
    
    # Get case number
    case_number = input('Enter case number: ').strip()
    if not case_number:
        print("Case number cannot be empty.")
        return
    
    # Get database connection
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return
    
    try:
        # Check if case exists
        cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
        case_result = cursor.fetchone()
        
        if not case_result:
            print(f"Case '{case_number}' not found.")
            return
        
        case_id = case_result[0]
        
        # Ask what action to perform
        print("\nParty Management Options:")
        print("1. Add party")
        print("2. Remove party")
        print("3. View parties")
        print("4. Cancel")
        
        action = input("Select an option (1-4): ").strip()
        
        if action == '1':  # Add party
            print("\n--- ADD PARTY ---")
            
            first_name = input('Enter first name: ').strip()
            if not first_name:
                print("First name cannot be empty.")
                return
            
            last_name = input('Enter last name: ').strip()
            if not last_name:
                print("Last name cannot be empty.")
                return
            
            # Get user type with validation
            while True:
                user_type = input('Enter user type (defendant/plaintiff) [default: defendant]: ').strip().lower()
                if not user_type:
                    user_type = 'defendant'
                
                if user_type in ['defendant', 'plaintiff']:
                    break
                else:
                    print("Invalid user type! Please enter 'defendant' or 'plaintiff'.")
            
            # Add party to database
            from datetime import datetime
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("INSERT INTO CLIENTS (firstName, lastName, type, caseID, updateDate) VALUES (%s, %s, %s, %s, %s)",
                          (first_name, last_name, user_type, case_id, current_date))
            connection.commit()
            print(f"Party '{first_name} {last_name}' ({user_type}) added to case '{case_number}'.")
        
        elif action == '2':  # Remove party
            print("\n--- REMOVE PARTY ---")
            
            # Get all parties for this case
            cursor.execute("SELECT firstName, lastName, type FROM CLIENTS WHERE caseID = %s", (case_id,))
            users = cursor.fetchall()
            
            if not users:
                print(f"No parties found for case '{case_number}'.")
                return
            
            print(f"Parties associated with case '{case_number}':")
            for index, user in enumerate(users, start=1):
                print(f"{index}. {user[0]} {user[1]} ({user[2]})")
            
            # Get user choice
            while True:
                try:
                    user_choice = int(input('Enter the number of the party to remove: ').strip())
                    if 1 <= user_choice <= len(users):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(users)}.")
                except ValueError:
                    print("Please enter a valid number.")
            
            user_to_remove = users[user_choice - 1]
            
            # Confirm removal
            confirm = input(f"Remove party '{user_to_remove[0]} {user_to_remove[1]} ({user_to_remove[2]})'? (yes/no): ").lower().strip()
            
            if confirm == 'yes':
                cursor.execute("DELETE FROM CLIENTS WHERE firstName = %s AND lastName = %s AND type = %s AND caseID = %s",
                              (user_to_remove[0], user_to_remove[1], user_to_remove[2], case_id))
                connection.commit()
                print(f"Removed party: {user_to_remove[0]} {user_to_remove[1]} ({user_to_remove[2]})")
            else:
                print("Party removal cancelled.")
        
        elif action == '3':  # View parties
            print("\n--- VIEW PARTIES ---")
            
            cursor.execute("SELECT firstName, lastName, type FROM CLIENTS WHERE caseID = %s", (case_id,))
            users = cursor.fetchall()
            
            if not users:
                print(f"No parties found for case '{case_number}'.")
            else:
                print(f"Parties associated with case '{case_number}':")
                print("-" * 50)
                print(f"{'#':<3} {'Name':<25} {'Type':<12}")
                print("-" * 50)
                
                for index, user in enumerate(users, start=1):
                    full_name = f"{user[0]} {user[1]}"
                    print(f"{index:<3} {full_name:<25} {user[2]:<12}")
                
                print("-" * 50)
                print(f"Total parties: {len(users)}")
        
        elif action == '4':  # Cancel
            print("Party management cancelled.")
        
        else:
            print("Invalid option selected.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

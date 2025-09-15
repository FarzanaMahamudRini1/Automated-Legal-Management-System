def case_remove():
    """Remove a case and optionally its associated data"""
    print("\n--- REMOVE CASE ---")
    
    # Get case number
    case_number = input('Enter case number to remove: ').strip()
    if not case_number:
        print("Case number cannot be empty.")
        return
    
    # Confirm removal
    confirmation = input(f"Are you sure you want to remove case '{case_number}'? (yes/no): ").lower().strip()
    if confirmation != 'yes':
        print("Case removal cancelled.")
        return
    
    # Ask about removing associated data
    remove_clients = input("Remove associated clients? (yes/no): ").lower().strip() == 'yes'
    remove_liabilities = input("Remove associated liabilities? (yes/no): ").lower().strip() == 'yes'
    
    # Get database connection
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return
    
    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        
        # Check if case exists
        cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
        case_result = cursor.fetchone()
        
        if case_result:
            case_id = case_result[0]
            
            # Remove associated clients if requested
            if remove_clients:
                cursor.execute("DELETE FROM CLIENTS WHERE caseID = %s", (case_id,))
                connection.commit()
                print(f"All clients associated with case '{case_number}' removed.")
            
            # Remove associated liabilities if requested
            if remove_liabilities:
                cursor.execute("DELETE FROM ACCOUNTING WHERE caseID = %s", (case_id,))
                connection.commit()
                print(f"All liabilities associated with case '{case_number}' removed.")
            
            # Remove the case itself
            cursor.execute("DELETE FROM CASES WHERE caseID = %s", (case_id,))
            connection.commit()
            print(f"Case '{case_number}' removed successfully.")
            
        else:
            print(f"Case '{case_number}' not found.")
    
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    
    finally:
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        cursor.close()
        connection.close()

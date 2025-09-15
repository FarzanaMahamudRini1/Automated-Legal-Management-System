def party_search():
    """Search clients by first name, last name, or both"""
    print("\n--- SEARCH PARTIES ---")
    
    # Get search criteria
    search_firstname = input('Enter first name to search (or press Enter to skip): ').strip()
    search_lastname = input('Enter last name to search (or press Enter to skip): ').strip()
    
    # Validate that at least one search parameter is provided
    if not search_firstname and not search_lastname:
        print("Please provide at least one search parameter (first name or last name).")
        return
    
    # Get database connection
    cursor, connection = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return
    
    try:
        # Build query based on provided search parameters
        if search_firstname and search_lastname:
            cursor.execute("SELECT * FROM CLIENTS WHERE firstName LIKE %s AND lastName LIKE %s",
                          (f'%{search_firstname}%', f'%{search_lastname}%'))
        elif search_firstname:
            cursor.execute("SELECT * FROM CLIENTS WHERE firstName LIKE %s", (f'%{search_firstname}%',))
        elif search_lastname:
            cursor.execute("SELECT * FROM CLIENTS WHERE lastName LIKE %s", (f'%{search_lastname}%',))
        
        clients = cursor.fetchall()
        
        if not clients:
            print("No clients found matching the search criteria.")
        else:
            print(f"\nFound {len(clients)} matching client(s):")
            print("-" * 80)
            print(f"{'Client ID':<10} {'Name':<25} {'Type':<12} {'Case Number':<15}")
            print("-" * 80)
            
            for client in clients:
                client_id = client[0]
                first_name = client[1]
                last_name = client[2]
                client_type = client[3]
                case_id = client[4]
                
                # Get the case number for this client
                cursor.execute("SELECT caseNumber FROM CASES WHERE caseID = %s", (case_id,))
                case_result = cursor.fetchone()
                case_number = case_result[0] if case_result else 'Not Found'
                
                full_name = f"{first_name} {last_name}"
                print(f"{client_id:<10} {full_name:<25} {client_type:<12} {case_number:<15}")
            
            print("-" * 80)
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

from database_config import get_database_cursor

def case_remove():
    """
    Remove a case and optionally its associated clients and liabilities.
    """
    print("\n--- REMOVE CASE ---")

    # Prompt for case number
    case_number = input("Enter case number to remove: ").strip()
    if not case_number:
        print("Case number cannot be empty.")
        return

    # Confirm removal
    confirmation = input(f"Are you sure you want to remove case '{case_number}'? (yes/no): ").strip().lower()
    if confirmation != "yes":
        print("Case removal cancelled.")
        return

    # Ask whether to remove associated data
    remove_clients = input("Remove associated clients? (yes/no): ").strip().lower() == "yes"
    remove_liabilities = input("Remove associated liabilities? (yes/no): ").strip().lower() == "yes"

    # Get database connection
    cursor, conn = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return

    try:
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # Check if the case exists
        cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
        case_result = cursor.fetchone()

        if not case_result:
            print(f"Case '{case_number}' not found.")
            return

        case_id = case_result[0]

        # Remove associated clients if requested
        if remove_clients:
            cursor.execute("DELETE FROM CLIENTS WHERE caseID = %s", (case_id,))
            conn.commit()
            print(f"All clients associated with case '{case_number}' removed.")

        # Remove associated liabilities if requested
        if remove_liabilities:
            cursor.execute("DELETE FROM ACCOUNTING WHERE caseID = %s", (case_id,))
            conn.commit()
            print(f"All liabilities associated with case '{case_number}' removed.")

        # Remove the case itself
        cursor.execute("DELETE FROM CASES WHERE caseID = %s", (case_id,))
        conn.commit()
        print(f"Case '{case_number}' removed successfully.")

    except Exception as e:
        print(f"Error removing case: {e}")
        conn.rollback()

    finally:
        # Re-enable foreign key checks and close connection
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        cursor.close()
        conn.close()

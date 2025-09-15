from datetime import datetime
from database_config import get_database_cursor  # Your DB helpers

def case_search():
    """
    Search for cases by partial case number and optional date range.
    """
    print("\n--- SEARCH CASES ---")

    # Prompt for partial case number
    case_number = input("Enter partial case number to search: ").strip()
    if not case_number:
        print("Case number cannot be empty.")
        return

    # Optional date filtering
    use_date_filter = input("Would you like to filter by date range? (yes/no): ").strip().lower()
    start_date = None
    end_date = None

    if use_date_filter == "yes":
        # Get start date
        while True:
            start_date_input = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if not start_date_input:
                break
            try:
                start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")

        # Get end date
        while True:
            end_date_input = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if not end_date_input:
                break
            try:
                end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")

        # Validate date range
        if start_date and end_date and start_date > end_date:
            print("Start date cannot be after end date.")
            return

    # Get database connection
    cursor, conn = get_database_cursor()
    if not cursor:
        print("Database connection failed.")
        return

    try:
        # Build query with optional date filtering
        query = "SELECT * FROM CASES WHERE caseNumber LIKE %s"
        params = ('%' + case_number + '%',)

        if start_date and end_date:
            query += " AND createDate BETWEEN %s AND %s"
            params += (start_date, end_date)
        elif start_date:
            query += " AND createDate >= %s"
            params += (start_date,)
        elif end_date:
            query += " AND createDate <= %s"
            params += (end_date,)

        query += " ORDER BY createDate DESC"

        # Execute query
        cursor.execute(query, params)
        cases = cursor.fetchall()

        if not cases:
            print(f"No matching cases found for '{case_number}'.")
            if start_date or end_date:
                print("Try searching without date filters or with a different date range.")
            return

        # Display results
        print(f"\nFound {len(cases)} matching case(s):")
        print("-" * 80)
        print(f"{'Case ID':<10} {'Case Number':<15} {'Create Date':<20} {'Update Date':<20}")
        print("-" * 80)
        for case in cases:
            case_id, case_num, create_date, update_date = case[:4]
            print(f"{case_id:<10} {case_num:<15} {str(create_date):<20} {str(update_date):<20}")
        print("-" * 80)

    except Exception as e:
        print(f"Error retrieving cases: {e}")

    finally:
        cursor.close()
        conn.close()

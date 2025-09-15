from datetime import datetime as dt
from database_config import get_database_cursor  # Your DB helpers

def update_case_number(case_number=None):
    """
    Update an existing case number.

    Parameters:
        case_number (str): Existing case number to update
    """
    cursor, conn = get_database_cursor()
    if not cursor:
        print("Failed to get database cursor.")
        return

    try:
        # Prompt for case number if not provided
        if not case_number:
            case_number = input("Enter case number to update: ").strip()

        # Fetch the case ID
        cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
        case_id_result = cursor.fetchone()
        if not case_id_result:
            print(f"Case '{case_number}' not found.")
            return
        case_id = case_id_result[0]

        # Prompt for new case number
        new_case_number = input("Enter new case number (2 letters, 8-10 characters): ").strip()
        # Validate new case number
        if not (len(new_case_number) >= 8 and len(new_case_number) <= 10 and new_case_number[:2].isalpha()):
            print("Case number must begin with 2 letters and have 8-10 characters.")
            return

        # Update case
        current_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE CASES SET caseNumber = %s, updateDate = %s WHERE caseID = %s",
            (new_case_number, current_date, case_id)
        )
        conn.commit()
        print(f"Case '{case_number}' updated to '{new_case_number}' with update date {current_date}.")

    except Exception as err:
        print(f"Error updating case: {err}")
    finally:
        cursor.close()
        conn.close()

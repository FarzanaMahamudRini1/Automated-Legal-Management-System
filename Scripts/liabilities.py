from datetime import datetime as dt
from database_config import get_database_cursor  # Your DB helpers

def manage_liabilities(case_number=None, add=False, remove=False, view=False, update_judgment=False):
    """
    Manage liabilities by case number.

    Parameters:
        case_number (str): Case number (2 letters + 8-10 characters)
        add (bool): Add new liabilities
        remove (bool): Remove existing liabilities
        view (bool): View liabilities
        update_judgment (bool): Update judgment date for liabilities
    """
    cursor, conn = get_database_cursor()
    if not cursor:
        print("Failed to get database cursor.")
        return

    try:
        # Prompt for case number if not provided
        if not case_number:
            case_number = input("Enter case number (2 letters, 8-10 characters): ").strip()

        # Validate case number
        if not (len(case_number) >= 8 and len(case_number) <= 10 and case_number[:2].isalpha()):
            print("Invalid case number. It should start with 2 letters and have 8-10 characters.")
            return

        # Get case ID
        cursor.execute("SELECT caseID FROM CASES WHERE caseNumber = %s", (case_number,))
        case_id_result = cursor.fetchone()
        if not case_id_result:
            print(f"Case '{case_number}' not found.")
            return
        case_id = case_id_result[0]

        # --- ADD LIABILITY ---
        if add:
            while True:
                while True:
                    incurred_date = input("Enter incurred date (YYYY-MM-DD): ").strip()
                    try:
                        dt.strptime(incurred_date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD.")
                
                amount = float(input("Enter amount: ").strip())
                description = input("Enter description: ").strip()

                # Interest type
                interest_type = input("Enter interest type (contractual/statutory) [contractual]: ").strip() or "contractual"
                while interest_type.lower() not in ("contractual", "statutory"):
                    print("Interest type must be 'contractual' or 'statutory'.")
                    interest_type = input("Enter interest type (contractual/statutory) [contractual]: ").strip() or "contractual"

                # Contractual interest
                contractual_interest = None
                if interest_type.lower() == "contractual":
                    while True:
                        contractual_interest = float(input("Enter contractual interest (0 to 1): ").strip())
                        if 0 <= contractual_interest <= 1:
                            break
                        print("Contractual interest must be between 0 and 1.")

                # Judgment date
                has_judgment = input("Is there a judgment for this liability? (yes/no): ").strip().lower() == "yes"
                judgment_date = None
                if has_judgment:
                    while True:
                        judgment_input = input("Enter judgment date (YYYY-MM-DD): ").strip()
                        try:
                            judgment_date = dt.strptime(judgment_input, "%Y-%m-%d").date()
                            break
                        except ValueError:
                            print("Invalid date format. Please use YYYY-MM-DD.")

                # Insert liability
                cursor.execute("""
                    INSERT INTO ACCOUNTING
                    (caseID, type, incurredDate, amount, description, interestType, interest, judgmentDate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (case_id, "liability", incurred_date, amount, description, interest_type,
                      contractual_interest, judgment_date))
                conn.commit()
                print("Liability added successfully.")

                add_another = input("Add another liability? (yes/no): ").strip().lower() == "yes"
                if not add_another:
                    break

        # --- REMOVE LIABILITY ---
        if remove:
            cursor.execute("SELECT * FROM ACCOUNTING WHERE caseID = %s", (case_id,))
            liabilities = cursor.fetchall()
            if not liabilities:
                print(f"No liabilities found for case '{case_number}'.")
            else:
                print(f"Liabilities for case '{case_number}':")
                for idx, liab in enumerate(liabilities, 1):
                    print(f"{idx}. ID {liab[0]}, Date {liab[2]}, Amount {liab[3]}, Desc {liab[4]}, Type {liab[5]}")

                choice = int(input("Enter the number of the liability to remove: ").strip())
                if 1 <= choice <= len(liabilities):
                    selected = liabilities[choice - 1]
                    cursor.execute("DELETE FROM ACCOUNTING WHERE accountingID = %s", (selected[0],))
                    conn.commit()
                    print(f"Removed liability ID {selected[0]}")
                else:
                    print("Invalid choice.")

        # --- VIEW LIABILITIES ---
        if view:
            cursor.execute("SELECT * FROM ACCOUNTING WHERE caseID = %s", (case_id,))
            liabilities = cursor.fetchall()
            if not liabilities:
                print(f"No liabilities found for case '{case_number}'.")
            else:
                print(f"Liabilities for case '{case_number}':")
                columns = [desc[0] for desc in cursor.description]
                print("Columns:", columns)
                for liab in liabilities:
                    print(liab)

        # --- UPDATE JUDGMENT DATE ---
        if update_judgment:
            cursor.execute("SELECT * FROM ACCOUNTING WHERE caseID = %s", (case_id,))
            liabilities = cursor.fetchall()
            if not liabilities:
                print(f"No liabilities found for case '{case_number}'.")
            else:
                print(f"Liabilities for case '{case_number}':")
                for idx, liab in enumerate(liabilities, 1):
                    print(f"{idx}. ID {liab[0]}, Date {liab[2]}, Amount {liab[3]}, Desc {liab[4]}, Type {liab[5]}")

                choice = int(input("Enter the number of the liability to update judgment date: ").strip())
                if 1 <= choice <= len(liabilities):
                    selected = liabilities[choice - 1]
                    while True:
                        new_judgment = input("Enter new judgment date (YYYY-MM-DD): ").strip()
                        try:
                            new_judgment_date = dt.strptime(new_judgment, "%Y-%m-%d").date()
                            break
                        except ValueError:
                            print("Invalid date format. Use YYYY-MM-DD.")

                    cursor.execute("UPDATE ACCOUNTING SET judgmentDate = %s WHERE accountingID = %s",
                                   (new_judgment_date, selected[0]))
                    conn.commit()
                    print(f"Updated judgment date for liability ID {selected[0]}")
                else:
                    print("Invalid choice.")

    except Exception as err:
        print(f"Error managing liabilities: {err}")
    finally:
        cursor.close()
        conn.close()

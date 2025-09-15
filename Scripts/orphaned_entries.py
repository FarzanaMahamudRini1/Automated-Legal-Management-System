from datetime import datetime as dt
from database_config import get_database_cursor  # Assuming this is the file you shared

def orphaned_entries(list_entries=False, show_attributes=False, remove_entries=False):
    """
    Manage orphaned entries in CLIENTS and ACCOUNTING tables.

    Parameters:
        list_entries (bool): List orphaned entries without deletion
        show_attributes (bool): Show full attributes of orphaned entries
        remove_entries (bool): Remove orphaned entries after confirmation
    """
    cursor, conn = get_database_cursor()
    if not cursor:
        print("Failed to get database cursor.")
        return

    try:
        # Helper function to fetch orphaned entries
        def fetch_orphans():
            cursor.execute("""
                SELECT c.* 
                FROM CLIENTS c
                LEFT JOIN CASES cs ON c.caseID = cs.caseID
                WHERE cs.caseID IS NULL
            """)
            orphaned_clients = cursor.fetchall()

            cursor.execute("""
                SELECT a.* 
                FROM ACCOUNTING a
                LEFT JOIN CASES cs ON a.caseID = cs.caseID
                WHERE cs.caseID IS NULL
            """)
            orphaned_accounting = cursor.fetchall()

            return orphaned_clients, orphaned_accounting

        orphaned_clients, orphaned_accounting = fetch_orphans()

        # LIST orphaned entries
        if list_entries:
            if not orphaned_clients and not orphaned_accounting:
                print("No orphaned entries found in CLIENTS or ACCOUNTING tables.")
            else:
                print("Orphaned entries found:")
                if orphaned_clients:
                    print("CLIENTS table:")
                    for entry in orphaned_clients:
                        print(f"  - caseID: {entry[0]}")
                if orphaned_accounting:
                    print("ACCOUNTING table:")
                    for entry in orphaned_accounting:
                        print(f"  - caseID: {entry[0]}")

        # SHOW full attributes
        if show_attributes:
            if not orphaned_clients and not orphaned_accounting:
                print("No orphaned entries found in CLIENTS or ACCOUNTING tables.")
            else:
                print("Orphaned entries with full attributes:")
                if orphaned_clients:
                    print("CLIENTS table entries:")
                    for entry in orphaned_clients:
                        print(f"  - {entry}")
                if orphaned_accounting:
                    print("ACCOUNTING table entries:")
                    for entry in orphaned_accounting:
                        print(f"  - {entry}")

        # REMOVE orphaned entries
        if remove_entries:
            if not orphaned_clients and not orphaned_accounting:
                print("No orphaned entries to remove.")
            else:
                # Remove CLIENTS entries
                if orphaned_clients:
                    print("CLIENTS orphaned entries:")
                    for entry in orphaned_clients:
                        print(f"  - caseID: {entry[0]}")
                    confirm = input("Do you want to remove these CLIENTS entries? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        for entry in orphaned_clients:
                            cursor.execute("DELETE FROM CLIENTS WHERE caseID = %s", (entry[0],))
                        conn.commit()
                        print("CLIENTS orphaned entries deleted.")

                # Remove ACCOUNTING entries
                if orphaned_accounting:
                    print("ACCOUNTING orphaned entries:")
                    for entry in orphaned_accounting:
                        print(f"  - caseID: {entry[0]}")
                    confirm = input("Do you want to remove these ACCOUNTING entries? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        for entry in orphaned_accounting:
                            cursor.execute("DELETE FROM ACCOUNTING WHERE caseID = %s", (entry[0],))
                        conn.commit()
                        print("ACCOUNTING orphaned entries deleted.")

    except Exception as err:
        print(f"Error while processing orphaned entries: {err}")
    finally:
        cursor.close()
        conn.close()

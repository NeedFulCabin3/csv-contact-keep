import csv
import sys
from pathlib import Path

CONTACTS_FILE = Path("contacts.csv")
CSV_HEADERS = ["Name", "Phone", "Email", "Notes"]


def load_contacts(file_path: Path) -> list[dict]:
    """Load existing contacts from a CSV file into a list of dictionaries."""
    contacts = []
    if not file_path.exists():
        return contacts

    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
    except (IOError, csv.Error) as err:
        print(f"Warning: Could not read '{file_path}': {err}. Starting fresh.")
    
    return contacts


def save_contacts(file_path: Path, contacts: list[dict]) -> bool:
    """Save the current list of contacts to the CSV file."""
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(contacts)
        return True
    except IOError as err:
        print(f"\n[Error] Failed to save contacts to disk: {err}")
        return False


def add_contact(contacts: list[dict]) -> None:
    """Prompt user for contact details and append to the list."""
    print("\n--- Add New Contact ---")
    name = input("Enter Name: ").strip()
    if not name:
        print("[Error] Name cannot be empty.")
        return

    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()
    notes = input("Enter Notes (optional): ").strip()

    new_contact = {
        "Name": name,
        "Phone": phone,
        "Email": email,
        "Notes": notes
    }

    contacts.append(new_contact)
    if save_contacts(CONTACTS_FILE, contacts):
        print(f"✓ Contact for '{name}' added successfully!")


def view_all_contacts(contacts: list[dict]) -> None:
    """Display all saved contacts in a clean, formatted layout."""
    print("\n--- All Contacts ---")
    if not contacts:
        print("No contacts found.")
        return

    for idx, c in enumerate(contacts, 1):
        print(f"{idx}. {c['Name']}")
        print(f"   Phone : {c.get('Phone', 'N/A')}")
        print(f"   Email : {c.get('Email', 'N/A')}")
        if c.get("Notes"):
            print(f"   Notes : {c['Notes']}")
        print("-" * 25)


def search_contacts(contacts: list[dict]) -> None:
    """Search contacts by name (case-insensitive substring match)."""
    print("\n--- Search Contacts ---")
    if not contacts:
        print("No contacts available to search.")
        return

    query = input("Enter name to search: ").strip().lower()
    if not query:
        print("[Error] Search query cannot be empty.")
        return

    matches = [c for c in contacts if query in c["Name"].lower()]

    if matches:
        print(f"\nFound {len(matches)} match(es):")
        view_all_contacts(matches)
    else:
        print(f"No contacts found matching '{query}'.")


def main() -> None:
    """Main execution loop for the terminal application."""
    contacts = load_contacts(CONTACTS_FILE)

    while True:
        print("\n=== Contact Book CLI ===")
        print("1. View All Contacts")
        print("2. Add Contact")
        print("3. Search Contact")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            view_all_contacts(contacts)
        elif choice == "2":
            add_contact(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("[Error] Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
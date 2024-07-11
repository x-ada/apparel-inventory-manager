import sys
import re
import os
import csv
import pandas as pd
import tabulate as tab

COLUMNS_DICT = {"1": "Item_ID",
                "2": "Item_Name",
                "3": "Category",
                "4": "Material",
                "5": "Color",
                "6": "Sizes",
                "7": "Vendor",
                "8": "Purchase_Price",
                "9": "Sales_Price",
                "10": "Quantity",
                "11": "Total_Value"}

def main():
    # Load inventory from file or create new if none provided
    inventory, file_path = load_file()

    # Display options menu
    options_menu(inventory, file_path)


def load_file():
    # Check if user provided a file path
    file_path = sys.argv[1] if len(sys.argv) > 1 else None

    # If user provided a file path, try to read it as a CSV file
    if file_path:
        try:
            inventory = pd.read_csv(file_path)

            # Get the names of the columns as a set and compare it to the COLUMNS dict converted to a set
            if set(inventory.columns) == set(COLUMNS_DICT.values()):
                print("Inventory successfully imported")
                return inventory, file_path
            else:
                sys.exit("ERROR: The file provided is not properly formatted.")

        except FileNotFoundError:
            sys.exit(f"ERROR: The file {file_path} does not exist.")
        except pd.errors.EmptyDataError:
            sys.exit(f"ERROR: The file {file_path} is empty or contains no valid data.")
        except pd.errors.ParserError:
            sys.exit(f"ERROR: The file {file_path} is not a valid CSV file.")
        except Exception as e:
            sys.exit(f"ERROR: An unexpected error occured: {e}")

    # Create new inventory file if no file provided
    else:
        print("Creating new inventory file...")
        inventory = pd.DataFrame(columns = COLUMNS_DICT.values())

        # Prompt user for new file name
        while True:
            file_path = input("What would you like to name the file? ").strip().lower()

            # Check if file name already exists
            if re.search(r"^[\w]+\.csv$", file_path):
                if os.path.exists(file_path):
                    if input("File already exists. Would you like to overwrite existing file? (y/n): ").strip().lower() != "y":
                        continue
                inventory.to_csv(file_path, index=False)
                return inventory, file_path

            else:
                print("ERROR: Format must be 'filename.csv'")
                continue


def options_menu(inventory, file_path):
    menu_dict = {"1": add_new_item,
                 "2": edit_item,
                 "3": remove_item,
                 "4": view_item,
                 "5": view_inventory}

    while True:
        # Reload inventory to account for changes
        inventory = pd.read_csv(file_path)

        print("\nOptions:\n"
              "1. Add new item\n"
              "2. Edit item\n"
              "3. Remove item\n"
              "4. View item\n"
              "5. View inventory as table\n"
              "x. Exit\n")

        option = input("Select a number: ").strip()

        if option in menu_dict:
            menu_dict[option](inventory, file_path)

        elif option == "x":
            sys.exit("Exiting program...")

        else:
            print("Must select a valid number.")

def add_new_item(inventory, file_path):
    print("Adding new item...")
    item = {}

    for col in COLUMNS_DICT.values():
        if col == "Item_ID":
            while True:
                id = input(f"{col}: ").strip().upper()

                if id in inventory["Item_ID"].values:
                    print("ID already exists.")

                else:
                    item[col] = id
                    break

        elif col in ("Purchase_Price", "Sales_Price"):
            while True:
                try:
                    price = float(input(f"{col}: ").strip())

                    if price >= 0:
                        item[col] = round(price, 2)
                        break
                    else:
                        print("ERROR: Price must be 0 or greater")
                except ValueError:
                    print("ERROR: Price must be a number in format '0.00'.")
        elif col == "Quantity":
            while True:
                try:
                    qty = int(input(f"{col}: ").strip())

                    if qty >= 0:
                        item[col] = qty
                        break

                except ValueError:
                    print("ERROR: Please enter a positive whole number.")

        elif col == "Total_Value":
            item[col] = item["Sales_Price"] * item["Quantity"]
        else:
            item[col] = input(f"{col}: ").strip().upper()

    # Prompt user to save changes
    save = input("Would you like to save changes? (y/n) ").strip().lower()

    if save == "y":
        with open(file_path, "a") as file:
            writer = csv.DictWriter(file, fieldnames = COLUMNS_DICT.values())
            writer.writerow(item)
            print("Changes saved.")

def edit_item(inventory, file_path):
    print("Editing item...")

    item_index = ""

    # Prompt user for item_id and get the index number to use
    while True:

        item_id = input("Enter the item ID: ").strip().upper()

        if item_id in inventory["Item_ID"].values:
            item_index = inventory.index[inventory["Item_ID"] == item_id]
            break
        else:
            print(f"ERROR: No item with ID '{item_id}'")

    # Print information of specified item_id
    while True:
        print("\n", inventory.iloc[item_index], "\n")

        # Prompt user for column name to edit
        edit_column = input("Enter the name of the column to edit or x to exit: ").strip()

        if edit_column == "Item_ID":
            while True:
                new_id = input("Item_ID: ").strip().upper()

                if new_id in inventory["Item_ID"].values:
                    print("ERROR: ID already exists")
                else:
                    inventory.loc[item_index, "Item_ID"] = new_id
                    break

        elif edit_column in ("Purchase_Price", "Sales_Price"):
            while True:
                try:
                    price = float(input(f"{edit_column}: ").strip())

                    if price >= 0:
                        inventory.loc[item_index, edit_column] = round(price, 2)
                        break
                    else:
                        print("ERROR: Price must be 0 or greater")

                except ValueError:
                    print("ERROR: Price must be a number in format '0.00'.")

        elif edit_column == "Quantity":
            while True:
                try:
                    qty = int(input(f"{edit_column}: ").strip())

                    if qty >= 0:
                        inventory.loc[item_index, "Quantity"] = qty
                        break

                except ValueError:
                    print("ERROR: Please enter a positive whole number.")

        elif edit_column == "Total_Value":
            print("ERROR: Can not edit a calculated field\n")

        elif edit_column in COLUMNS_DICT.values():
            inventory.loc[item_index, edit_column] = input(f"{edit_column}: ").strip().upper()

        elif edit_column == "x":
            save = input("Would you like to save changes? (y/n) ")

            if save == "y":
                inventory.to_csv(file_path, index = False)
                print("Changes saved.")
            break


def remove_item(inventory, file_path):
    print("Removing item...")

    while True:
        item_id = input("Enter the item ID or x to exit: ").upper()

        try:
            if item_id in inventory["Item_ID"].values:

                # Get the item index from the item id
                item_index = inventory.index[inventory["Item_ID"] == item_id]

                print("\n", inventory.iloc[item_index], "\n")

                while True:
                    remove = input(f"Confirm removal of item {item_id}? (y/n) ").strip().lower()

                    if remove == "y":
                        inventory = inventory.drop(item_index)
                        print(f"Item {item_id} successfully removed.\n")
                        break
                    elif remove == "n":
                        print("Removal cancelled.\n")
                        break
                    else:
                        print("ERROR: Invalid input. Must enter 'y' or 'n'.\n")

            elif item_id == "X":
                save = input("Would you like to save changes? (y/n) ").strip().lower()

                if save == "y":
                    inventory.to_csv(file_path, index = False)
                    print("Changes saved.\n")
                break

            else:
                print("ERROR: Invalid item ID.\n")

        except Exception:
            print("ERROR: An unexpected error occured. Please try again.")

def view_item(inventory, file_path):
    print("Viewing item...")

    while True:
        item_id = input("Enter the item ID or x to exit: ").upper()

        if item_id in inventory["Item_ID"].values:

            item_index = inventory.index[inventory["Item_ID"] == item_id]
            print("\n", inventory.iloc[item_index], "\n")

        elif item_id == "X":
            break
        else:
            print(f"ERROR: No item with ID {item_id}.")

def view_inventory(inventory, file_path):
    print("\nViewing tabular inventory...")
    table = False

    while True:
        print("Tabular Inventory Menu:\n",
              "1. Create/Reset Table\n",
              "2. Sort Table\n")

        option = input("Select a number or x to exit: ").strip().lower()

        if option == "1":
            table_file_path = file_path.replace(".csv", ".txt")

            if os.path.exists(table_file_path):
                overwrite = input(f"The file {table_file_path} already exists. Would you like to overwrite it? (y/n) ").strip().lower()
                if overwrite != "y":
                    while True:
                        table_file_path = input("Enter a new file name for the table ending in '.txt': ").strip().lower()

                        if os.path.exists(table_file_path):
                            print("ERROR: File name already exists.")
                        elif re.search(r"^[\w]+\.txt$", table_file_path):
                            break

            with open(table_file_path, "w") as file:
                file.write(tab.tabulate(inventory, headers = COLUMNS_DICT.values(), tablefmt = "grid", showindex = False))
                print(f"Table saved to file {table_file_path}\n")
                table = True

        elif option == "2":
            if table == False:
                print("ERROR: Must create table or reset existing before sorting.")
                break

            selected_columns = []
            selected_columns_names = []

            while True:

                # Display sorting options menu
                print("\nSorting Options: ")

                for col in COLUMNS_DICT:
                    print(f"{col}. {COLUMNS_DICT[col]}")

                print(f"\nSelected Columns: {selected_columns_names}")

                sort = input("\nSelect columns to sort by entering the number one by one.\nPress x to execute sorting or exit: ").strip()

                if sort in COLUMNS_DICT and sort not in selected_columns:
                    selected_columns.append(sort)
                    selected_columns_names.append(COLUMNS_DICT[sort])
                elif sort.lower() == "x":
                    if not selected_columns:
                        print("Exiting sorting...")
                        break
                    else:

                        print(f"Sorting by {selected_columns_names}...")

                        try:
                            sorted_inventory = inventory.sort_values(by=selected_columns_names)

                            with open(table_file_path, "w") as file:
                                file.write(tab.tabulate(sorted_inventory, headers=COLUMNS_DICT.values(), tablefmt="grid", showindex=False))
                                print(f"Sorted table saved to file {table_file_path}\n")

                        except Exception:
                            print("ERROR: An unexpected error occured")
                        break
                else:
                    print("ERROR: Invalid option or already selected")

        elif option == "x":
            break

if __name__ == "__main__":
    main()

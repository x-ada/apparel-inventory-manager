# Apparel Retail Inventory Manager

## [Video Demo](https://www.youtube.com/watch?v=oC1Okrxd0eY)
## Description:
This program was created as my final project for CS50P. 

The program creates an inventory file and displays a menu that allows the user to add a new item to their inventory, edit, remove, or view an existing item, or view the overall inventory as a table using different sorting methods. The user may also input a csv file in the command-line to interact with an existing inventory file.

## Libraries:
This program requires the following libraries for these usages:

sys: This module allows for command-line arguments and exits the program if an error occurs.

os: This module checks if a file already exists.

regex: This module checks if the user inputed a csv and txt file.

csv: This module allows for a dictionary to be written as a row in a csv file.

pandas: This module allows for dataframe creation and modification, as well as raises dataframe-related errors.

tabulate: This module formats data into a tabular format for easier visualization.

## Installing Libraries:

The required libraries can be installed by simply running the following command:
```pip install -r requirements.txt```

## Functions:
The program includes 7 functions, excluding main.

#### load_file()
This function checks if the user provided a command-line argument. If yes, the argument is assigned to the file_path variable. The function attempts to read the file_path as a csv file and creates a dataframe from it. If successful, the inventory dataframe and file path are returned, otherwise an error message occurs and the program exits. If no argument is provided, a new inventory dataframe and file are created and the user is prompted to name the file. The inventory dataframe and file path are returned.

#### options_menu()
This function displays a menu with numbers correlating to the possible actions that can be taken on the inventory. The user is prompted to input a number and if it's a valid option, the respective function will be called.

#### add_new_item()
The user is prompted to input values for each column in the inventory dataframe. Columns such as "Purchase_Price" and "Sales_Price" must be non-negative numbers 0 or greater. The user is then prompted to save changes to the file or exit the function.

#### edit_item()
The user is prompted to enter the item ID for the item they intend to edit. An error occurs if the ID doesn't exist, otherwise the row with the specified item ID is printed and the user is prompted to enter the column name for the respective value to edit. The user is prommpted to input the new value and if valid, the user is prompted to save changes to the file or exit the function.

#### remove_item()
The user is prompted to enter the item ID of the item they intend to remove from the dataframe. An error occurs if the ID doesn't exist; otherwise, the row with the specified item ID is printed and the user is prompted to confirm if they want to remove the item and save changes.

#### view_item()
The user is prompted to enter the item ID of the item they want to view. An error occurs if the ID doesn't exist; otherwise the row with the specified item ID is printed. The user is then reprompted to enter an item ID or exit the function.

#### view_inventory()
This function prints a menu of options with 1 corresponding to "Create/Reset Table" and 2 for "Sort Table" and prompts the user to select an option. For option 1, a txt file is created, using the same name as the csv file from file_path but replacing "csv" with "txt". If the file already exists, the user is prompted to overwrite the file or rename it. A table is created from the dataframe and written to the new file, and the user is redirected to the view_inventory() menu. For option 2, an error is displayed if the user has not run option 1 before selecting option 2. If a table has already been created through option 1, the user is prompted with a menu of numbered options corresponding to the column names of the dataframe. The user is prompted to enter the columns they want to sort the table by one after another, and the sort is executed when the user enters "x".

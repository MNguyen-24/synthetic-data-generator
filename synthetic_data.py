import random # Importing random for when we need to roll random values
import csv # Importing csv for reading and writing to CSV files

# The read_csv method is used to read from the Fictional_Customers.csv file and return the data rows
def read_csv():
    rows = [] # Initializing the rows list
    with open("Fictional_Customers.csv", "r", newline="") as csvfile: # Opening the file
        reader = csv.reader(csvfile, delimiter=",") # Reading the csv file using the csv library

        # For every row in the csv file, we apppend it to the rows list
        for row in reader:
            rows.append(row)
    return rows # Return the rows list data

# The separate_headers_from_row_data method splits the column headers from the rest of the row data and returns them as a tuple
def separate_headers_from_row_data(rows):

    # Initializing the headers and row_data lists
    headers = []
    row_data = []

    headers = rows[0] # The column headers are the first row in the rows from the csv file

    # We loop through the rows starting from the second element (the first one was the column headers, so that does not count)
    # Loop starts from index 1 instead of the default 0
    for i in range(1, len(rows)):
        row_data.append(rows[i]) # We append the row to the row_data list

    return (headers, row_data) # We return the column headers and row data as a tuple

# The convert_rows_to_columns method converts the data from rows format, to columns format, by using a dictionary
# where the column header name is the key for all the column values
def convert_rows_to_columns(headers, row_data):
    column_data = {} # Initializing the column_data dictionary

    # Initializing the key values for each header name in the column_data dictionary to an empty list
    for header in headers:
        column_data[header] = []
    
    # We loop through every row in row_data to get each individual row
    for row in row_data:
        # We then loop through the number of headers, where i is the index of the header we are working on
        for i in range(len(headers)):
            # We set the current header (the key) at index i and the value at the current row, for its current adjacent header at index i
            key = headers[i]
            value = row[i]

            # We append the current value to the column_data dictionary, by using the current adjacent header as the key
            column_data[key].append(value)

    return column_data # We return the column_data dictionary containing all our values in column format

# The get_distinct_column_values method takes our current column_data dictionary and removes all duplicate values for each key value pair
def get_distinct_column_values(column_data):
    # Initialize a variable by setting it to the current column_data to modify the data safely
    distinct_column_data = column_data
    
    # We loop through each key-value pair in the column_data dictionary
    for key, value in column_data.items():
        distinct_column_data[key] = list(set(value)) # We convert the current value to a set to remove duplicate values, then back to a list to preserve the list type
    return distinct_column_data # We return the distinct column values, in the same format as before


# The is_valid_integer method, validates the user input by checking if the input_string is an integer, and if the value is greater than 0
# It returns False if not an integer or if the input_string is less than or equal to 0. Returns True in all other cases.
def is_valid_integer(input_string):
  try:
    validated_integer = int(input_string) # If this fails, it means the value is not an Integer, so it will trigger a ValueError

    # If the value is less than or equal to 0, the method returns False
    if validated_integer <= 0:
        print(input_string + " is smaller than or equal to 0! The minimum value is 1!")
        return False
  except ValueError: # If there is a ValueError, the input is invalid, so return False
    print(input_string + " is not an integer!")
    return False
  
  return True # If all above works out, then the input is a valid Integer

# The ask_user_for_number_of_records_and_validate method asks the user for how many records they'd like to roll using the sample data, then uses the is_valid_integer method
# to validate the input. If the input is not valid, then it re-prompts the user to try again
def ask_user_for_number_of_records_and_validate():
    userInput = input("How many records would you like to roll? The number must be greater than 0! ")

    if is_valid_integer(userInput): # Checks if the user input is valid
        # If the input is valid, it returns the input as an integer
        numOfRecords = int(userInput)
        return numOfRecords
    
    # If the input is not valid, then it reprompts the user
    return ask_user_for_number_of_records_and_validate()

# The roll_randoms method synthesizes new data by rolling random choices from the existing column data, depending on the number of record requested
def roll_randoms(headers, distinct_column_data, num_of_records):

    # We initialize the rolled_randoms list which is our output data rows
    rolled_randoms = []
    # We initialize the num_of_columns value which is the total number of columns (based on the column header count)
    num_of_columns = len(headers)
    
    # We loop for however many records the user requested
    for i in range(num_of_records):

        current_row = [] # we initialize the current_row list as an empty list 
        
        # We loop through every column by using index j
        for j in range(num_of_columns):
            # Here we will roll a random value given the distinct_column_data dictionary choices
            key = headers[j] # First we set the key to the current header name at index j
            list_of_roll_choices = distinct_column_data[key] # We then get the list of choices using the key

            # We then use the random.choice() method to select a random value from the list of roll choices for this current column
            rolled_value = random.choice(list_of_roll_choices)
            # We append the random rolled_value to the current row and continue the loop to repeat for the rest of the columns in this row
            current_row.append(rolled_value)
        # Once the current row has been filled, we append it to the rolled_randoms list, and start over for the next row
        rolled_randoms.append(current_row)

    return rolled_randoms # We return the newly formed data rows

# The write_csv_synthetic_data method takes the headers and newly formed rolled_data list and writes them all to the rolled_data.csv file in proper row format
def write_csv_synthetic_data(headers, rolled_data):
    # Firstly, we combine the headers row with the rolled_data rows and we insert the headers first 
    rows = [headers] + rolled_data

    # We open the rolled_data.csv file for writing and give the file the variable name csv_output_file
    with open('rolled_data.csv', 'w', newline='') as csv_output_file:
        csv_writer = csv.writer(csv_output_file) # We initialize the csv writer to use the csv_output_file
        csv_writer.writerows(rows) # We write all our data rows to the rolled_data.csv file by using the writerows() method of the csv library

# The main method
def main():

    # We first read the CSV file
    print("Reading CSV File...")
    rows = read_csv()

    # We then Separate the headers from the row data
    print("Separating Column Headers and Data Rows...")
    (headers, row_data) = separate_headers_from_row_data(rows)

    # We convert the data from rows format to columns format (which now uses a dictionary)
    print("Converting Data Rows from row format to column format")
    column_data = convert_rows_to_columns(headers, row_data)

    # We remove all duplicate data for each column so we can have the data be distinct and unique
    print("\nGetting Distinct Column Values and their Counts\n")
    distinct_column_data = get_distinct_column_values(column_data)

    # We print out all the possible distinct values, as well as the counts for each column header key
    for key, value in distinct_column_data.items():
        print("Distinct \"" + key + "\" values (" + str(len(value)) + " values)\n" + str(value) + "\n")
    
    # We ask the user how many records they'd like to roll
    num_of_records = ask_user_for_number_of_records_and_validate()

    # We roll the random data
    print("Rolling Random Data...\n")
    rolled_data = roll_randoms(headers, distinct_column_data, num_of_records)

    # We write the newly synthesized rolled_data into the rolled_data.csv file
    print("Writing Rolled Data to rolled_data.csv ...\n")
    write_csv_synthetic_data(headers, rolled_data)

    return 0


main()

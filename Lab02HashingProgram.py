# Author: Ryan LaCroix
# Date: 02/08/2026
# Description: This program generates a hash table for all files in a user-specified directory
#              and saves it to a .json file. It can also verify the integrity of the files by comparing
#              their current hashes to the stored hashes in the .json file.
# Course: ITIS 3200: Intro to Privacy and Security

import hashlib
import os
import json

# Calculates the cryptographic hash of a file's contents.
def hash_file(file_path):
    hash_obj = hashlib.sha256() # Create a SHA-256 hash object
    with open(file_path, 'rb') as file: # Open the file in binary mode
        digest = hashlib.sha256(file.read()).hexdigest() # Read the file and compute its hash
    return digest # Return the computed hash

# Navigates to the directory entered by the user and calls the hash_file function.
def traverse_directory(directory):
    file_hashes = [] # Array to store a dictionary for each file. Dictionary has filepath and hash.
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.") # Check if the directory exists and print an error message if it does not.
        return file_hashes # Return an empty list if the directory does not exist

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file) # Get the full file path
            file_hashes.append({"filepath": file_path, "hash": hash_file(file_path)}) # Store the file path and its hash in the list
    return file_hashes

# Calls the traverse_directory function, takes the hashes generated and outputs a 
# .json file containing filepath and hash. Returns "Hash table generated" to the console.
def generate_table():

    directory = input("Enter the directory path to generate the hash table: ")
    # Call the traverse_directory function to get the file paths and their hashes
    file_hashes = traverse_directory(directory)
    # Outputs the file paths and their hashes to the .json file within the same directory as the program
    try:
        with open('hash_table.json', 'w') as json_file:
            json.dump(file_hashes, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the JSON file: {e}")
        return
    
    print("Hash table generated.")

# Read from generated .json hash table, traverse the directory again, and 
# compare the newly generated hashes to the ones in the .json file.
# Returns "filepath hash is valid" or "filepath hash is invalid" to the console for each file.
# Return a message to console if a new file has been added or if a file was deleted.
def validate_hashes():
    # Load the existing hash table from the .json file
    try:
        with open('hash_table.json', 'r') as json_file:
            stored_hashes = json.load(json_file)
    except FileNotFoundError:
        print("Hash table file not found. Please generate a hash table first.")
        return

    directory = input("Enter the directory path to verify the hashes: ")
    # Call the traverse_directory function to get the current file paths and their hashes
    current_hashes = traverse_directory(directory)

    stored_hash_dict = {}
    current_hash_dict = {}
    for dictionary in stored_hashes:
        stored_hash_dict.update({dictionary['filepath']: dictionary['hash']}) # Create a dictionary from the stored hashes for easy lookup
    for dictionary in current_hashes:
        current_hash_dict.update({dictionary['filepath']: dictionary['hash']}) # Create a dictionary from the current hashes for easy lookup

    # Check for new files and file name changes
    # Check for deleted files
    # Check hash validity for existing files
    for stored_file_path, stored_hash in stored_hash_dict.items():
        if stored_file_path not in current_hash_dict:
            # First check to see if file name changed.
            if (stored_hash in current_hash_dict.values()):
                new_file_path = next(key for key, value in current_hash_dict.items() if value == stored_hash) # Get the new file path that has the same hash as the stored file
                print(f"File name change detected, {stored_file_path.split('/')[-1]} has been renamed to {new_file_path.split('/')[-1]}.") # Print a message indicating that a file name change has been detected, showing the old and new file names.
            else:
                print(f"File deleted: {stored_file_path}")
        elif current_hash_dict[stored_file_path] == stored_hash:
            print(f"{stored_file_path} hash is valid.")
        else:
            print(f"{stored_file_path} hash is invalid.")

# Handles the user input, calls functions, and outputs the results to the console.
# User options: 1. Generate a new hash table, 2. verify hashes, 3. exit the program.
def main():

    print("Welcome to the Hashing Program!")
    while True:
        print("\nPlease select an option:")
        print("1. Generate a new hash table")
        print("2. Verify hashes")
        print("3. Exit the program")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            generate_table()
        elif choice == '2':
            validate_hashes()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
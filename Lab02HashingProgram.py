# Author: Ryan LaCroix
# Date: 02/08/2026
# Description:
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
    with open('hash_table.json', 'r') as json_file:
        existing_hashes = json.load(json_file)

    directory = input("Enter the directory path to verify the hashes: ")
    # Call the traverse_directory function to get the current file paths and their hashes
    current_hashes = traverse_directory(directory)

    # Compare the current hashes with the existing hashes. Check for new files.
    existing_hash_dict = {item['filepath']: item['hash'] for item in existing_hashes}
    current_hash_dict = {item['filepath']: item['hash'] for item in current_hashes}

    # Check each file in the current hash dictionary
    for file_path, current_hash in current_hash_dict.items():
        if file_path not in existing_hash_dict:
            print(f"File added: {file_path}")
        elif existing_hash_dict[file_path] == current_hash:
            print(f"{file_path} hash is valid.")
        else:
            print(f"{file_path} hash is invalid.")

    # Check for deleted files
    for file_path in existing_hash_dict:
        if file_path not in current_hash_dict:
            print(f"File deleted: {file_path}")

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
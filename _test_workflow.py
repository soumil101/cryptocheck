import os

def write_hello_to_file():
    file_path = "data/_test.txt"
    
    try:
        with open(file_path, "a") as file:
            file.write("Hello\n")
        print("Successfully wrote 'Hello' to the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_goodbye_to_file():
    file_path = "data/_test.txt"
    
    try:
        with open(file_path, "a") as file:
            file.write("Goodbye\n")
        print("Successfully wrote 'Goodbye' to the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to write "Hello" to the file
if __name__ == "__main__":
    write_hello_to_file()
    write_goodbye_to_file()
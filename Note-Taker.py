import os
import webbrowser
import requests

def create_note():
    """Create a new note."""
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    with open(f"{title}.bin", "wb") as file:
        file.write(content.encode('utf-8'))
    print(f"Note '{title}' has been created.")

def view_note():
    """View an existing note."""
    title = input("Enter note title: ")
    try:
        with open(f"{title}.bin", "rb") as file:
            content = file.read().decode('utf-8')
            print(f"Note '{title}':\n{content}")
    except FileNotFoundError:
        print(f"Note '{title}' does not exist.")

def delete_note():
    """Delete an existing note."""
    title = input("Enter note title: ")
    try:
        os.remove(f"{title}.bin")
        print(f"Note '{title}' has been deleted.")
    except FileNotFoundError:
        print(f"Note '{title}' does not exist.")

def cache_data():
    """Cache data from the default browser."""
    url = input("Enter URL to cache: ")
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        with open("cached_data.bin", "wb") as file:
            file.write(content)
        print("Data has been cached.")
    else:
        print(f"Error caching data: {response.status_code}")

def main():
    """Main function."""
    while True:
        print("Note Taker Menu:")
        print("1. Create a new note")
        print("2. View an existing note")
        print("3. Delete an existing note")
        print("4. Cache data from default browser")
        print("5. Quit")
        choice = input("Enter choice (1-5): ")
        if choice == "1":
            create_note()
        elif choice == "2":
            view_note()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            cache_data()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

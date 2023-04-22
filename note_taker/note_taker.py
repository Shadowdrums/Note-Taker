import os
import webbrowser
import requests
import appdirs
from time import sleep
from cryptography.fernet import Fernet


class NoteTaker:
    def __init__(self):
        self.appdata_dir = appdirs.user_data_dir("note-taker", "shadowdrums")
        if not os.path.isdir(os.path.split(self.appdata_dir)[0]):
            os.mkdir(os.path.split(self.appdata_dir)[0])
        if not os.path.isdir(self.appdata_dir):
            os.mkdir(self.appdata_dir)

        self.key_file_path = os.path.join(self.appdata_dir, "key.bin")
        if os.path.isfile(self.key_file_path):
            with open(self.key_file_path, "rb") as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file_path, "wb") as file:
                file.write(self.key)

    def build_notes_path(self, filename):
        """Return the absolute path of a note file."""
        return os.path.join(self.appdata_dir, filename)

    def get_note_names(self):
        """Return a list of note filenames."""
        filenames = []
        for item in os.listdir(self.appdata_dir):
            if os.path.isfile(os.path.join(self.appdata_dir, item)) and item.endswith('.bin'):
                filenames.append(item)
        return filenames

    def list_notes(self):
        """List all available notes."""
        note_names = self.get_note_names()
        if note_names:
            print("Available notes:")
            for note in note_names:
                print(f" - {note[:-4]}")
        else:
            print("No notes found.")

    def create_note(self):
        """Create a new note."""
        title = input("Enter note title: ")
        content = input("Enter note content: ")
        f = Fernet(self.key)
        encrypted_content = f.encrypt(content.encode("utf-8"))
        with open(self.build_notes_path(f"{title}.bin"), "wb") as file:
            file.write(encrypted_content)
        print(f"Note '{title}' has been created.")

    def view_note(self):
        """View an existing note."""
        title = input("Enter note title: ")
        try:
            with open(self.build_notes_path(f"{title}.bin"), "rb") as file:
                encrypted_content = file.read()
                f = Fernet(self.key)
                content = f.decrypt(encrypted_content).decode("utf-8")
                print(f"Note '{title}':\n{content}")
        except FileNotFoundError:
            print(f"Note '{title}' does not exist.")

    def delete_note(self):
        """Delete an existing note."""
        title = input("Enter note title: ")
        try:
            os.remove(self.build_notes_path(f"{title}.bin"))
            print(f"Note '{title}' has been deleted.")
        except FileNotFoundError:
            print(f"Note '{title}' does not exist.")

    def cache_data(self):
        """Cache data from the default browser."""
        url = input("Enter URL to cache: ")
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            with open(self.build_notes_path("cached_data.bin"), "wb") as file:
                file.write(content)
            print("Data has been cached.")
        else:
            print(f"Error caching data: {response.status_code}")

    def menu(self):
        """Display the menu and handle user input."""
        sleep(1)
        print("""
Note Taker Menu:
----------------
1. Create a new note
2. List saved notes
3. View an existing note
4. Delete a saved note
5. Cache data from default browser
6. Quit
        """)
        choice = input("Enter choice (1-6): ")
        if not choice.isdigit() or len(choice) != 1 and int(choice) not in range(1, 7):
            print("Invalid choice.")
        elif choice == "1":
            self.create_note()
        elif choice == "2":
            self.list_notes()
        elif choice == "3":
            self.view_note()
        elif choice == "4":
            self.delete_note()
        elif choice == "5":
            self.cache_data()
        elif choice == "6":
            print("Thank you for using NoteTaker. Goodbye!")
            return
        return self.menu()

if __name__ == "__main__":
    note_taker = NoteTaker()
    note_taker.menu()

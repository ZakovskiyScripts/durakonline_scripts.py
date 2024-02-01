import random
import sys
import math
import threading
import time
from durakonline import durakonline
from datetime import datetime
import base64
import tkinter
import tkinter.messagebox
import customtkinter


FILE_DIRECTORY: str = "" # tokens.txt directory
IMG_DIRECTORY: str = "" # image directory
DEBUG_MODE: bool = False # Debug
REMOVE_INVALID_ACCOUNTS: bool = False

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    tokens: [str] = []
    accounts: [durakonline.Client] = []

    def __init__(self):
        super().__init__()

        self.title("Tools")
        self.geometry(f"{350}x{350}")
        self.resizable(False, False)

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)

        self.nicknames =[] # Enter your random nick here

        self.authbutton = customtkinter.CTkButton(master=self,text="Authorizate",command=self.authorization_accounts, width=5)
        self.authbutton.grid(row=5, column=1, padx=(20, 20), pady=(20, 20))

        self.get_info = customtkinter.CTkButton(master=self,text="Get info",command=self.get_account_info, corner_radius=8)
        self.get_info.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.nickbtn = customtkinter.CTkButton(master=self,text="Random nick",command=self.random_nickname, corner_radius=8)
        self.nickbtn.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.nickenter = customtkinter.CTkButton(master=self, text="Enter nick", command=self.nickname_enter, corner_radius=8)
        self.nickenter.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.update_avatar = customtkinter.CTkButton(master=self, text="Update avatar", command=self.update_avatar, corner_radius=8)
        self.update_avatar.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.del_reqs = customtkinter.CTkButton(master=self, text="Delete requests", command=self.delete_requests, corner_radius=8)
        self.del_reqs.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.del_friends = customtkinter.CTkButton(master=self, text="Delete requests", command=self.delete_friends, corner_radius=8)
        self.del_friends.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.get_frlist = customtkinter.CTkButton(master=self, text="Get friend list", command=self.get_friend_list, corner_radius=8)
        self.get_frlist.grid(row=5, column=0, padx=10, pady=(10, 10))

        self.bylabel = customtkinter.CTkLabel(master=self, text="by zakovskiy | GUI by chelicx")
        self.bylabel.grid(row=6, column=0, padx=20, pady=(10, 10))


    def __done(self) -> None:
        self.log("Done\n", "CONSOLE")

    def authorization_accounts(self) -> None:
        with open(FILE_DIRECTORY, 'r') as file:
            self.tokens = file.read().split()
        self.log("Authorizations accounts::", "CONSOLE")
        with open(FILE_DIRECTORY, 'w') as file:
            for token in self.tokens:
                try:
                    account = durakonline.Client(debug=DEBUG_MODE)
                    account.authorization.signin_by_access_token(token)
                    file.write(f"{token}\n")
                except Exception as e:
                    self.log("Failed log account", token)
                    if not REMOVE_INVALID_ACCOUNTS:
                        file.write(f"{token}\n")
                    continue
                self.accounts.append(account)
                self.log("Logged in", account.uid)
                time.sleep(.2)
        self.log("All auth", "CONSOLE")

    def random_nickname(self) -> None:
        for account in self.accounts:
            account.update_name(random.choice(self.nicknames))
            data = account._get_data("uu")
            while data["k"] != "name":
                data = account._get_data("uu")
            print(f"New name>> {data['v']}")
            time.sleep(.2)

    def nickname_enter(self):
        dialog = customtkinter.CTkInputDialog(text="Enter your nick", title="Change nick")
        name = dialog.get_input()
        for account in self.accounts:
            account.update_name(name)
            print(f"[{account.uid}] Nick changed")
            time.sleep(.2)
        self.__done()

    def update_avatar(self) -> None:
        with open(IMG_DIRECTORY, 'rb') as image_file:
            avatar = base64.b64encode(image_file.read()).decode()
        for account in self.accounts:
            account.update_avatar(avatar)
            time.sleep(.2)
            data = account._get_data("uu")
            while data["k"] != "avatar":
                data = account._get_data("uu")
            print(f"New avatar >> {data['v']}")
        self.__done()

    def delete_requests(self):
        for account in self.accounts:
            print(f"-----{account.uid}-----")
            friends = account.friend.get_list()
            print(f">> Всего друзей/заявок {len(friends)}")
            for friend in friends:
                if friend.kind == "REQUEST":
                    account.send_server(
                        {
                            "command": "friend_delete",
                            "id": friend.user.id
                        }
                    )
                    print(f">> Отменяю {friend.user.name}")
                    time.sleep(.5)
        self.__done()

    def delete_friends(self):
        for account in self.accounts:
            print(f"-----{account.uid}-----")
            friends = account.friend.get_list()
            print(f">> Всего друзей/заявок {len(friends)}")
            for friend in friends:
                account.send_server(
                    {
                        "command": "friend_delete",
                        "id": friend.user.id
                    }
                )
                print(f">> Удаляю {friend.user.name}")
                time.sleep(.5)
        self.__done()

    def get_friend_list(self):
        for account in self.accounts:
            print(f"-----{account.uid}-----")
            friends = account.friend.get_list()
            print(f"Всего друзей/заявок {len(friends)}")
            for friend in friends:
                if friend.kind == "REQUEST":
                    print(f"Ник: {friend.user.name} (заявка)")
                else:
                    print(f"Ник: {friend.user.name}")
        self.__done()

    def get_account_info(self) -> None:
        for account in self.accounts:
            print(f"""Token/UID {account.token} / {account.uid}
Name: {account.info.get('name')}
Balance: {account.info.get('points')}$
Avatar: {account.info.get('avatar')}\n""")
        self.__done()

    def log(self, message: str, server: str) -> None:
        print(f">> [{server}] [{datetime.now().strftime('%H:%M:%S')}] {message}")


if __name__ == "__main__":
    app = App()
    app.mainloop()


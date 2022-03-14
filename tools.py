import sys
import math
import threading
import time
from durakonline import durakonline
from datetime import datetime

FILE_DIRECTORY: str = "./accounts.txt"
DEBUG_MODE: bool = False

class DurakOnlineTools:

    tokens: [] = []
    accounts: [] = []

    def __init__(self) -> None:
        self.log(f"Load {self.load_accounts()} accounts", "CONSOLE")
        self.authorization_accounts()
        self.pages = [
            self.welcome,
            self.rename_nickname,
            self.buy_prem,
            self.free_bonus,
            self.delete_friends,
            self.mailing_to_friends,
            self.complaint_all,
        ]
        self.pages[0]()

    def welcome(self):
        print("""
        Select need function::
            1: Rename nicknames;
            2: Buy premium;
            3: Get free bonus;
            4: Remove all friends;
            5: Mailing to friends;
            6: Send complaints.
        """)
        function = int(
            input("<< Number: ")
        )
        self.pages[function]()

    def load_accounts(self) -> int:
        """
        data accounts in file by format:
            "
            token
            token
            ...
            "
        """
        file = open(FILE_DIRECTORY, "r")
        self.tokens = file.read().split("\n")
        file.close()
        return len(self.tokens)

    def authorization_accounts(self) -> None:
        self.log("Authorizations accounts::", "CONSOLE")
        for token in self.tokens:
            account = durakonline.Client(token=token, debug=DEBUG_MODE)
            self.accounts.append(account)
            self.log("Logged in", account.uid)
        self.log("All auth", "CONSOLE")


    def rename_nickname(self) -> None:
        nickname = str(
            input("<< Input new nickname: ")
        )
        for account in self.accounts:
            account.update_name(nickname)
            self.log("Rename nickname", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def buy_prem(self) -> None:
        for account in self.accounts:
            account.buy_prem()
            self.log("Buy premium", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def free_bonus(self) -> None:
        for account in self.accounts:
            account.buy_points()
            self.log("Get free bonus", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def delete_friends(self) -> None:
        for account in self.accounts:
            friends = account.get_friend_list()
            for friend in friends:
                account.friend_delete(friend.user.id)
                self.log(f"Remove friend {friend.user.name}", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def mailing_to_friends(self) -> None:
        text = str(
            input("<< Message: ")
        )
        for account in self.accounts:
            friends = account.get_friend_list()
            for friend in friends:
                account.send_message_friend(text, friend.user.id)
                self.log(f"Send to {friend.user.name}", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def complaint_all(self) -> None:
        to_id = int(
            input("<< User ID: ")
        )
        for account in self.accounts:
            account.complaint(to_id)
            self.log("Complaint send", account.uid)
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def log(self, message: str, server: str) -> None:
        print(f">> [{server}] [{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == "__main__":
    DurakOnlineTools()

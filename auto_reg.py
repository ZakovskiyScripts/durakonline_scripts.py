from durakonline import durakonline
from secrets import token_hex
from datetime import datetime


class AutoReg:

    def __init__(self):
        self.NICKNAME = str(
            input("<< Input nickname for all accounts (set the empty if you want random nickname): ")
        )

    def start(self) -> None:
        count = int(
            input("<< Accounts count: ")
        )
        for account in range(count):
            self.register_account(account + 1)

    def register_account(self, number: int) -> None:
        bot = durakonline.Client()
        nickname = self.NICKNAME if self.NICKNAME else token_hex(10)
        while True:
            self.log("Receiving captcha...", number)
            url = bot.authorization.get_captcha()["url"]
            captcha = ""
            if url:
                self.log(f"Captcha - {url}", number)
                captcha = str(input("<< Answer: "))
            self.log("Try register account...", number)
            try:
                token = bot.authorization.register(nickname, captcha).token
                self.log(f"Account with nickname {nickname} successfully do maked!\n", number)
            except:
                self.log("Unknown captcha, try again", number)
                continue

            return self.save(token)

    def save(self, token: str) -> None:
        file = open("./accounts.txt", "a+")
        file.write(f"{token}\n")
        file.close()

    def log(self, message: str, number: int) -> None:
        print(f">> [{number}] [{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == "__main__":

    AutoReg().start()

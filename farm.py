from durakonline import durakonline
from secrets import token_hex
from datetime import datetime

MAIN_TOKEN: str = ""
DEBUG_MODE: bool = False
SERVER_ID: str = "u1"
BET: int = 5000
FILE_DIRECTORY: str = "./accounts.txt"
PASSWORD: str = "byzakovskiy"

class Farm:

    def __init__(self):
        self.main = durakonline.Client(MAIN_TOKEN, server_id=SERVER_ID, tag="[MAIN]", debug=DEBUG_MODE)
        self.bot = durakonline.Client(tag="[BOT]", server_id=SERVER_ID, debug=DEBUG_MODE)
        self.log("Authorized account\n")
        self.pages = [
            self.from_file,
            self.auto_reg,
        ]
        print("Where to get accounts?:\n  1: From file;\n  2: Autoreg.")

    def start(self):
        page_type = int(input("<< Input number: "))
        self.pages[page_type-1]()

    def from_file(self):
        """
        The file with the accounts be in format
            '''
            token
            token
            ...
            '''
        """
        file = open(FILE_DIRECTORY, "r")
        accounts = file.read().split("\n")
        file.close()
        for token in accounts:
            self.game(token)

    def auto_reg(self):
        count = int(input("<< Count accounts: "))

        for _ in range(count):
            token = self.register_bot_account()
            self.log("Account successfully created!", "BOT")
            self.game(token)

    def game(self, token: str):
        # Step 0 - Auth bot-account
        self.bot.authorization.signin_by_access_token(token)
        self.bot._get_data("tour")
        self.log("Authorized account", "BOT")

        # Step 1 - Give bot-account 100 credits
        game = self.bot.game.create(100, PASSWORD, 2, 36)
        self.log("Created game on 100 credits", "BOT")
        self.main.game.join(PASSWORD, game.id)
        self.log("Join")
        self.main._get_data("game")
        self.log("Join in game and ready")
        self.main.game.ready()
        self.bot.game.ready()
        self.main._get_data("ready_on")
        self.log("Ready", "MAIN|BOT")
        self.main.game.surrender()
        self.main.game.leave(game.id)
        self.main._get_data("game_over")
        self.log("Surrender and leave")
        self.bot.game.leave(game.id)
        self.bot._get_data("game_over")
        self.log("Leave", "BOT")

        # Step 2 - Bot-account give us BET credits
        game = self.bot.game.create(BET, PASSWORD, 2, 36)
        self.log(f"Created game on {BET} credits", "BOT")
        self.main.game.join(PASSWORD, game.id)
        self.log("Join")
        self.main._get_data("game")
        self.log("Join in game and ready")
        self.main.game.ready()
        self.bot.game.ready()
        self.main._get_data("ready_on")
        self.log("Ready", "MAIN|BOT")
        self.bot.game.surrender()
        self.bot.game.leave(game.id)
        self.bot._get_data("game_over")
        self.log("Surrender and leave", "BOT")
        self.main.game.leave(game.id)
        self.main._get_data("game_over")
        self.log("Leave")

        # Step 3 - The write now balance
        data = self.main._get_data("uu")
        while data["k"] != "points":
            data = self.main._get_data("uu")
        self.log(f"Balance: {data['v']}")

    def register_bot_account(self) -> str:
        while True:
            self.log("Receiving captcha...", "BOT")
            url = self.bot.authorization.get_captcha()["url"]
            captcha = ""
            if url:
                self.log(f"Captcha - {url}", "BOT")
                captcha = str(input("<< Answer: "))
            self.log("Try register bot-account...", "BOT")
            try:
                return self.bot.authorization.register(token_hex(10), captcha).token
            except:
                self.log("Unknown captcha, try again", "BOT")
                continue

    def log(self, message: str, tag: str = "MAIN") -> None:
        print(f">> [{tag}] [{datetime.now().strftime('%H:%M:%S')}] {message}")


if __name__ == "__main__":
    script = Farm()
    script.start()

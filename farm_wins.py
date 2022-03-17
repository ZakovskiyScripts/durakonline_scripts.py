"""
The free version script written by t.me/zakovskiy
"""
import time
import threading
from durakonline import durakonline
from secrets import token_hex
from datetime import datetime

MAIN_TOKEN: str = ""
DEBUG_MODE: bool = False
PASSWORD: str = "zakovskiy"
BET: int = 100

class FarmWins:

    def start_game(self, main, bot, server_id: str, count: int = 49) -> None:
        game = bot.game.create(BET, PASSWORD, 2, 52)
        main.game.join(PASSWORD, game.id)
        main._get_data("game")
        for i in range(count):
            self.log(f"{i+1} game", server_id)
            main.game.ready()
            bot.game.ready()

            for i in range(4):
                try:
                    main_cards = main._get_data("hand")["cards"]
                except:
                    pass
                try:
                    bot_cards = bot._get_data("hand")["cards"]
                except:
                    pass
                mode = bot._get_data("mode")
                if mode["0"] == 1:
                    bot.game.turn(bot_cards[0])
                    time.sleep(.1)
                    main.game.take()
                    time.sleep(.1)
                    bot.game._pass()
                else:
                    main.game.turn(main_cards[0])
                    time.sleep(.1)
                    bot.game.take()
                    time.sleep(.1)
                    main.game._pass()
            bot.game.surrender()
            bot._get_data("game_over")
        main.game.leave(game.id)
        self.log("Leave", "MAIN")
        data = main._get_data("uu")
        while data["k"] != "points":
            data = main._get_data("uu")
        self.log(f"Balance: {data.get('v')}", "MAIN")

    def start(self) -> None:
        count = int(input("<< Count: "))
        for _ in range(count):
            bot = durakonline.Client(tag="[BOT]", server_id="u1", debug=DEBUG_MODE)
            token = self.register_bot_account(bot)
            self.acc(token)

    def acc(self, token: str) -> None:
        main = durakonline.Client(MAIN_TOKEN, server_id="u1", tag="[MAIN]", debug=DEBUG_MODE)
        bot = durakonline.Client(token, server_id="u1", tag="[BOT]", debug=DEBUG_MODE)
        self.start_game(main, bot, "u1")

    def register_bot_account(self, bot) -> str:
        while True:
            self.log("Receiving captcha...", "BOT")
            url = bot.authorization.get_captcha()["url"]
            captcha = ""
            if url:
                self.log(f"Captcha - {url}", "BOT")
                captcha = str(input("<< Answer: "))
            self.log("Try register bot-account...", "BOT")
            try:
                return bot.authorization.register(token_hex(10), captcha).token
            except:
                self.log("Unknown captcha, try again", "BOT")
                continue

    def log(self, message: str, tag: str = "MAIN") -> None:
        print(f">> [{tag}] [{datetime.now().strftime('%H:%M:%S')}] {message}")


if __name__ == "__main__":
    FarmWins().start()

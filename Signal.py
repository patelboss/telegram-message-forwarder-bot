import bot.helper.utils
import sys
import logging
from os import environ

log_level = environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(format='[%(asctime)s - %(pathname)s - %(levelname)s] %(message)s',
                    handlers=[logging.FileHandler(
                        'log.txt'), logging.StreamHandler()],
                    level=log_level)
LOG = logging.getLogger(__name__)


def get_formatted_chats(chats, app):
    formatted_chats = []
    for chat in chats:
        try:
            if isInt(chat):
                formatted_chats.append(int(chat))
            elif chat.startswith("@"):
                formatted_chats.append(app.get_chat(chat.replace("@", "")).id)
            elif chat.startswith("https://t.me/c/") or chat.startswith("https://telegram.org/c/") or chat.startswith("https://telegram.dog/c/"):
                chat_id = chat.split("/")[4]
                if isInt(chat_id):
                    chat_id = "-100" + str(chat_id)
                    chat_id = int(chat_id)
                else:
                    chat_id = app.get_chat(chat_id).id
                formatted_chats.append(chat_id)
            else:
                LOG.warn("Chat ID cannot be parsed: {chat}")
        except Exception as e:
            LOG.error("Chat ID cannot be parsed: {chat}")
            LOG.error(e)
            sys.exit(1)

    # Handle the SIGINT signal
    signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))

    return formatted_chats


def main():
    app = Telegram()
    chats = ["@user1", "https://t.me/c/123456789", "123456789"]
    formatted_chats = get_formatted_chats(chats, app)
    print(formatted_chats)


if __name__ == "__main__":
    main()

import os
import sys
import logging
from os import environ
from dotenv import load_dotenv
from pyrogram import Client
from bot.helper.utils import get_formatted_chats

logging.basicConfig(
    format='[%(asctime)s - %(pathname)s - %(levelname)s] %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOG = logging.getLogger(__name__)


def setup_logging():
    # Add line numbers and error messages to log entries
    logging.basicConfig(
        format='[%(asctime)s - %(module)s - %(levelname)s] %(message)s',
        handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
        level=logging.INFO
    )


def load_configuration():
    try:
        api_id = int(environ["API_ID"])
        api_hash = environ["API_HASH"]
        bot_token = environ.get("BOT_TOKEN")
        tg_session = environ.get("TELEGRAM_SESSION")
        sudo_users = list(set(x for x in environ.get("SUDO_USERS", "999197022").split(";")))
        
        try:
            from_chats = list(set(int(x) for x in environ.get("FROM_CHATS").split()))
            to_chats = list(set(int(x) for x in environ.get("TO_CHATS").split()))
        except ValueError as e:
            LOG.error(e)
            LOG.error("One or more variables are wrong. Exiting...")
            sys.exit(1)

        advance_config = environ.get("ADVANCE_CONFIG")
        if advance_config:
            from_chats = []
    
        replace_string = environ.get("REPLACE_STRING", "")

        # Add port information
        port = int(environ.get("PORT", 8080))
    except KeyError as e:
        LOG.error(e)
        LOG.error("One or more variables missing. Exiting...")
        sys.exit(1)

    # Return the configuration variables as a dictionary
    return {
        "api_id": api_id,
        "api_hash": api_hash,
        "bot_token": bot_token,
        "tg_session": tg_session,
        "sudo_users": sudo_users,
        "from_chats": from_chats,
        "to_chats": to_chats,
        "advance_config": advance_config,
        "replace_string": replace_string,
        "port": port  # Add port to the dictionary
        }

def setup_app(api_id, api_hash, bot_token, tg_session):
    if tg_session:
        app = Client(tg_session, api_id, api_hash)
    elif bot_token:
        app = Client(":memory:", api_id, api_hash, bot_token=bot_token)
    else:
        LOG.error("Set either TELEGRAM_SESSION or BOT_TOKEN variable.")
        sys.exit(1)
    
    return app


def configure_logging():
    LOG.info(f"Sudo users - {sudo_users}")


def configure_advance_config():
    if advance_config:
        for chats in advance_config.split(";"):
            chat = chats.strip().split()
            chat = get_formatted_chats(chat, app)
            f = chat[0]
            del chat[0]
            if f in chats_data:
                c = chats_data[f]
                c.extend(chat)
                chats_data[f] = c
            else:
                chats_data[f] = chat
            if f not in from_chats:
                from_chats.append(f)
        LOG.info(from_chats)
        LOG.info(chats_data)
    else:
        if len(to_chats) == 0 or len(from_chats) == 0:
            LOG.error("Set either ADVANCE_CONFIG or FROM_CHATS and TO_CHATS")
            sys.exit(1)
        else:
            from_chats = get_formatted_chats(from_chats, app)
            to_chats = get_formatted_chats(to_chats, app)
            LOG.info(from_chats)
            LOG.info(to_chats)


def main():
    setup_logging()
    configuration = load_configuration()

    app = setup_app(
        configuration["api_id"],
        configuration["api_hash"],
        configuration["bot_token"],
        configuration["tg_session"]
    )

    with app:
        configure_logging()
        configure_advance_config()


if __name__ == "__main__":
    main()

from os import path, getenv
from dotenv import load_dotenv

# fmt: off

TEST_MODE        = True
BUILD_LOCAL_DEPS = True

check_cooldown          = 1500
reconnecting_error_sent = False

current_dir = path.dirname(path.abspath(__file__))
secrets_dir = path.join(current_dir, '..', 'Secrets')

BUILD_DIR            = path.join(current_dir, '..', 'build')
SERVICE_ACCOUNT_FILE = path.abspath(path.join(secrets_dir, 'schedulespybot-6e8cfdc17fcb.json'))
SCHEDULE_CLASS_DIR   = path.abspath(path.join(current_dir, '..', 'scheduleClass'))
COMPARER_DIR         = path.abspath(path.join(current_dir, '..', 'comparer'))
COMPARER_DLL_PATH    = path.join(BUILD_DIR, 'comparer.dll')
PARSER_DIR           = path.abspath(path.join(current_dir, '..', 'parser'))
PARSER_DLL_PATH      = path.join(BUILD_DIR, 'parser.dll')

load_dotenv(path.join(secrets_dir, 'KEYS.env'))

ADMIN_IDS      = getenv('ADMIN_IDS')
LOG_CLIENT_API = getenv('LOG_CLIENT_API')

if TEST_MODE:
    TELEGRAM_BOT_API = getenv('BOT_API_T')
    SPREADSHEET_ID   = getenv('SPREADSHEET_ID_T')

    # database
    PHP_API_URL        = getenv('PHP_API_URL_T')
    USER_IDS_URL       = getenv('USER_IDS_URL_T')
    OLD_SCHEDULE_URL   = getenv('OLD_SCHEDULE_URL_T')
    ALL_BY_USERS_URL   = getenv('ALL_BY_USERS_URL_T')
    SAVE_SCHEDULE_URL  = getenv('SAVE_SCHEDULE_URL_T')
    GET_SHEET_NAME_URL = getenv('GET_SHEET_NAME_T')
    DELETE_SHEET_URL   = getenv('DELETE_SHEET_T')
    BLOCK_USERS_URL    = getenv('BLOCK_USERS_T')
    GET_BLOCKED_URL    = getenv('GET_BLOCKED_USERS_T')
else:
    TELEGRAM_BOT_API = getenv('BOT_API')
    SPREADSHEET_ID   = getenv('SPREADSHEET_ID')

    # database
    PHP_API_URL        = getenv('PHP_API_URL')
    USER_IDS_URL       = getenv('USER_IDS_URL')
    OLD_SCHEDULE_URL   = getenv('OLD_SCHEDULE_URL')
    ALL_BY_USERS_URL   = getenv('ALL_BY_USERS_URL')
    SAVE_SCHEDULE_URL  = getenv('SAVE_SCHEDULE_URL')
    GET_SHEET_NAME_URL = getenv('GET_SHEET_NAME')
    DELETE_SHEET_URL   = getenv('DELETE_SHEET')
    BLOCK_USERS_URL    = getenv('BLOCK_USERS_URL')
    GET_BLOCKED_URL    = getenv('GET_BLOCKED_USERS_URL')

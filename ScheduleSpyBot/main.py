import time
import telebot
import threading
import subprocess
import botCommands  # noqa: F401 (this import is necessary to register commands)

from logger import log
from botBase import bot
from dataProcessor import compare_all_groups
from botEnv import (
    BUILD_DIR,
    BUILD_LOCAL_DEPS,
    COMPARER_DIR,
    PARSER_DIR,
    SCHEDULE_CLASS_DIR,
    check_cooldown,
    reconnecting_error_sent,
)


def build_local_dependency(dir: str, build_target: str) -> None:
    try:
        build_result = subprocess.run(
            ['dotnet', 'build', '-c', 'Release', '-o', BUILD_DIR, dir],
            capture_output=True,
            text=True,
        )

        if build_result.returncode != 0:
            log(f'{build_target} Build Error: {build_result.stderr.strip()}')
            return

        log(f'{build_target} compiled successfully.')
    except FileNotFoundError:
        log(f'{build_target} Build Error: .NET SDK not found. Is `dotnet` installed and in PATH?')


def checker_loop(check_cooldown: int) -> None:
    log('Checker loop started...')

    while True:
        compare_all_groups()
        time.sleep(check_cooldown)


def connection_checker() -> None:
    global reconnecting_error_sent

    while True:
        time.sleep(10)

        try:
            # chat id is random, just for check the connection
            bot.send_message(777000, '')
        except Exception as e:
            if 'Bad Request: message text is empty' in str(e) and reconnecting_error_sent:
                log("З'єднання відновлено.")
                reconnecting_error_sent = False
        else:
            if reconnecting_error_sent:
                log("З'єднання відновлено.")
                reconnecting_error_sent = False


def reconnect() -> None:
    global reconnecting_error_sent

    while True:
        try:
            bot.polling(none_stop=True, timeout=180)
        except telebot.apihelper.ApiException as e:
            if 'retry after' in str(e):
                log('Виникла помилка. Забагато запитів.')
        except Exception as e:
            if not reconnecting_error_sent:
                log(f'Виникла помилка:\n{e}')
                log('Перезапуск...')
                reconnecting_error_sent = True


if __name__ == '__main__':
    if BUILD_LOCAL_DEPS:
        log('Building local dependencies...')

        build_local_dependency(SCHEDULE_CLASS_DIR, 'ScheduleClass')
        build_local_dependency(COMPARER_DIR, 'Comparer')
        build_local_dependency(PARSER_DIR, 'Parser')

        log('Build finished')

    log('Bot started...')

    thread = threading.Thread(target=checker_loop, args=(check_cooldown,))
    thread.start()

    reconnect_thread = threading.Thread(target=reconnect)
    reconnect_thread.start()

    connection_checker_thread = threading.Thread(target=connection_checker)
    connection_checker_thread.start()

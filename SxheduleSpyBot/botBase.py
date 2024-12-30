from openpyxl import workbook
import telebot
from dotenv import load_dotenv
from dataProcessor import GetSchedule, CompareSchedules, LoadWorkbook
import os
import enumerations as enums

load_dotenv(dotenv_path=r'../Secrets/KEYS.env')
TELEGRAM_BOT_API = os.getenv("BOT_API")
bot = telebot.TeleBot(TELEGRAM_BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Є єдина команда /print {номер тижня}\nНаприклад /print 4 - виведе розклад за 4 тиждень. Поки все")

@bot.message_handler(commands=['print'])
def send_sheet_data(message):
    print(f"print call by {message.from_user.first_name}")
    try:
        cParts = message.text.split()
        if len(cParts) != 2:
            bot.send_message(
                message.chat.id,"Будь ласка, вкажіть номер аркуша. Наприклад: /print 4")
            return

        if int(cParts[1]) - 1 < 0 or int(cParts[1]) - 1 > 17:
            raise IndexError("Номер аркуша виходить за межі допустимого діапазону (1-17).")

        bot.send_message(message.chat.id, "Почекайте...")
        bot.send_message(message.chat.id, GetSchedule(LoadWorkbook().worksheets[int(cParts[1]) - 1], enums.Group.KN24_1.value))

    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть коректний номер аркуша. Наприклад: /print 4")
    except IndexError:
        bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {e}")

@bot.message_handler(commands=['compare'])
def compare(message):
    print(f"comparator call by {message.from_user.first_name}")
    try:
        cParts = message.text.split()
        if len(cParts) != 3:
            bot.send_message(
                message.chat.id,
                "Будь ласка, вкажіть два номери аркушів для порівняння. Наприклад: /compare 4 5"
            )
            return
        if int(cParts[1]) - 1 < 0 or int(
                cParts[1]) - 1 > 17 or int(
                    cParts[2]) - 1 < 0 or int(
                        cParts[2]) - 1 > 17:
            raise IndexError(
                "Номер аркуша виходить за межі допустимого діапазону (1-17).")
        bot.send_message(message.chat.id, "Почекайте...")

        workbook = LoadWorkbook()
        schedule1 = GetSchedule(workbook.worksheets[int(cParts[1]) - 1], enums.Group.KN24_1.value)
        schedule2 = GetSchedule(workbook.worksheets[int(cParts[2]) - 1], enums.Group.KN24_1.value)

        bot.send_message(
            message.chat.id,
            f'{CompareSchedules(f"{schedule1}", f"{schedule2}")}')

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Будь ласка, введіть коректні номери аркушів для порівняння. Наприклад: /compare 4 5"
        )
    except IndexError:
        bot.send_message(message.chat.id,
                         "Немає аркуша з таким номером. Перевірте ще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {e}")
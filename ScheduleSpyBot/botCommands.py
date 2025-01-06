import telebot
from dataProcessor import GetSchedule, CompareSchedules, LoadWorkbook, ParseComparerOutput, CompareAllGroups
from botBase import bot
import databaseManager
from enumerations import Group
from logger import log, adminPanel

@bot.message_handler(commands=['start'])
def start(message):
    log(f"start call by {message.from_user.first_name}")
    bot.send_message(message.chat.id, "Є єдина команда /print {номер тижня}\nНаприклад /print 4 - виведе розклад за 4 тиждень. Поки все", message_thread_id=message.message_thread_id)

    fullName = None
    if message.from_user.last_name is not None:
        fullName = f"{message.from_user.first_name} {message.from_user.last_name}"
    else:
        fullName = message.from_user.first_name

    databaseManager.SaveUser(message.from_user.id, fullName, message.from_user.username)

    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("КС241_1", callback_data=f"{Group.KC241_1.name}")
    button2 = telebot.types.InlineKeyboardButton("КС241_2", callback_data=f"{Group.KC241_2.name}")
    button3 = telebot.types.InlineKeyboardButton("КС242_1", callback_data=f"{Group.KC242_1.name}")
    button4 = telebot.types.InlineKeyboardButton("КС242_2", callback_data=f"{Group.KC242_2.name}")
    button5 = telebot.types.InlineKeyboardButton("КН24_1",  callback_data=f"{Group.KN24_1.name}")
    button6 = telebot.types.InlineKeyboardButton("КН24_2",  callback_data=f"{Group.KN24_2.name}")
    button7 = telebot.types.InlineKeyboardButton("КТ24",    callback_data=f"{Group.KT24.name}")
        
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5, button6, button7)
      
    sent_message = bot.send_message(message.chat.id, "Оберіть групу:", reply_markup=keyboard, message_thread_id=message.message_thread_id)

@bot.message_handler(commands=['changeGroup'])
def change_group(message):
    log(f"change group call by {message.from_user.first_name}")
    fullName = None
    if message.from_user.last_name is not None:
        fullName = f"{message.from_user.first_name} {message.from_user.last_name}"
    else:
        fullName = message.from_user.first_name

    databaseManager.SaveUser(message.from_user.id, fullName, message.from_user.username)

    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("КС241_1", callback_data=f"{Group.KC241_1.name}")
    button2 = telebot.types.InlineKeyboardButton("КС241_2", callback_data=f"{Group.KC241_2.name}")
    button3 = telebot.types.InlineKeyboardButton("КС242_1", callback_data=f"{Group.KC242_1.name}")
    button4 = telebot.types.InlineKeyboardButton("КС242_2", callback_data=f"{Group.KC242_2.name}")
    button5 = telebot.types.InlineKeyboardButton("КН24_1",  callback_data=f"{Group.KN24_1.name}")
    button6 = telebot.types.InlineKeyboardButton("КН24_2",  callback_data=f"{Group.KN24_2.name}")
    button7 = telebot.types.InlineKeyboardButton("КТ24",    callback_data=f"{Group.KT24.name}")
        
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5, button6, button7)
    
    sent_message = bot.send_message(message.chat.id, "Оберіть групу:", reply_markup=keyboard, message_thread_id=message.message_thread_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, f"Ви обрали групу: {call.data}", message_thread_id=call.message_thread_id)

    databaseManager.UpdateUserGroup(call.from_user.id, call.data)

# Admin only

@bot.message_handler(commands=['print'])
def send_sheet_data(message):
    if message.chat.id == adminPanel.groupId:
        log(f"print call by {message.from_user.first_name}")
        try:
            cParts = message.text.split()
            if len(cParts) != 2:
                bot.send_message(message.chat.id, "Будь ласка, вкажіть номер аркуша. Наприклад: /print 4", message_thread_id=message.message_thread_id)
                return

            bot.send_message(message.chat.id, "Почекайте...", message_thread_id=message.message_thread_id)

            bot.send_message(message.chat.id, GetSchedule(LoadWorkbook().worksheets[int(cParts[1]) - 1], Group.KC241_1.value, False), message_thread_id=message.message_thread_id)      

        except ValueError:
            bot.send_message(message.chat.id, "Будь ласка, введіть коректний номер аркуша. Наприклад: /print 4", message_thread_id=message.message_thread_id)
        except IndexError:
            bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.", message_thread_id=message.message_thread_id)
        except Exception as e:
            log(f"Сталася помилка: {e}", message.message_thread_id)

@bot.message_handler(commands=['compare'])
def compare(message):
    if message.chat.id == adminPanel.groupId:
        log(f"comparator call by {message.from_user.first_name}")
        try:
            cParts = message.text.split()
            if len(cParts) != 3:
                bot.send_message(message.chat.id, "Будь ласка, вкажіть два номери аркушів для порівняння. Наприклад: /compare 4 5", message_thread_id=message.message_thread_id)
                return

            bot.send_message(message.chat.id, "Почекайте...", message_thread_id=message.message_thread_id)

            workbook = LoadWorkbook()
            schedule1 = GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KN24_1.value)
            schedule2 = GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KN24_1.value)

            bot.send_message(message.chat.id, CompareSchedules(schedule1, schedule2))

        except ValueError:
            bot.send_message(message.chat.id, "Будь ласка, введіть коректні номери аркушів для порівняння. Наприклад: /compare 4 5", message_thread_id=message.message_thread_id)
        except IndexError:
            bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.", message_thread_id=message.message_thread_id)
        except Exception as e:
            log(f"Сталася помилка: {e}", message.message_thread_id)

@bot.message_handler(commands=['cool_compare'])
def coolCompare(message):
    if message.chat.id == adminPanel.groupId:
        log(f"coolComparator call by {message.from_user.first_name}")
        try:
            cParts = message.text.split()
            if len(cParts) != 3:
                bot.send_message(message.chat.id, "Будь ласка, вкажіть два номери аркушів для порівняння. Наприклад: /coolCompare 4 5", message_thread_id=message.message_thread_id)
                return

            bot.send_message(message.chat.id, "Почекайте...", message_thread_id=message.message_thread_id)

            workbook = LoadWorkbook()
            schedule1 = GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KC242_2.value)
            schedule2 = GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KC242_2.value)

            bot.send_message(message.chat.id, ParseComparerOutput(CompareSchedules(schedule1, schedule2)), parse_mode='Markdown', message_thread_id=message.message_thread_id)

        except ValueError:
            bot.send_message(message.chat.id, "Будь ласка, введіть коректні номери аркушів для порівняння. Наприклад: /compare 4 5", message_thread_id=message.message_thread_id)
        except IndexError:
            bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.", message_thread_id=message.message_thread_id)
        except Exception as e:
            log(f"Сталася помилка: {e}", message_thread_id=message.message_thread_id)

@bot.message_handler(commands=['fill_schedule_table'])
def fill_group_handler(message):
    if message.chat.id == adminPanel.groupId:
        try:
            cParts = message.text.split()
            if len(cParts) != 2:
                bot.send_message(message.chat.id, "Будь ласка, вкажіть номер аркуша. Наприклад: /fill_schedule_table 4", message_thread_id=message.message_thread_id)
                return
            log("Заповнюю бд...", message.message_thread_id)
            sheet = LoadWorkbook().worksheets[int(cParts[1])]
            for group in Group:
                log(f"Заповнюю групу {group.name}", message.message_thread_id)
                schedule = GetSchedule(sheet, group.value)            
                databaseManager.WriteSchedule(group.name, f"{schedule}")
            log("Готово", message.message_thread_id)

        except ValueError:
            bot.send_message(message.chat.id, "Будь ласка, введіть коректні номери аркушів для порівняння. Наприклад: /fill_schedule_table 4", message.message_thread_id)
        except IndexError:
            bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.", message.message_thread_id)
        except Exception as e:
            log(f"Сталася помилка: {e}", message.message_thread_id)       

@bot.message_handler(commands=['call_checker'])
def fill_group_handler(message):
    if message.chat.id == adminPanel.groupId:   
        CompareAllGroups()               

@bot.message_handler(func=lambda message: True)
def send(message):
    if message.chat.id == adminPanel.groupId and message.text.startswith('$'):
        text=message.text.replace('$', '', 1)
        try:            
            exec(text)
        except Exception as e:            
            log(e)
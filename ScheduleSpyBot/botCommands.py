import telebot
import dataProcessor
import databaseManager
from botBase import bot
from logger import log, adminPanel
from enumerations import Group, Notifier, notifierToGroup

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
    bot.send_message(call.message.chat.id, f"Ви обрали групу: {call.data}")

    databaseManager.UpdateUserGroup(call.from_user.id, call.data)

# Admin only

@bot.message_handler(commands=['delete_week'])
def delete_week(message):
    if message.chat.id == adminPanel.groupId:        
        try:
            cParts = message.text.split()
            if len(cParts) == 2:
                databaseManager.DeleteSheet(cParts[1])
            elif len(cParts) == 2:
                databaseManager.DeleteSheet()
            else:
                bot.send_message(message.chat.id, "Будь ласка, вкажіть номер тижня. Наприклад: /delete_week 4", message_thread_id=message.message_thread_id)
                return           

        except ValueError:
            bot.send_message(message.chat.id, "Будь ласка, введіть коректний номер тижня. Наприклад: /delete_week 4", message_thread_id=message.message_thread_id)
        except IndexError:
            bot.send_message(message.chat.id, "Немає тижня з таким номером. Перевірте ще раз.", message_thread_id=message.message_thread_id)
        except Exception as e:
            log(f"Сталася помилка: {e}", message.message_thread_id)

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

            bot.send_message(message.chat.id, dataProcessor.GetSchedule(dataProcessor.LoadWorkbook().worksheets[int(cParts[1]) - 1], Group.KC241_1, False), message_thread_id=message.message_thread_id)      

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

            workbook = dataProcessor.LoadWorkbook()
            schedule1 = dataProcessor.GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KN24_1)
            schedule2 = dataProcessor.GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KN24_1)

            bot.send_message(message.chat.id, dataProcessor.CompareSchedules(schedule1, schedule2))

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

            workbook = dataProcessor.LoadWorkbook()
            schedule1 = dataProcessor.GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KC242_2)
            schedule2 = dataProcessor.GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KC242_2)

            bot.send_message(message.chat.id, dataProcessor.ParseComparerOutput(dataProcessor.CompareSchedules(schedule1, schedule2)), parse_mode='Markdown', message_thread_id=message.message_thread_id)

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
            sheet = dataProcessor.LoadWorkbook().worksheets[int(cParts[1])-1]
            sheetWeekNum = sheet.title.split("т")[0]
            for group in Group:
                log(f"Заповнюю групу {group.name}", message.message_thread_id)
                schedule = dataProcessor.GetSchedule(sheet, group)          
                databaseManager.WriteSchedule(sheetWeekNum, group, f"{schedule}")
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
        dataProcessor.CompareAllGroups()               

@bot.message_handler(func=lambda message: message.chat.id == adminPanel.groupId and
                     message.message_thread_id == adminPanel.commandPlaceThreadId and
                     message.text.startswith('$'))
def send(message):
    text=message.text.replace('$', '', 1)
    try:            
        exec(text)
    except Exception as e:            
        log(e)

@bot.message_handler(func=lambda message: message.chat.id == adminPanel.groupId and
                     message.message_thread_id in [item.value for item in Notifier],
                     content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker', 'voice', 'location', 'contact', 'animation'])
def send(message):
    if Notifier(message.message_thread_id) != Notifier.general:
        group = notifierToGroup.get(Notifier(message.message_thread_id))
        users = databaseManager.GetAllUsersByGroup(group)   
    else:            
        users = databaseManager.GetAllUserIds()

    if users:
        for user in users:
            try:                                                           
                if message.content_type == 'text':
                    bot.send_message(chat_id=user, text=message.text)                    
                elif message.content_type == 'sticker':
                    bot.send_sticker(chat_id=user, sticker=message.sticker.file_id)
                elif message.content_type == 'video':
                    bot.send_video(chat_id=user, video=message.video.file_id, caption=message.caption or "")
                elif message.content_type == 'audio':
                    bot.send_audio(chat_id=user, audio=message.audio.file_id, caption=message.caption or "")
                elif message.content_type == 'voice':
                    bot.send_voice(chat_id=user, voice=message.voice.file_id, caption=message.caption or "")
                elif message.content_type == 'photo':
                    bot.send_photo(chat_id=user, photo=message.photo[-1].file_id, caption=message.caption or "")
                elif message.content_type == 'document':
                    bot.send_document(chat_id=user, document=message.document.file_id, caption=message.caption or "")
                elif message.content_type == 'animation':
                    bot.send_animation(chat_id=user, animation=message.animation.file_id, caption=message.caption or "")
                else:
                    log(f"Тип повідомлення {message.content_type} не підтримується.")

            except Exception as e:
                log(f"Сталася помилка: {e}")
    else:
        log(f"Сталася помилка. Группу для масового сповіщення не знайдено")
import os
import telebot
import platform
import dataProcessor
import databaseManager
from logger import log
from botBase import bot
from enumerations import Group, Notifier, AdminPanel, notifierToGroup


@bot.message_handler(commands=['start'])
def start(message):
    log(f"start call by {message.from_user.first_name}")
    bot.send_message(message.chat.id, 
                    "Привіт! Це бот, який автоматично відслідковує зміни у твоєму розкладі. 📅\n"
                    "Як тільки буде знайдено оновлення, він в межах декількох хвилин надішле тобі повідомлення! 🔔\n"
                    "Все що тобі потрібно це лише вибрати про оновлення розкладу якої групи ти хочеш отримувати сповіщення.\n"
                    "Введи /about, щоб дізнатися більше про його можливості та як він влаштований.", 
                    message_thread_id=message.message_thread_id)
    fullName = None
    if message.from_user.last_name is not None:
        fullName = f"{message.from_user.first_name} {message.from_user.last_name}"
    else:
        fullName = message.from_user.first_name

    databaseManager.SaveUser(message.from_user.id, fullName, message.from_user.username)


    if databaseManager.GetUserInfo(message.from_user.id)['group_name']=="":
        change_group(message)

@bot.message_handler(commands=['change_group'])
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
    
    sent_message = bot.send_message(message.chat.id, "Обери групу за розкладом якої ти хочеш слідкувати:", reply_markup=keyboard, message_thread_id=message.message_thread_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, f"Ви обрали групу: {call.data}")

    databaseManager.UpdateUserGroup(call.from_user.id, call.data)

@bot.message_handler(commands=['help'])
def helpComm(message):
    log(f"help call by {message.from_user.first_name}")
    bot.send_message(message.chat.id, 
                     "Список доступних комманд:\n"
                     "/start - вивести стартове вітання бота.\n"
                     "/changeGroup - змінити групу за розкладом якої ти хочеш слідкувати.\n"
                     "/schedule - вивести способи перегляду розкладу на актуальному тижні (Через слабку підтримку віджета Google Spreadsheet на мобільних пристроях вибір аркушів незручний.).\n"
                     "/about - вивести інформацію про бота.\n"
                     "/help - вивести цей список.\n",                     
                     message_thread_id=message.message_thread_id)

@bot.message_handler(commands=['about'])
def about(message):
    log(f"about call by {message.from_user.first_name}")
    bot.send_message(message.chat.id, 
                     "Це бот для відслідковування змін у розкладі.\n"
                     "Ось як він працює:\n"
                     "- Завантажує поточний розклад. ⬇️\n"
                     "- Порівнює його зі збереженим розкладом, що був декілька хвилин тому. ↔️\n"
                     "- Якщо знаходить зміни в вибраній тобою групі, надсилає тобі повідомлення. 🔔\n"
                     "\nТакож бот повідомить тебе при появі нового тижня в розкладі. 📅\n"
                     "\nЯкщо потрібна допомога, є ідеї для покращення або ти зіткнувся з [багом](https://youtu.be/dQw4w9WgXcQ), звертайся до адміністратора (контакти вказані в опису бота).", 
                     parse_mode="Markdown",
                     disable_web_page_preview=True,
                     message_thread_id=message.message_thread_id)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    log(f"schedule call by {message.from_user.first_name}")    
    markup = telebot.types.InlineKeyboardMarkup()
    
    if len(dataProcessor.weekNums) == 0:
        log("Помилка. Не вдалося отримати записані тижні з бази данних.")
        bot.send_message(message.chat.id, "Виникла помилка. Зв'яжіться з адміністратором.")
        return None

    currWeekNum = dataProcessor.weekNums[0]
    currWeekGid = dataProcessor.gids[int(currWeekNum)-1] or 1

    button1 = telebot.types.InlineKeyboardButton(text="Відкрити розклад", web_app=telebot.types.WebAppInfo(url=
                                                    f"https://remenod.github.io/ScheduleSpyBot/?currWeekGid={currWeekGid}"))
    button = telebot.types.InlineKeyboardButton(text="Відкрити розклад (URL)", url=
                                                    f"https://docs.google.com/spreadsheets/u/0/d/{dataProcessor.SPREADSHEET_ID}"
                                                    f"/htmlview?output=html&rm=demo&pli=1&widget=true&gid={currWeekGid}#gid={currWeekGid}")

    markup.add(button1)
    markup.add(button)
    bot.send_message(message.chat.id, "Ось розклад на актуальній сторінці", reply_markup=markup)


# Admin only

@bot.message_handler(commands=['delete_week'])
def delete_week(message):
    if message.chat.id == AdminPanel.groupId.value:
        log(f"delete_week call by {message.from_user.first_name}")
        try:
            cParts = message.text.split()
            if len(cParts) == 2:
                databaseManager.DeleteSheet(cParts[1])
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
    if message.chat.id == AdminPanel.groupId.value:
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
    if message.chat.id == AdminPanel.groupId.value:
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
    if message.chat.id == AdminPanel.groupId.value:
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
    if message.chat.id == AdminPanel.groupId.value:
        log(f"fill_schedule_table call by {message.from_user.first_name}")
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
    if message.chat.id == AdminPanel.groupId.value: 
        log("checker call")
        dataProcessor.CompareAllGroups()
        
@bot.message_handler(commands=['stop'])
def stop(message):
    if message.chat.id == AdminPanel.groupId.value:
        log(f"stop call by {message.from_user.first_name}")
        curent_system = platform.system()
        if curent_system == 'Windows':
            log("Зупинка бота...")
            os.system('taskkill /F /PID %d' % os.getpid())
            log("But it refused.")
        elif curent_system == 'Linux':
            log("Зупинка бота...")
            os._exit(0)
            log("But it refused.")
        else:
            try:
                log("Зупинка бота...")
                os._exit(0)
                os.system('taskkill /F /PID %d' % os.getpid())
            except Exception as e:
                log(f"Помилка при спробі зупинки бота: {e}")
            log("Спроба зупинки бота на незареєстрованій системі завершилась невдачею.")   


@bot.message_handler(func=lambda message: message.chat.id == AdminPanel.groupId.value and
                     message.message_thread_id == AdminPanel.commandPlaceThreadId.value and
                     message.text.startswith('$'))
def execMsg(message):
    text=message.text.replace('$', '', 1)
    try:            
        exec(text)
    except Exception as e:            
        log(e)

@bot.message_handler(func=lambda message: message.chat.id == AdminPanel.groupId.value and
                     message.message_thread_id in [item.value for item in Notifier],
                     content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker', 'voice', 'location', 'contact', 'animation'])
def notify(message):
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
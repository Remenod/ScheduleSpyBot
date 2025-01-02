from dataProcessor import GetSchedule, CompareSchedules, LoadWorkbook, ParseComparerOutput
from botBase import bot
import databaseManager
from enumerations import Group

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "� ����� ������� /print {����� �����}\n��������� /print 4 - ������ ������� �� 4 �������. ���� ���")

    databaseManager.SaveUser(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name}", message.from_user.username)

    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("��241_1", callback_data=f"{Group.KC241_1.name}")
    button2 = telebot.types.InlineKeyboardButton("��241_2", callback_data=f"{Group.KC241_2.name}")
    button3 = telebot.types.InlineKeyboardButton("��242_1", callback_data=f"{Group.KC242_1.name}")
    button4 = telebot.types.InlineKeyboardButton("��242_2", callback_data=f"{Group.KC242_2.name}")
    button5 = telebot.types.InlineKeyboardButton("��24_1",  callback_data=f"{Group.KN24_1.name}")
    button6 = telebot.types.InlineKeyboardButton("��24_2",  callback_data=f"{Group.KN24_2.name}")
    button7 = telebot.types.InlineKeyboardButton("��24",    callback_data=f"{Group.KT24.name}")
        
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5, button6, button7)
      
    sent_message = bot.send_message(message.chat.id, "������ �����:", reply_markup=keyboard)

@bot.message_handler(commands=['changeGroup'])
def change_group(message):
    databaseManager.SaveUser(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name}", message.from_user.username)

    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("��241_1", callback_data=f"{Group.KC241_1.name}")
    button2 = telebot.types.InlineKeyboardButton("��241_2", callback_data=f"{Group.KC241_2.name}")
    button3 = telebot.types.InlineKeyboardButton("��242_1", callback_data=f"{Group.KC242_1.name}")
    button4 = telebot.types.InlineKeyboardButton("��242_2", callback_data=f"{Group.KC242_2.name}")
    button5 = telebot.types.InlineKeyboardButton("��24_1",  callback_data=f"{Group.KN24_1.name}")
    button6 = telebot.types.InlineKeyboardButton("��24_2",  callback_data=f"{Group.KN24_2.name}")
    button7 = telebot.types.InlineKeyboardButton("��24",    callback_data=f"{Group.KT24.name}")
        
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5, button6, button7)
    
    sent_message = bot.send_message(message.chat.id, "������ ����� ����:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)    
    bot.send_message(call.message.chat.id, f"�� ������ �����: {call.data}")

    databaseManager.UpdateUserGroup(call.message.chat.id, call.data)

@bot.message_handler(commands=['print'])
def send_sheet_data(message):
    print(f"print call by {message.from_user.first_name}")
    try:
        cParts = message.text.split()
        if len(cParts) != 2:
            bot.send_message(
                message.chat.id,"���� �����, ������ ����� ������. ���������: /print 4")
            return

        if int(cParts[1]) - 1 < 0 or int(cParts[1]) - 1 > 17:
            raise IndexError("����� ������ �������� �� ��� ����������� �������� (1-17).")

        bot.send_message(message.chat.id, "���������...")

        bot.send_message(message.chat.id, GetSchedule(LoadWorkbook().worksheets[int(cParts[1]) - 1], Group.KN24_1.value, False))        


    except ValueError:
        bot.send_message(message.chat.id, "���� �����, ������ ��������� ����� ������. ���������: /print 4")
    except IndexError:
        bot.send_message(message.chat.id, "���� ������ � ����� �������. �������� �� ���.")
    except Exception as e:
        bot.send_message(message.chat.id, f"������� �������: {e}")

@bot.message_handler(commands=['compare'])
def compare(message):
    print(f"comparator call by {message.from_user.first_name}")
    try:
        cParts = message.text.split()
        if len(cParts) != 3:
            bot.send_message(message.chat.id, "���� �����, ������ ��� ������ ������� ��� ���������. ���������: /compare 4 5")
            return
        if int(cParts[1]) - 1 < 0 or int(cParts[1]) - 1 > 17 or int(cParts[2]) - 1 < 0 or int(cParts[2]) - 1 > 17:
            raise IndexError("����� ������ �������� �� ��� ����������� �������� (1-17).")

        bot.send_message(message.chat.id, "���������...")

        workbook = LoadWorkbook()
        schedule1 = GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KN24_1.value)
        schedule2 = GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KN24_1.value)

        bot.send_message(message.chat.id, CompareSchedules(schedule1, schedule2))

    except ValueError:
        bot.send_message(message.chat.id, "���� �����, ������ �������� ������ ������� ��� ���������. ���������: /compare 4 5")
    except IndexError:
        bot.send_message(message.chat.id, "���� ������ � ����� �������. �������� �� ���.")
    except Exception as e:
        bot.send_message(message.chat.id, f"������� �������: {e}")

@bot.message_handler(commands=['coolCompare'])
def coolCompare(message):
    print(f"coolComparator call by {message.from_user.first_name}")
    try:
        cParts = message.text.split()
        if len(cParts) != 3:
            bot.send_message(message.chat.id, "���� �����, ������ ��� ������ ������� ��� ���������. ���������: /coolCompare 4 5")
            return
        if int(cParts[1]) - 1 < 0 or int(cParts[1]) - 1 > 17 or int(cParts[2]) - 1 < 0 or int(cParts[2]) - 1 > 17:
            raise IndexError("����� ������ �������� �� ��� ����������� �������� (1-17).")

        bot.send_message(message.chat.id, "���������...")

        workbook = LoadWorkbook()
        schedule1 = GetSchedule(workbook.worksheets[int(cParts[1]) - 1], Group.KC242_2.value)
        schedule2 = GetSchedule(workbook.worksheets[int(cParts[2]) - 1], Group.KC242_2.value)

        bot.send_message(message.chat.id, ParseComparerOutput(CompareSchedules(schedule1, schedule2)), parse_mode='Markdown')

    except ValueError:
        bot.send_message(message.chat.id, "���� �����, ������ �������� ������ ������� ��� ���������. ���������: /compare 4 5")
    except IndexError:
        bot.send_message(message.chat.id, "���� ������ � ����� �������. �������� �� ���.")
    except Exception as e:
        bot.send_message(message.chat.id, f"������� �������: {e}")
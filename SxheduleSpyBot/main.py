from openpyxl import workbook
from csAutoCompiler import CompileAll
from dataProcessor import GetSchedule, CompareSchedules, LoadWorkbook
from botBase import bot

CompileAll()
print("Bot started...")

@bot.message_handler(commands=['print'])
def send_sheet_data(message):
    print("print call")
    try:        
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.send_message(message.chat.id, "Будь ласка, вкажіть номер аркуша. Наприклад: /print 4")
            return

        if int(command_parts[1]) - 1 < 0 or int(command_parts[1]) - 1 > 17:
            raise IndexError("Номер аркуша виходить за межі допустимого діапазону (1-17).")

        bot.send_message(message.chat.id, "Почекайте...")
        
        result = GetSchedule(LoadWorkbook(), int(command_parts[1]) - 1)
        bot.send_message(message.chat.id, result)
        print(result)

    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть коректний номер аркуша. Наприклад: /print 4")
    except IndexError:
        bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {e}")

@bot.message_handler(commands=['compare'])
def compare(messae):
    print("comparator call")
    try:
        command_parts = messae.text.split()
        if len(command_parts) != 3:
            bot.send_message(messae.chat.id, "Будь ласка, вкажіть два номери аркушів для порівняння. Наприклад: /compare 4 5")
            return
        if int(command_parts[1]) - 1 < 0 or int(command_parts[1]) - 1 > 17 or int(command_parts[2]) - 1 < 0 or int(command_parts[2]) - 1 > 17:
            raise IndexError("Номер аркуша виходить за межі допустимого діапазону (1-17).")
        bot.send_message(messae.chat.id, "Почекайте...")

        workbook = LoadWorkbook()
        schedule1 = GetSchedule(workbook, int(command_parts[1])-1)
        schedule2 = GetSchedule(workbook, int(command_parts[2])-1)
        print(schedule1)
        print(schedule2)
        result = CompareSchedules(f"{schedule1}",f"{schedule2}")
        print(f"result:{result}")
        bot.send_message(messae.chat.id, result)
        print(result)
    except ValueError:
        bot.send_message(messae.chat.id, "Будь ласка, введіть коректні номери аркушів для порівняння. Наприклад: /compare 4 5")
    except IndexError:
        bot.send_message(messae.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.")
    except Exception as e:
        bot.send_message(messae.chat.id, f"Сталася помилка: {e}")

bot.polling(none_stop=True)





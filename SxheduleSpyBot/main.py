from dataProcessor import GetSchedule
from botBase import bot

print("Bot started...")

@bot.message_handler(commands=['print'])
def send_sheet_data(message):
    try:        
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.send_message(message.chat.id, "Будь ласка, вкажіть номер аркуша. Наприклад: /print 4")
            return

        if int(command_parts[1]) - 1 < 0 or int(command_parts[1]) - 1 > 17:
            raise IndexError("Номер аркуша виходить за межі допустимого діапазону (1-17).")

        bot.send_message(message.chat.id, "Почекайте...")
        
        result = GetSchedule(int(command_parts[1]) - 1)
        bot.send_message(message.chat.id, result)
        print(result)

    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть коректний номер аркуша. Наприклад: /print 4")
    except IndexError:
        bot.send_message(message.chat.id, "Немає аркуша з таким номером. Перевірте ще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {e}")

bot.polling(none_stop=True)





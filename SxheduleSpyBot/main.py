from csAutoCompiler import CompileAll
from botBase import bot
from unIdler import StartUnIdler
import dataProcessor as dp
from enumerations import Group

CompileAll()
StartUnIdler()

print("Bot started...")

# parse test
workbook = dp.LoadWorkbook()
schedule1 = dp.GetSchedule(workbook.worksheets[6], Group.KC242_2.value)
schedule2 = dp.GetSchedule(workbook.worksheets[9], Group.KC242_2.value)
#print(dp.ParseSchedule(dp.CompareSchedules(schedule1, schedule2)))
bot.send_message(-1002499863221, dp.ParseSchedule(dp.CompareSchedules(schedule1, schedule2)), parse_mode='Markdown')

bot.polling(none_stop=True)
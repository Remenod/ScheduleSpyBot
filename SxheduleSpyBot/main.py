from csAutoCompiler import CompileAll
from botBase import bot
from unIdler import StartUnIdler

CompileAll()
#StartUnIdler()

print("Bot started...")

bot.polling(none_stop=True)
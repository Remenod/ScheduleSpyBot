from csAutoCompiler import CompileAll
from botBase import bot
from unIdler import StartUnIdler
from changesChecker import StartCheckerLoop

CompileAll()
#StartUnIdler()
#StartCheckerLoop(300)

print("Bot started...")

bot.polling(none_stop=True)
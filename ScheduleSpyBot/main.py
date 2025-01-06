from csAutoCompiler import CompileAll
# CompileAll()

from changesChecker import StartCheckerLoop
from botBase import bot
from logger import log
import botCommands

log("Bot started...")

# StartCheckerLoop(120)

bot.polling(none_stop=True)
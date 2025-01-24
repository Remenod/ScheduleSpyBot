from csAutoCompiler import CompileAll
CompileAll()

import botCommands # This import is necessary to register commands
from logger import log
from botBase import bot
from changesChecker import StartCheckerLoop

log("Bot started...")

# StartCheckerLoop(120)

bot.polling(none_stop=True)
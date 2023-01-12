import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler, \
    messagequeue as mq

from game import sim_o, sim_x, start_game
from toc import TOKEN_FOR_BOT


def start(bot, update):
    text = 'Для того чтобы начать играть введите: /start_game.' \
           ' Если во время игры ввести "stop", то игра прервется'
    update.message.reply_text(text)


def interceptor(bot, update):
    global board
    if update.message.text == "stop":
        return ConversationHandler.END
    else:
        update.message.reply_text("Некорректный ввод. Вы уверены, что ввели число от 1 до 9?")


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot.log'
                        )
    updater = Updater(TOKEN_FOR_BOT)

    updater.bot._msg_queue = mq.MessageQueue()
    updater.bot._is_messages_queued_default = True

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_game", start_game)],

        states={
            "S_X": [RegexHandler('^(1|2|3|4|5|6|7|8|9)$', sim_x)],
            "S_O": [RegexHandler('^(1|2|3|4|5|6|7|8|9)$', sim_o)],
        },

        fallbacks=[MessageHandler(Filters.text, interceptor)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
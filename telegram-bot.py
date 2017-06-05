#!/usr/bin/python
# -*- coding: utf-8 -*-
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
from security import encrypt
from security import decrypt
import os
from extractLines import getFormatedLines
from bs4 import BeautifulSoup
from telegram import Emoji
userName = ''
passwd = ''
token_key = 'XXXXXXXX'
updater = Updater(token=token_key)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def getCredentials(password):
    in_filename = 'credentialsEnc'
    out_filename = 'credentials'
    print len(password)
    lines = []
    # with open(out_filename, 'rb') as in_file, open(in_filename, 'wb') as out_file:
    #      encrypt(in_file, out_file, password)

    with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
        decrypt(in_file, out_file, password)
    with open(out_filename, 'rb') as in_file:
        lines = [line for line in in_file]

    os.remove(out_filename)
    return lines


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hola penya! Teniu que dir-me el password")


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def paga(bot, update, args):

    # import subprocess
    # bash_command='../gardenWeb/generateChart.gp'
    # process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    #     output = process.communicate()[0]
    #
    # bash_command='inkscape -z -e introduction.png  ../gardenWeb/public/charts/introduction.svg'
    # process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    # output = process.communicate()[0]
    # bot.sendPhoto(chat_id=update.message.chat_id, photo=open('introduction.png', 'rb'))
    text_caps = getFormatedLines()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps, parse_mode=telegram.ParseMode.MARKDOWN)


def empty_message(bot, update):
    """
    Empty messages could be status messages, so we check them if there is a new
    group member, someone left the chat or if the bot has been added somewhere.
    """

    if update.message.new_chat_members is not None:
            return welcome(bot, update)


def welcome(bot, update):
    """ Welcomes a user to the chat """

    message = update.message
    chat_id = message.chat.id

    # Pull the custom message for this chat from the database
    text = 'Hola $username! Benivingut al grup de la $title %s' % Emoji.GRINNING_FACE_WITH_SMILING_EYES

    # Replace placeholders and send message
    text = text.replace('$username',
                        message.new_chat_members.first_name.encode('utf-8'))\
        .replace('$title', message.chat.title)
    send_async(bot, chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def passwd(bot, update, args):
    credentials = getCredentials(args[0].encode('utf-8'))
    userName = credentials[0]
    passwd = credentials[1]
    bot.sendMessage(chat_id=update.message.chat_id, text='Perfecte!')



start_handler = CommandHandler('start', start)
paga_handler = CommandHandler('paga', paga, pass_args=True)
passwd_handler = CommandHandler('passwd', passwd, pass_args=True)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(paga_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(passwd_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(MessageHandler(Filters.status_update, empty_message))


updater.start_polling()
updater.idle()

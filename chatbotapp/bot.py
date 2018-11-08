from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bot = ChatBot('kutumbitaBot')
bot.set_trainer(ListTrainer)


def init_bot():

    files = BASE_DIR + '/chatbotapp/files'
    for _file in os.listdir(files):
        chats = open(files + '/' + _file, 'r').readlines()
        bot.train(chats)


def get_response(user_response):
    return str(bot.get_response(user_response))

if __name__ == "__main__":
    print(get_response("hello"))
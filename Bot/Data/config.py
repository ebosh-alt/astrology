from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
link_to_bot = "https://t.me/manager_example_bot"
openai_key = env("ANTHROPIC_API_KEY")
STRIPE_API_KEY = env("STRIPE_API_KEY")
LINK_SUPPORT = env("LINK_SUPPORT")
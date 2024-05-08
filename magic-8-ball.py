from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder
import random
import time

app = ApplicationBuilder().token("6893681698:AAHlkwoL77nQ3A1MNLixoDZffmTxt7B95j8").build()

answer_list = ['Yes, Ratmir is gay', 'Meow', 'Ask your friend for advice' , 'It is certain', 'Reply hazy, try again', 'Don’t count on it', 'It is decidedly so', 'Ask again later', 'My reply is no', 'Without a doubt', 'Better not tell you now', 'My sources say no', 'Yes definitely', 'Cannot predict now', 'Outlook not so good', 'You may rely on it', 'Concentrate and ask again', 'Very doubtful', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes']
def generate_answer():
    number = random.randint(0, len(answer_list)-1)
    return answer_list[number]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/ask [your question] to answer your most confusing question.\n/reroll to get a different answer(once per question)\n/history to view past questions and answers\n/new [custom answer] to add custom answers\n/remove to remove existing answer from list")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    answer = generate_answer()
    await update.message.reply_text('Shuffling...')
    time.sleep(3)
    await update.message.reply_text(answer)

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I hear: " + update.message.text)

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get actual data from database
    question = 'question'
    first_answer = 'answer 1'
    rerolled = True
    if rerolled:
        second_answer = 'answer 2'
        message = f'Question: {question}\nInitial Answer: {first_answer}\nAfter rerolling the answer was:\n{second_answer}'
    else:   
        message = f'Question: {question}\nAnswer: {first_answer}\nThe ball was not rerolled'
    print(message)
    await update.message.reply_text(message)

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer_list.append(update.message.text)
    await update.message.reply_text('New answer succesfully added')

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = 1
    keyboard_list = []
    keyboard = []
    for answer in answer_list:
        keyboard_list.append(f'InlineKeyboardButton("{answer}", callback_data="{count}")')
        count +=1
    print(keyboard_list)
    keyboard.append(keyboard_list)
    print(keyboard)
    keyboard = [
        [InlineKeyboardButton("test", callback_data="1")],
        [InlineKeyboardButton("test2", callback_data="2")],
        [InlineKeyboardButton("test3", callback_data="3")],
        [InlineKeyboardButton("test4", callback_data="4")],
        [InlineKeyboardButton("test5", callback_data="5")],

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    # await update.message.reply_text('Answer not found. Try again')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reroll", reroll))
app.add_handler(CommandHandler("ask", answer))
app.add_handler(CommandHandler("new", new))
app.add_handler(CommandHandler("remove", remove))

app.run_polling()

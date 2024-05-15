from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder
import random
import time
import json

with open("user_history.json",'r') as file:
    user_history = json.load(file)

def save():
    with open("user_history.json", "w") as file:
        json.dump(user_history, file)


app = ApplicationBuilder().token("6893681698:AAHlkwoL77nQ3A1MNLixoDZffmTxt7B95j8").build()

answer_list = ['Meow', 'Ask your friend' , 'It is certain', 'Reply hazy, try again', 'Don’t count on it', 'It is decidedly so', 'Ask again later', 'My reply is no', 'Without a doubt', 'Better not tell you now', 'My sources say no', 'Yes definitely', 'Cannot predict now', 'Outlook not so good', 'You may rely on it', 'Concentrate and ask again', 'Very doubtful', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes']

def generate_answer():
    number = random.randint(0, len(answer_list)-1)
    return answer_list[number]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/ask [your question] to answer your most confusing question.\n/reroll to get a different answer(once per question)\n/history to view last 10 questions\n/new [custom answer] to add custom answers\n/remove to remove existing answer from list")


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user['id']
    question = update.message.text.replace('/ask', '').strip()
    if str(user_id) not in user_history:
        user_history[user_id] = []
    save()
    if question:
        answer = generate_answer()
        user_history[user_id].append({"question" : question, "answer_1" : answer, "rerolled" : False, "answer_2" : None})
        save()
        await update.message.reply_text('Shuffling...')
        time.sleep(3)
    else:
        answer = 'No question provided.'
    await update.message.reply_text(answer)

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user['id']
    if user_history[user_id][-1]['rerolled'] == False:
        answer = generate_answer()
        user_history[user_id][-1]['answer_2'] = answer
        user_history[user_id][-1]['rerolled'] = True
        save()
        await update.message.reply_text('Shuffling...')
        time.sleep(3)
    else:
        answer = 'You have already rerolled on this question'
    await update.message.reply_text(answer)

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here is the history of your last 10 rounds:')
    user_id = str(update.message.from_user['id'])
    reversed_history = user_history
    # reversed_history[user_id].reverse()
    if reversed_history[user_id]:
        try:
            for i in range(10):
                question = reversed_history[user_id][i]['question']
                answer_1 = reversed_history[user_id][i]['answer_1']
                rerolled = reversed_history[user_id][i]['rerolled']
                if rerolled:
                    answer_2 = reversed_history[user_id][i]['answer_2']
                    message = f'Question: {question}\nInitial Answer: {answer_1}\nAfter rerolling the answer was:\n{answer_2}'
                else:   
                    message = f'Question: {question}\nAnswer: {answer_1}\nThe ball was not rerolled'
                messages.append(message)
        except Exception as e:
            pass
    else:
        await update.message.reply_text('You dont have any history yet.')
        

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_answer = update.message.text.replace('/new', '').strip()
    if new_answer:
        answer_list.append(new_answer)
        message = 'New answer succesfully added'
    else:
        message = 'No answer provided'
    await update.message.reply_text(message)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    count = 0
    keyboard = [[InlineKeyboardButton('-cancel-', callback_data=-1)]]
    for answer in answer_list:
        keyboard.append([InlineKeyboardButton(answer, callback_data=count)])
        count +=1
    print(keyboard)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose which answer you want removed:", reply_markup=reply_markup)
    # await update.message.reply_text('Answer not found. Try again')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    callback_data = int(query.data)
    if callback_data == -1:
        message="No answers were removed."
    else:
        answer_list.remove(answer_list[callback_data])
        message="Answer succesfully removed."
    await query.edit_message_text(message)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reroll", reroll))
app.add_handler(CommandHandler("ask", answer))
app.add_handler(CommandHandler("new", new))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("history", history))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()

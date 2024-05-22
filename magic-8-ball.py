from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder
import random
import time
import json

with open("user_history.json",'r') as file:
    user_history = json.load(file)

def save():
    with open("user_history.json", "w") as file:
        json.dump(user_history, file)

async def shuffling(update, context, answer):
    shuffling_message = await update.message.reply_text('🎱 Shuffling')
    for _ in range(2): #repeats the shuffling animation 2 times
        time.sleep(0.5)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=shuffling_message.message_id, text="🎱 Shuffling.")
        time.sleep(0.5)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=shuffling_message.message_id, text="🎱 Shuffling..")
        time.sleep(0.5)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=shuffling_message.message_id, text="🎱 Shuffling...")
        time.sleep(0.5)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=shuffling_message.message_id, text="🎱 Shuffling")
    await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=shuffling_message.message_id, text=answer)


app = ApplicationBuilder().token("6893681698:AAHlkwoL77nQ3A1MNLixoDZffmTxt7B95j8").build()

answer_list = ['Meow', 'It is certain', 'Reply hazy, try again', 'Don’t count on it', 'It is decidedly so', 'Ask again later', 'My reply is no', 'Without a doubt', 'Better not tell you now', 'My sources say no', 'Yes definitely', 'Cannot predict now', 'Outlook not so good', 'You may rely on it', 'Concentrate and ask again', 'Very doubtful', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes']

def generate_answer(user_id):
    if user_history[user_id]['answer_list']: #Check if answer_list exists
        number = random.randint(0, len(user_history[user_id]['answer_list'])-1)
        return user_history[user_id]['answer_list'][number]
    else:
        return 'Answer list is empty, add to it using /add [answer]'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/ask [your question] to answer your most confusing question.\n/reroll to get a different answer(once per question)\n/history to view last 10 questions\n/add [custom answer] to add custom answers\n/remove to remove existing answer from list")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user['id'])
    question = update.message.text.replace('/ask', '').strip()
    if user_id not in user_history: #Checks if user is not already in the history
        user_history[user_id] = {
            'history' : [],
            'answer_list' : answer_list
                }
    save()
    if question: #Check if a question was provided
        answer = generate_answer(user_id)
        user_history[user_id]['history'].append({"question" : question, "answer_1" : answer, "rerolled" : False, "answer_2" : None})
        save()
        await shuffling(update, context, answer)
    else:
        await update.message.reply_text('No question provided')

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user['id'])
    if user_history[user_id]['history'][-1]['rerolled'] == False: #Checks if for the last question the user has ont rerolled the ball
        answer = generate_answer(user_id)
        user_history[user_id]['history'][-1]['answer_2'] = answer
        user_history[user_id]['history'][-1]['rerolled'] = True
        save()
        await shuffling(update, context, answer)
    else:
        await update.message.reply_text('You have already rerolled on this question')

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here is the history of your last 10 rounds:')
    user_id = str(update.message.from_user['id'])
    user_history[user_id]['history'][::-1]
    messages = []
    if user_history[user_id]['history']: #Check if history exists for a certain user
        try:
            for i in range(10): #Shows the last 10 questions asked
                question = user_history[user_id]['history'][i]['question']
                answer_1 = user_history[user_id]['history'][i]['answer_1']
                rerolled = user_history[user_id]['history'][i]['rerolled']
                if rerolled: #Check if the the ball has been rerolled
                    answer_2 = user_history[user_id]['history'][i]['answer_2']
                    message = f'❔ <b>Question:</b> {question}\n<b>❌ Initial Answer:</b> {answer_1}\n<b>🎱 Answer after reroll:</b> {answer_2}'
                else:   
                    message = f'❔ <b>Question:</b> {question}\n<b>🎱 Answer:</b> {answer_1}'
                await update.message.reply_text(message, parse_mode='HTML')
        except:
            pass
    else:
        await update.message.reply_text('You dont have any history yet')
        

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user['id'])
    new_answer = update.message.text.replace('/add', '').strip()
    if new_answer: #Check if new_answer was provided
        user_history[user_id]['answer_list'].append(new_answer)
        message = 'New answer succesfully added'
        save()
    else:
        message = 'No answer provided'
    await update.message.reply_text(message)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user['id'])
    count = 0
    keyboard = [[InlineKeyboardButton('-CANCEL-', callback_data=-1)]]
    for answer in user_history[user_id]['answer_list']: #goes over each answer in the answer list to add it as a button
        keyboard.append([InlineKeyboardButton(answer, callback_data=count)])
        count +=1
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose which answer you want removed:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.callback_query.from_user['id'])
    query = update.callback_query
    await query.answer()
    callback_data = int(query.data)
    if callback_data == -1: #Checks if the callback_data value is -1(canceling removal)
        message="No answer removed"
    else:
        user_history[user_id]['answer_list'].remove(user_history[user_id]['answer_list'][callback_data])
        message="Answer succesfully removed"
        save()
    await query.edit_message_text(message)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reroll", reroll))
app.add_handler(CommandHandler("ask", answer))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("history", history))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()

from itertools import count

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler, ContextTypes

from credentials import ChatGPT_TOKEN,TELEBOT_TOKEN
from gpt import ChatGptService
from util import load_message, load_prompt, send_text_buttons, send_text, \
    send_image, show_main_menu, Dialog, default_callback_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'main'
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓',
        'recommend': 'Получить рекомендацию для фильма или книги'
        # Добавить команду в меню можно так:
        # 'command': 'button text'

    })

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'gpt'
    promt = load_prompt('gpt')
    message = load_message('gpt')
    chat_gpt.set_prompt(promt)
    await send_image(update, context, 'gpt')
    await send_text(update, context, message)

count = 0
async def gpt_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global count
    text = update.message.text
    message = await  send_text(update, context, "Думаю, что ответить")
    answer =  await chat_gpt.add_message(text)
    if answer == 'Правильно!':
        count +=1
        answer == (answer,'- Количество правильных ответов',count) #Почему-то не работает надо проверить, хотя счетчик отрабатывает
        await message.edit_text(answer)
        await message.edit_text(f'Количество правильных ответов: {count}')
    else:
        await message.edit_text(answer)
    if dialog.mode == 'quiz':
        await send_text_buttons(update, context, "Выбор темы для нового вопроса:", {
            'quiz_prog': 'Программирование на языке python',
            'quiz_math': 'Математические теории',
            'quiz_biology': 'Биология',
            'quiz_more': 'Вопрос по той же теме'
        })

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Создание кнопок для диалогов с известными личностями
    """

    dialog.mode = 'talk'
    message = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text_buttons(update, context,message,{
        'talk_cobain':'Поговорить с Кобейном',
        'talk_hawking':'Поговорить с Хокингом',
        'talk_nietzsche':'Поговорить с Ницше',
        'talk_queen':'Поговорить с Елизпветой ||',
        'talk_tolkien':'Поговорить с Толкиеным'
    })

async def talk_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Обработчик кнопок выбора диалога с известной личностью
    """

    await update.callback_query.answer()
    cb = update.callback_query.data
    if cb == 'talk_cobain':
        promt = load_prompt('talk_cobain')
        chat_gpt.set_prompt(promt)
        await send_image(update, context, 'talk_cobain')
        await send_text(update, context, 'Курт! Хороший выбор! Можете задать вопрос:')
    elif cb == 'talk_hawking':
        promt = load_prompt('talk_hawking')
        chat_gpt.set_prompt(promt)
        await send_image(update, context, 'talk_hawking')
        await send_text(update, context, 'Хокинг приветсвует вас! Можете задать вопрос:')
    elif cb == 'talk_nietzsche':
        promt = load_prompt('talk_nietzsche')
        chat_gpt.set_prompt(promt)
        await send_image(update, context, 'talk_nietzsche')
        await send_text(update, context, 'Добрый друг, вас приветствует известный философ! Можете задать вопрос:')
    elif cb == 'talk_queen':
        promt = load_prompt('talk_queen')
        chat_gpt.set_prompt(promt)
        await send_image(update, context, 'talk_queen')
        await send_text(update, context, 'Вам посчастливилось пообщаться с Английской Королевой! Можете задать вопрос, но не усердствуйте, старушка совсем плоха:')
    elif cb == 'talk_tolkien':
        promt = load_prompt('talk_tolkien')
        chat_gpt.set_prompt(promt)
        await send_image(update, context, 'talk_tolkien')
        await send_text(update, context, 'Вас приветствует репетитор эльфийского языка! Можете задать вопрос:')
    else:
        await send_text(update, context, 'Вы выбрали личность не из списка')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Создание нового квиза
    """
    dialog.mode = 'quiz'
    message = load_message('quiz')
    await send_image(update, context, 'quiz')
    await send_text_buttons(update, context,message,{
        'quiz_prog':'Программирование на языке python',
        'quiz_math':'Математические теории',
        'quiz_biology':'Биология'
    })

button = ''
async def quiz_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Функция управления кнопками квиза
    """

    global button
    await update.callback_query.answer()
    cb = update.callback_query.data
    promt = load_prompt('quiz')
    chat_gpt.set_prompt(promt)
    if cb == 'quiz_prog':
        button = 'quiz_prog'
        message = await  send_text(update, context, "Думаю, над вопросом")
        answer = await chat_gpt.send_question(promt, 'quiz_prog')
        await message.edit_text(answer)
    elif cb == 'quiz_math':
        button = 'quiz_math'
        message = await  send_text(update, context, "Думаю, над вопросом")
        answer = await chat_gpt.send_question(promt, 'quiz_math')
        await message.edit_text(answer)
    elif cb == 'quiz_biology':
        button = 'quiz_biology'
        message = await  send_text(update, context, "Думаю, над вопросом")
        answer = await chat_gpt.send_question(promt, 'quiz_biology')
        await message.edit_text(answer)
    elif cb == 'quiz_more':
        message = await  send_text(update, context, "Думаю, над вопросом")
        answer = await chat_gpt.send_question(promt, button)
        await message.edit_text(answer)

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Функция, которая выдает категории для рекомендаций фильмам или книгам
    """

    dialog.mode = 'recommend'
    message = load_message('recommend')
    await send_image(update, context, 'recommend')
    await send_text_buttons(update, context, message, {
        'recommend_books': 'Книги',
        'recommend_films': 'Фильмы'
    })

async def recommend_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Функция, обработки кнопок для выбора рекомендаций
    """

    await update.callback_query.answer()
    cb = update.callback_query.data
    if cb == 'recommend_books':
        promt = 'Подбери список книг исходя из запроса пользователя'
        await  send_text(update, context, "Укажите автора, жанр и любую другую информацию для рекомендации книги")
    elif cb == 'recommend_films':
        promt = 'Подбери список фильмов исходя из запроса пользователя'
        await  send_text(update, context, "Укажите режиссера, актеров, жанр и любую другую информацию для рекомендации фильма")
    chat_gpt.set_prompt(promt)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Функция, которая принимает сообщение пользователя и проверяет режим приложения, если режим не задан, то отсылает пользователю в ответ текст полученного сообщения.
    """

    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'talk':
        await gpt_dialog(update, context)
    elif dialog.mode == 'quiz':
        await gpt_dialog(update, context)
    elif dialog.mode == 'recommend':
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, update.message.text)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Функция выдает рандомный интересный факт
    """

    promt = load_prompt('random')
    message = load_message('random')
    await send_image(update, context, 'random')
    message = await send_text(update, context, message)
    answer = await chat_gpt.send_question(promt, '')
    await message.edit_text(answer)


dialog = Dialog()
dialog.mode = None
# Переменные можно определить, как атрибуты dialog

chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token(TELEBOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)) #~filters.COMMAND исключает команды из обработки
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(CommandHandler('recommend', recommend))

# Зарегистрировать обработчик команды можно так:
# app.add_handler(CommandHandler('command', handler_func))

# Зарегистрировать обработчик кнопки можно так:
app.add_handler(CallbackQueryHandler(talk_button, pattern='^talk.*'))
app.add_handler(CallbackQueryHandler(quiz_button, pattern='^quiz.*'))
app.add_handler(CallbackQueryHandler(recommend_button, pattern='^recommend.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()

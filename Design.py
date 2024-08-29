import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, 
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, 
                          ContextTypes, ConversationHandler, MessageHandler, filters)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger("DesignGenie")

PROJECT_GOALS, PROJECT_OBJECTIVES, TARGET_AUDIENCE, DESIRED_OUTCOME, PROJECT_TIMELINE, PROJECT_BUDGET = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the client about their project goals."""
    reply_keyboard = [['Tell me about your project goals']]
    await update.message.reply_text(
        '<b>Добро пожаловать в Telegram-бот веб-студии!\n'
        'I\'m here to help you brief your project. Let\'s get started!\n'
        'Каковы цели вашего проекта?</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return PROJECT_GOALS

async def project_goals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client's project goals and asks about their objectives."""
    user = update.message.from_user
    context.user_data['project_goals'] = update.message.text
    logger.info('Project goals of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        '<b>Каковы цели вашего проекта?</b>',
        parse_mode='HTML',
    )
    return PROJECT_OBJECTIVES

async def project_objectives(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client's project objectives and asks about their target audience."""
    user = update.message.from_user
    context.user_data['project_objectives'] = update.message.text
    logger.info('Project objectives of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        '<b>Кто ваша целевая аудитория?</b>',
        parse_mode='HTML',
    )
    return TARGET_AUDIENCE

async def target_audience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client's target audience and asks about their desired outcome."""
    user = update.message.from_user
    context.user_data['target_audience'] = update.message.text
    logger.info('Target audience of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        '<b>Какой результат вы хотите достичь?</b>',
        parse_mode='HTML',
    )
    return DESIRED_OUTCOME

async def desired_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client's desired outcome and asks about their project timeline."""
    user = update.message.from_user
    context.user_data['desired_outcome'] = update.message.text
    logger.info('Desired outcome of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        '<b>Какой срок реализации проекта?</b>',
        parse_mode='HTML',
    )
    return PROJECT_TIMELINE

async def project_timeline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client's project timeline and asks about their budget."""
    user = update.message.from_user
    context.user_data['project_timeline'] = update.message.text
    logger.info('Project timeline of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        '<b>Какой бюджет проекта?</b>',
        parse_mode='HTML',
    )
    return PROJECT_BUDGET

async def project_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the client"""

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("7538710302:AAEvIgAb-Fi9biTxEVsGplSZyaqeTLK_Irc").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Начало', start)],
        states={
            PROJECT_GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_goals)],
            PROJECT_OBJECTIVES: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_objectives)],
            TARGET_AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_audience)],
            DESIRED_OUTCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, desired_outcome)],
            PROJECT_TIMELINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_timeline)],
            PROJECT_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_budget)],
        },
        fallbacks=[CommandHandler('Назад', cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()
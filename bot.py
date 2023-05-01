import os
from google.cloud import language_v1
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
import telegram_token

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/niksol/.config/gcloud/application_default_credentials.json'

client = language_v1.LanguageServiceClient()


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привіт, я можу визначати емоційний зміст твоїх повідомлень! Емоційне забарвлення визначаєься" \
             "наступними характеристиками: score(-1 - дуже негативне повідомлення, +1 - дуже позитивне), " \
             "magnitude від 0 до нескінченності - ознчає силу забарвленості"
    )


async def handle_message(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    response = "Емоційне забарвлення: score = {:.2f}, magnitude = {:.2f}".format(sentiment.score, sentiment.magnitude)

    await context.bot.send_message(chat_id=chat_id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_token.BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

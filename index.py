import logging
import time
import random
from pytube import YouTube
from pydub import AudioSegment
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from instaloader import Instaloader, Profile
from youtubesearchpython import VideosSearch
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from youtubesearchpython import VideosSearch

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

OWNERS_IDS = [
    6996992405,
    6085506230,
    2345678901,
    3456789012,
    4567890123
]

IMAGE_PATH = '/home/usuario/ChestyBot/imágenes uwu/images.jpg'

start_time = time.time()
unique_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unique_users.add(update.effective_user.id)
    welcome_text = "Hola, soy un bot. ¿En qué puedo ayudarte?\n\nEscribe '/help' para ver mis comandos"
    keyboard = [[InlineKeyboardButton("GitHub de mi creador", url="https://www.github.com/matias-crypto")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, reply_markup=reply_markup)

async def search_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el texto de búsqueda.")
        return

    query = " ".join(context.args)
    loader = Instaloader()
    profiles = loader.get_hashtag_posts(query)
    videos = []
    for post in profiles:
        if post.typename == 'GraphVideo':
            videos.append(post.url)

    if videos:
        message_text = f"Encontré los siguientes videos de Instagram:\n"
        for video in videos:
            message_text += f"{video}\n"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se encontraron videos de Instagram para el texto de búsqueda.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in OWNERS_IDS:
        if context.args:
            user_to_ban = int(context.args[0])
            BANNED_USERS.add(user_to_ban)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Usuario {user_to_ban} baneado.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el ID del usuario a banear.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No tienes permiso para usar este comando.")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in OWNERS_IDS:
        if context.args:
            user_to_unban = int(context.args[0])
            if user_to_unban in BANNED_USERS:
                BANNED_USERS.remove(user_to_unban)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Usuario {user_to_unban} desbaneado.")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"El usuario {user_to_unban} no está en la lista de baneados.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el ID del usuario a desbanear.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No tienes permiso para usar este comando.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in OWNERS_IDS:
        if context.args:
            message_text = " ".join(context.args)
            for user in BANNED_USERS:
                await context.bot.send_message(chat_id=user, text=message_text)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Mensaje enviado a todos los usuarios baneados.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el mensaje a enviar.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No tienes permiso para usar este comando.")

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el nombre de la canción o del video.")
        return

    query = " ".join(context.args)
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    if result['result']:
        video_info = result['result'][0]
        video_title = video_info['title']
        video_link = video_info['link']
        message_text = f"¡Hecho! Resultado de la canción/video:\n{video_title}\n{video_link}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se encontraron resultados.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ChestyBot: Telegram bot\n\n"
        "Comandos disponibles:\n\n"
        "/start - Inicia el bot\n"
        "/help - Muestra este menú de comandos\n"
        "/image - Envía una imagen\n"
        "/echo - Repite tu mensaje\n"
        "/info - Proporciona información sobre el bot\n"
        "/stop - Detiene la ejecución del bot\n"
        "/setname - Cambia el nombre del bot (comando exclusivo para owners)\n"
        "/estado - Muestra el tiempo activo y usuarios que interactuaron con el bot\n"
        "/searchyt - Busca música/videos en YouTube\n"
        "/searchinstagram - Busca videos de ig\n"
        "/ppt - Piedra, papel o tijera\n"
        "/ban/unban - Banear/desbanear usuarios (solo owners del bot)\n"
        "/broadcast - enviar mensajes a usuarios baneados (solo owners)"
    )

    keyboard = [
        [InlineKeyboardButton("Visita mi GitHub", url="https://www.github.com/matias-crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(IMAGE_PATH, 'rb') as image:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(image), caption=help_text, reply_markup=reply_markup)

async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unique_users.add(update.effective_user.id)
    with open(IMAGE_PATH, 'rb') as image:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(image))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unique_users.add(update.effective_user.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def ppt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = ["piedra", "papel", "tijera"]
    bot_choice = random.choice(options)
    user_choice = context.args[0].lower() if context.args else None

    if user_choice not in options:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, elige entre 'piedra', 'papel' o 'tijera'.")
        return

    if user_choice == bot_choice:
        result_text = f"Empate! Ambos elegimos {user_choice}."
    elif (user_choice == "piedra" and bot_choice == "tijera") or (user_choice == "papel" and bot_choice == "piedra") or (user_choice == "tijera" and bot_choice == "papel"):
        result_text = f"¡Ganaste! Elegiste {user_choice} y yo elegí {bot_choice}."
    else:
        result_text = f"¡Perdiste! Elegiste {user_choice} y yo elegí {bot_choice}."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=result_text)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unique_users.add(update.effective_user.id)
    info_text = (
        "Soy un bot creado para demostrar las capacidades de la imaginación . "
        "Puedes encontrar mi código en GitHub en el usuario de matias-crypto (aún no está posible)."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Deteniendo el bot...")
    context.application.stop()

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in OWNERS_IDS:
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona un nuevo nombre.")
            return
        new_name = " ".join(context.args)
        await context.bot.set_my_description(new_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Nombre del bot cambiado a: {new_name}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No tienes permiso para usar este comando.")

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    elapsed_time = time.time() - start_time
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_seconds = int(elapsed_time % 60)
    user_count = len(unique_users)

    estado_text = (
        f"El bot ha estado activo por: {elapsed_hours} horas, {elapsed_minutes} minutos y {elapsed_seconds} segundos.\n"
        f"Número de usuarios que interactuaron con el bot: {user_count}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=estado_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7241645978:AAGtwfh4Zj8p--qnecrgEsc5QrJUpgBdPD4').build()

        application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('image', send_image))
    application.add_handler(CommandHandler('echo', echo))
    application.add_handler(CommandHandler('info', info))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('setname', set_name))
    application.add_handler(CommandHandler('estado', estado))
    application.add_handler(CommandHandler('searchyt', search_music))
    application.add_handler(CommandHandler('ppt', ppt))
    application.add_handler(CommandHandler('ban', ban))
    application.add_handler(CommandHandler('unban', unban))
    application.add_handler(CommandHandler('broadcast', broadcast))
    application.run_polling()
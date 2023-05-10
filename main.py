import os
import loguru
import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="n.", intents=intents, test_guilds=[1100160648182243359])

# ID роли "Новичок"
NEWCOMER_ROLE_ID = 1100318142410002432

# Функция для выдачи роли новичка
@bot.event
async def on_member_join(member):
    newcomer_role = member.guild.get_role(NEWCOMER_ROLE_ID)
    await member.add_roles(newcomer_role)

activity = disnake.Activity(type=disnake.ActivityType.watching, application_id="1100405395157172304", name="n.help", state='Всем сыркам', details='сырной жизни!', large_image_url='https://media.discordapp.net/attachments/553824595237666841/1101927149759377418/photo_2023-04-24_03-20-15.jpg?width=669&height=669')

# Обработчик события запуска бота
@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    logger.info(f"{bot.user} запущен.")

# Инициализируем логгер
logger = loguru.logger

# ID канала, в который будут отправляться логи
log_channel_id = 1102634719377637468

# Настройки логгера
logger.add("bot.log", rotation="1 day")

# Список имен команд, которые нужно логгировать
tracked_commands = ['таймаут', 'антаймаут', 'бан', 'анбан', 'чистка', 'grole', 'sender', 'варн', 'анварн']


# Обработчик события использования Slash-команды
@bot.event
async def on_application_command(ctx):
    if ctx.data.get('name') in tracked_commands:
        logger.info(f"{ctx.author} использовал Slash-команду {ctx.data.get('name')} в канале {ctx.channel}.")

        # Получаем объект канала, в который нужно отправить лог
        log_channel = bot.get_channel(log_channel_id)

        if log_channel is None:
            logger.warning(f"Канал для логов с ID {log_channel_id} не найден на сервере.")
            return

        if log_channel:
            # Отправляем лог в канал
            await log_channel.send(
                f"{ctx.author} использовал Slash-команду {ctx.data.get('name')} в канале {ctx.channel}.")

    # Обработка команды
    await bot.process_application_commands(ctx)

# Список запрещенных слов
forbidden_words = ["негр", "пидор", "чмо", "уёбище", "шлюха", "выблядок", "сын портовой шлюхи"]

@bot.event
async def on_message(message):
    # Проверяем, является ли автор сообщения ботом
    if message.author.bot:
        return
    # Проверяем, содержит ли сообщение запрещенные слова
    for word in forbidden_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention}, сообщения, содержащие запрещенные слова, запрещены.")
            return

@bot.event
async def on_command_error(ctx, error):
    """Перехват ошибок команд"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена.")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run('secret') # токен бота

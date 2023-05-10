import disnake
from disnake.ext import commands

class AdminSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='sender')
    @commands.has_any_role(1100165777283354704, 1102721161089007646, 1100166446367117363)
    async def send_message(self, ctx, user: disnake.User, *, message: str):
        """Отправляет сообщение пользователю в ЛС"""
        admin_name = ctx.author.name
        # Формируем текст сообщения
        await ctx.send('Сообщение отправлено!')
        text = f"Администратор {admin_name} написал(а) вам: {message}"
        # Отправляем сообщение пользователю в ЛС от имени бота
        await user.send(text)

def setup(bot):
    bot.add_cog(AdminSender(bot))


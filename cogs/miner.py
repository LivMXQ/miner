import discord
import user
import pickle
from replit import db
from cogs.error import UserNotInDb
from discord.ext import commands
from discord.ui import Button, View

cooldowns = dict()
registeredviews = list()
currentview = None

admin_users = ["714826336102907976","895289342497538059", "808223912688746496"]#hegen, liv, dwizard 

class endinteractionbtn(Button):
    def __init__(self, row=1):
        super().__init__(label="End Interaction")

    async def callback(self, interaction):
        await currentview.disable_all()
        await interaction.response.edit_message(view=currentview)


def initialize_cooldowns(cooldowns_):
    for i in db["users"]:
        user_id = i
        duration = 17.5
        cooldowns_[user_id] = commands.CooldownMapping.from_cooldown(
            1, duration, commands.BucketType.user)


class view_timeout(View):
    def __init__(self, ctx, timeout=10):
        super().__init__(timeout=timeout)
        self.inactive = False
        self.ctx = ctx

    async def on_timeout(self):
        if self.inactive == False:
            for i in self.children:
                i.disabled = True
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "That's not your miner bro", ephemeral=True)
            return False
        else:
            return True


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        initialize_cooldowns(cooldowns)

    def check_cooldown():
        async def predicate(ctx):
            user_id = str(ctx.author.id)
            if user_id in admin_users:
                return True
            else:
                if user_id in cooldowns:
                    bucket = cooldowns[user_id].get_bucket(ctx.message)
                    retry_after = bucket.update_rate_limit()
                    if retry_after:
                        raise commands.CommandOnCooldown(
                            bucket, retry_after, commands.BucketType.user)
                else:
                    raise UserNotInDb(ctx.author)
                return True

        return commands.check(predicate)

    def check_if_in_db():
        async def predicate(ctx):
            user_ = user.User(ctx.author)
            if not user_.check_if_in_db():
                raise UserNotInDb(ctx.author)
            return True

        return commands.check(predicate)

    @commands.command(name="distribution", aliases=["dist"])
  
    async def distrubution(self, ctx):
        embed = discord.Embed(title="Miner Ore Distributing Chart")
        embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
        await ctx.send(embed=embed)

    @commands.command(name="mine", aliases=["dig"])
    @check_cooldown()
    @check_if_in_db()
    async def mine(self, ctx):
      user_ = user.User(ctx.author)
      embed = user_.mine_()
      await ctx.send(embed=embed)
      
    
    @commands.command(name="returntobase", aliases=["rtb"])
    async def returntobase(self, ctx):
        user_ = user.User(ctx.author)
        if user_.return_to_basetobase():
            await ctx.send("You Successfully returned to base!")
        else:
            await ctx.send("You are already in your base lol")

    @commands.command(name="inventory", aliases=["inv"])
    @check_if_in_db()#i will fix this dont worry
    async def inventory(self, ctx):
      avatar = ctx.author.avatar
      user_ = user.User(ctx.author)
      user_.sort_inventory(user_.get_user_data("configurations")["inventory_key"])
      value = []
      for i in user_.inv:
        if user_.inv[i] != 0:
          item = pickle.loads(i.encode())
          value.append(f"{item.emoji_id} **{item.display_name}** ─ {user_.inv[i]}")
      embed = discord.Embed(description="\n".join(value))
      embed.set_author(name=f"{ctx.author.name}'s inventory", icon_url=avatar)
      embed.set_footer(text="You can't use 'pls use [item]' to use an item lol")
      await ctx.send(embed=embed)

    @commands.command(name="createaccount", aliases=["start", "create"])
    async def createaccount(self, ctx):
        user_ = user.User(ctx.author)
        if user_.check_if_in_db():
            await ctx.send("You already have an account bro.")
        else:
            await user_.create_account()
            initialize_cooldowns(cooldowns)
            await ctx.send("Created a miner for you!", mention_author=False)

    @commands.command(name="deleteaccount")
    @check_if_in_db()
    async def deleteaccount(self, ctx):
        user_ = user.User(ctx.author)
        cfmbtn = Button(label="CONFIRM", style=discord.ButtonStyle.danger)
        cfmview = view_timeout(timeout=10, ctx=ctx)
        cfmview.add_item(cfmbtn)
        await ctx.send(
            "Are you ABSOLUTELY SURE you want to delete your account PERMANANTLY"
        )
        msg = await ctx.send("This action CANNOT be undone", view=cfmview)
        cfmview.message = msg

        async def cfmcb(interaction):
            user_.delete_user()
            cfmbtn.disabled = True
            await ctx.send("You deleted your account );")
            await interaction.response.edit_message(view=cfmview)

        cfmbtn.callback = cfmcb
      
    @commands.command(name="settings", aliases = ["config"])
    @check_if_in_db() 
    async def setting(self, ctx, *args):
      user_ = user.User(ctx.author)
      if not args:
        config = user_.get_user_data("config")
        embed = discord.Embed(title=f"{ctx.author.name}'s configurations")
        for i in config:
          embed.add_field(name=i, value=config[i], inline=False)
        await ctx.send(embed=embed)
        
      elif args[0] == "direction" or args[0] == "mining_direction":
        if args[1] == "up":
          user_.update_user_data("config", "Mining Direction", "up")
          ctx.send("Congratulations! You are now mining upwards!") 
        if args[1] == "down":
          user_.update_user_data("config", "Mining Direction", "down") 
          await ctx.send("Congratulations! You are now mining downwards!")
          
    @commands.command(name="shop")
    @check_if_in_db()
    async def shop(self, ctx, *args):
      pass
      
def setup(bot: commands.bot):
    bot.add_cog(Miner(bot))

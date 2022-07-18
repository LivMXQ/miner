import discord
import user
from fuzzywuzzy import process
from cogs.error import UserNotInDb
from discord.ext import commands

admin_users = ["895289342497538059", "808223912688746496", "836571495886880829"]#liv, dwizard, jadentrain69
cooldowns = dict()

class Miner(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      user.initialize_cooldowns(cooldowns)

    def check_cooldown():
      async def predicate(ctx):
        user_id = str(ctx.author.id)
        if user_id in admin_users:
          return True
        if user_id in cooldowns:
          bucket = cooldowns[user_id].get_bucket(ctx.message)
          retry_after = bucket.update_rate_limit()
          if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.user)
          else:
            raise UserNotInDb(ctx.author)
        return True
      return commands.check(predicate)

    def check_if_in_db():
        async def predicate(ctx):
          _user = user.User(ctx)
          if not _user.check_if_in_db():
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
      _user = user.User(ctx)
      await _user.mine_()
      
    
    @commands.command(name="returntobase", aliases=["rtb"])
    async def returntobase(self, ctx):
        _user = user.User(ctx)
        if _user.return_to_base():
            await ctx.send("You Successfully returned to base!")
        else:
            await ctx.send("You are already in your base lol")

  
    @commands.command(name="inventory", aliases=["inv"])
    @check_if_in_db()
    async def inventory(self, ctx):
      _user = user.User(ctx.author)
      await _user.send_inventory_message()

    @commands.command(name="collections", aliases=["col", "collection"])
    @check_if_in_db()
    async def collections(self, ctx, *item):
      _user = user.User(ctx)
      if item:
        pass
      else:
        pass
        await _user.send_collection_message()
      

    @commands.command(name="createaccount", aliases=["start", "create"])
    async def createaccount(self, ctx):
        _user = user.User(ctx)
        if _user.check_if_in_db():
            await ctx.send("You already have an account bro.")
        else:
            await _user.create_account()
            user.initialize_cooldowns(cooldowns)
            await ctx.send("Created a miner for you!", mention_author=False)

  
    @commands.command(name="deleteaccount")
    @check_if_in_db()
    async def deleteaccount(self, ctx):
        _user = user.User(ctx)
        cfmbtn = discord.ui.Button(label="CONFIRM", style=discord.ButtonStyle.danger)
        cfmview = user.ViewTimeout(timeout=10, ctx=ctx)
        cfmview.add_item(cfmbtn)
        await ctx.send(
            "Are you ABSOLUTELY SURE you want to delete your account PERMANANTLY"
        )
        cfmview.message = await ctx.send("This action CANNOT be undone", view=cfmview)
        
      
        async def cfmcb(interaction):
            _user.delete_user()
            cfmbtn.disabled = True
            await ctx.send("You deleted your minor );")
            await interaction.response.edit_message(view=cfmview)
        cfmbtn.callback = cfmcb

      
    @commands.command(name="settings", aliases = ["config","setting"])
    @check_if_in_db() 
    async def setting(self, ctx, *setting):
      _user = user.User(ctx)
      if not setting:
        config = _user.get_user_data("configurations")
        embed = discord.Embed(title=f"{ctx.author.name}'s configurations")
        for i in config:
          embed.add_field(name=i, value=config[i], inline=False)
        await ctx.send(embed=embed)
        
      elif setting[0] == "direction" or setting[0] == "mining_direction":
        if setting[1] == "up":
          _user.update_user_data("up", "config", "mining_direction")
          await ctx.send("Congratulations! You are now mining upwards!") 
        if setting[1] == "down":
          _user.update_user_data("down", "config", "mining_direction") 
          await ctx.send("Congratulations! You are now mining downwards!")

    @commands.command(name="item")
    async def item(self, ctx, item_name=None):
      if not item_name: 
        pass
      else:
        item_names = [i.display_name for i in user.get_all_items()]
        item = process.extractOne(item_name, item_names)
        pass
        
    @commands.command(name="shop")
    @check_if_in_db()
    async def shop(self, ctx, item):
      pass
      
def setup(bot: commands.bot):
    bot.add_cog(Miner(bot))

# pylint: disable=unused-variable
# pylint: enable=too-many-lines

import discord
from discord.ext import commands
import random
import json
import asyncio
import userdata as ud



class fishing(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @ud.has_pp()
    async def fish(self, ctx):
        async with ctx.typing():
            embed = await ud.create_embed(ctx)
            pp = await ud.Pp.fetch(ctx.author.id, self.bot)
            inv = ud.Inv(ctx.author.id)
            
            if not await inv.has_item('fishing rod'):
                raise ud.ItemRequired(f"How are you planning on fishing without a **fishing rod**? You need that item to use this command. Check if its for sale at the shop!")
            
            random_number = random.randint(1, 40)
            if random_number == 1:
                await inv.new_item("fishing rod", -1)
                embed.description = f"{ctx.author.mention} flung their fishing rod too hard and it broke lmaoo"
                return await ctx.send(embed=embed)
            if random_number == 2:
                embed.description = f"{ctx.author.mention} went fishing and caught nothing."
                return await ctx.send(embed=embed)
            
            fish_amount = random_number // 2 * pp.multiplier["multiplier"]
            pp.size += fish_amount
            await pp.update()
            quote = random.choice(['Pretty cool huh?','Nice!','Epic!'])
            embed.description = f"{ctx.author.mention} went fishing and caught **{fish_amount} inches!** {quote}"
        return await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @ud.has_pp()
    async def hunt(self, ctx):
        embed = await ud.create_embed(ctx)
        pp = await ud.Pp.fetch(ctx.author.id, self.bot)
        inv = ud.Inv(ctx.author.id)
        
        if not await inv.has_item('rifle'):
            raise ud.ItemRequired(f"you need a **rifle** to use this command and become a master of the memes. Check if its for sale at the shop!")
        
        random_number = random.randrange(1, 50)
        
        if random_number == 1:
            await inv.new_item("rifle", -1)
            embed.description = f"{ctx.author.mention} got arrested and their rifle was confiscated."
            return await ctx.send(embed=embed)
        
        if random_number == 2:
            embed.description = f"{ctx.author.mention} shot a homeless man who had just gambled away the last of his inches."
            return await ctx.send(embed=embed)
        
        if random_number <= 45:
            options = {
                'shot a homeless man': random.randint(1,20) * pp.multiplier["multiplier"],
                'deadass just killed a man': random.randint(5,20) * pp.multiplier["multiplier"],
                'shot up a walmart': random.randint(10,30) * pp.multiplier["multiplier"],
                'hijacked a fucking orphanage and sold all the kids': random.randint(30,50) * pp.multiplier["multiplier"],
                }
            choice = random.choice(list(options.items()))
            pp.size += choice[1]
            await pp.update()
            embed.description = f"{ctx.author.mention} {choice[0]} for **{choice[1]} inches!**"
            return await ctx.send(embed=embed)
        
        else:
            options = {
                '[ _ _ _ _ ] an ambulance! But not for me.': 'CALL',
                'You\'ll never [ _ _ _ _ ] me alive! *doot*': 'TAKE',
                '*dodges bullets like in The [ _ _ _ _ _ _ ]*': 'MATRIX',
                'I have the power of [ _ _ _   _ _ _   _ _ _ _ _ ] on my side!': 'GOD AND ANIME',
                }
            choice = random.choice(list(options.items()))
            embed.description = f"{ctx.author.mention} tried to shoot a police officer but they shot back! **Fill in this sentence to dodge the bullets:**\n\n`{choice[0]}`"
            await ctx.send(embed=embed)
            
            try:
                await self.bot.wait_for('message',timeout=20.0,check=lambda m: m.content.upper() == choice[1] and m.author == ctx.author and m.channel == ctx.channel)
                
            except asyncio.TimeoutError:
                random_number = random.randint(1,50) * pp.multiplier["multiplier"]
                
                if pp.size > 50 * pp.multiplier["multiplier"]:
                    pp.size -= random_number
                    await pp.update()
                    embed.description = f"**Too slow!** The police officer shoots you and takes **{random_number} inches** from your corpse. The correct word was `{choice[1]}`"
                    
                else:
                    embed.description = f"**Too slow!** The police officer shoots you and realises your pp is so small it's not even worth taking. The correct word was `{choice[1]}`"
                return await ctx.send(embed=embed)
            
            if random_number < 30:
                options = [
                    'bronze coin',
                    'happy flour',
                    'fishing rod',
                    ]
                choice = random.choice(options)
                await inv.new_item(choice)
                pp.size += random_number
                await pp.update()
                embed.description = f"You avoid the bullet and loot the police officer. You find **{random_number} inches** and **1 {choice}!**"
                
            else:
                pp.size += random_number
                await pp.update()
                embed.description = f"You avoid the bullet and loot the police officer. You find **{random_number} inches!**"
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(fishing(bot))

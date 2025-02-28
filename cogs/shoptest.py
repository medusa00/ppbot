import discord
from discord.ext import commands
from datetime import datetime
import random
import userdata as ud



class shoptest(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(aliases=['storetest'])
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def shoptest(self, ctx, page:int=1):
        async with ctx.typing():
            embed,pp,exception = await ud.create_embed(ctx)
            if exception:
                return await ud.handle_exception(ctx,exception)
            shop = ud.Shop()
            shopitems = await shop.dict_items()
            totalpages = len(shopitems) // 5 + (len(shopitems) % 5 > 0)
            #yes pp
            #page bad
            if page < 1 or page > totalpages:
                embed.description = f"{ctx.author.mention}, that page is doesn't exist."
                return await ctx.send(embed=embed)
            #page good
            embed.title = "shop"
            embed.description = f'In the shop you can buy items with inches. You currently have **{await pp.pp_size()}** inches.\n Type `pp buy <amount> <item>` to buy an item. Prices of items may change depending on how many you\'ve bought'
            for i in shopitems[page * 5 - 5:page * 5]:
                item = shop.Item(i["item_name"])
                embed.add_field(
                    name = f'**{item.item_name}** ─ __{await item.price(pp)} inches__ `{i["item_type"]}: sell for {i["sell_for"]} inches`',
                    value = f'{i["item_desc"]}{" | The price of this item depends on your current multiplier" if i["multiplierdependent"] else ""}',
                    inline=False
                    )
            embed.set_footer(text=f'page {page}/{totalpages}')
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(shoptest(bot))

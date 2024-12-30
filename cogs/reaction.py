import disnake
from disnake.ext import commands
import random
from disnake.ext.commands import UserInputError
bot = commands.Bot(command_prefix=commands.when_mentioned)





class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="Выбрать реакцию")

    async def reaction(inter, member: disnake.Member = (commands.Param(description='Выбери юзера из списка')), reaction: str = commands.Param(description='Выберите реакцию из списка',choices=["Поцеловать", "Секс", "Укусить", "Ударить", "Обнять", "Тыкнуть", "Погладить", "Облизать", "Проявить любовь"])):
        if member == inter.author:
            await inter.response.send_message("Вы не можете выбирать себя!", ephemeral=True)
            return
        elif member.bot:
            await inter.response.send_message("Вы не можете выбирать ботов!",ephemeral=True)
            return   


        Поцелуй = {
            "Поцеловать": [
                "https://media.tenor.com/jnndDmOm5wMAAAAC/kiss.gif",
                "https://media.tenor.com/F02Ep3b2jJgAAAAC/cute-kawai.gif",
                "https://media.tenor.com/dn_KuOESmUYAAAAC/engage-kiss-anime-kiss.gif",
                "https://media.tenor.com/lYKyQXGYvBkAAAAC/oreshura-kiss.gif",
                "https://media.tenor.com/fiafXWajQFoAAAAC/kiss-anime.gif",
                "https://media.tenor.com/8mUI_rkXUuAAAAAC/kiss.gif"
            ]
        }

        Укус = {
            "Укусить": [
                "https://media.tenor.com/5mVQ3ffWUTgAAAAC/anime-bite.gif",
                "https://media.tenor.com/3lz4gjb3q-QAAAAM/moka-bite.gif",
                "https://media.tenor.com/6HhJw-4zmQUAAAAC/anime-bite.gif",
                "https://media.tenor.com/adecnFrCqRsAAAAC/neck-no-blood.gif",
                "https://media.tenor.com/n__KGrZPlQEAAAAC/bite.gif",
                "https://media.tenor.com/4j3hMz-dUz0AAAAC/anime-love.gif",
                "https://media.tenor.com/BVFbvCZKNEsAAAAC/princess-connect-anime-bite.gif",
                "https://media.tenor.com/c3mqGRCrAzsAAAAC/bite.gif"
            ]
        }

        Любовь = {
            "Проявить любовь": [
                "https://media.tenor.com/28r8PzKN0HMAAAAd/anime-thanks.gif",
                "https://media.tenor.com/ffwNjCo-P4wAAAAC/dragon-maid-tohru.gif",
                "https://media.tenor.com/8r7jLECx5LIAAAAC/anime.gif",
                "https://media.tenor.com/WEV6KvZIoAIAAAAC/anime-hybrid-heart.gif",
                "https://media.tenor.com/ra5zLAMqL-kAAAAC/foxplushy-foxy.gif",
                "https://media.tenor.com/nOARJZENR9UAAAAC/anime-in-love.gif"
            ]
        }

        Ударить = {
            "Ударить":[
                "https://media.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
                "https://media.tenor.com/ra17G61QRQQAAAAC/tapa-slap.gif",
                "https://media.tenor.com/zXqvIewp3ToAAAAC/asobi-asobase.gif",
                "https://media.tenor.com/kggzZQ1ldoUAAAAC/slapped-anime-slap.gif",
                "https://media.tenor.com/8VAgT4nmZ-UAAAAC/slap-anime.gif",
                "https://media.tenor.com/yJmrNruFNtEAAAAC/slap.gif",
                "https://media.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif",
                "https://media.tenor.com/Irk80uToJA0AAAAC/slap-anime.gif"
            ]
        }
    
        Обнять = {
        "Обнять":[
            "https://media.tenor.com/G_IvONY8EFgAAAAM/aharen-san-anime-hug.gif",
            "https://media.tenor.com/J7eGDvGeP9IAAAAC/enage-kiss-anime-hug.gif",
            "https://media.tenor.com/9e1aE_xBLCsAAAAC/anime-hug.gif",
            "https://media.tenor.com/8o4fWGwBY1EAAAAd/aharensan-aharen.gif",
            "https://media.tenor.com/y9_xxO9iMwkAAAAC/hug.gif",
            "https://media.tenor.com/RWD2XL_CxdcAAAAd/hug.gif",
            "https://media.tenor.com/Maq1tnCFd2UAAAAC/hug-anime.gif",
            "https://media.tenor.com/jSr41Jz0CQYAAAAC/anime-hug-anime-girls.gif",
            "https://media.tenor.com/KoS-POKwhQYAAAAC/yuri-hug.gif"
        ]
    }

        Тыкнуть ={
        "Тыкнуть":[
            "https://media.tenor.com/y4R6rexNEJIAAAAC/boop-anime.gif",
            "https://media.tenor.com/1YMrMsCtxLQAAAAC/anime-poke.gif",
            "https://media.tenor.com/vu1AUXE8wtsAAAAd/anime-sleep.gif",
            "https://media.tenor.com/iu_Lnd86GxAAAAAC/nekone-utawarerumono.gif",
            "https://media.tenor.com/B-E9cSUwhw8AAAAC/highschool-dxd-anime.gif",
            "https://media.tenor.com/7iV_gBGrRAUAAAAC/boop-poke.gif",
            "https://media.tenor.com/dCzpPLhJfQ4AAAAC/anime-poke.gif",
            "https://media.tenor.com/NjIdfk7i3bsAAAAC/poke-poke-poke.gif",
            "https://media.tenor.com/AKMRjD0UDVoAAAAC/poke.gif",
            "https://media.tenor.com/6rS1x-dVUwEAAAAC/ishtar-ishtar-fgo.gif"
        ]
    }

        Погладить = {
            "Погладить":[
            "https://media.tenor.com/7pzJnti052wAAAAC/pat.gif",
            "https://media.tenor.com/7xrOS-GaGAIAAAAC/anime-pat-anime.gif",
            "https://media.tenor.com/98bIO09hMWEAAAAC/project-sekai-pjsk.gif",
            "https://media.tenor.com/pvF8xcytu1YAAAAC/pat.gif",
            "https://media.tenor.com/oGbO8vW_eqgAAAAC/spy-x-family-anya.gif",
            "https://media.tenor.com/jpx4HDUyBLoAAAAC/anime-pat.gif",
            "https://media.tenor.com/OvrmH29V-44AAAAC/pat.gif",
            "https://media.tenor.com/fvUdTeAF95oAAAAC/pat.gif",
            "https://media.tenor.com/9lEuseoEheUAAAAC/pat.gif",
            "https://media.tenor.com/ZeYnQ6uBq8MAAAAC/anime-pat.gif"
        ]
    }

        Лизнуть = {
            "Облизать":[
            "https://media.tenor.com/sNVeYN1jIcIAAAAC/licks-anime-anime.gif",
            "https://media.tenor.com/30jarFTFk5kAAAAC/anime-girl.gif",
            "https://media.tenor.com/jyv9sexi1fYAAAAC/anime-lick.gif",
            "https://media.tenor.com/al640NjsUccAAAAC/lick-intimate.gif",
            "https://media.tenor.com/WEV6KvZIoAIAAAAC/anime-hybrid-heart.gif",
            "https://media.tenor.com/t6cxb_yox3QAAAAC/lick-ear.gif",
            "https://media.tenor.com/sNVeYN1jIcIAAAAC/licks-anime-anime.gif"
            ]
        }

        Секс = {
            "Секс":[
                "https://media.tenor.com/dRlCBGZ0NwEAAAAC/anime-panties.gif",
                "https://media.tenor.com/eSBQVi2o4dQAAAAC/surprised-anime.gif"
            ]
        }

        if reaction in Укус:
            embed = disnake.Embed(title="Реакция: Укусить", description=f"{inter.author.mention} укусил(-а) {member.mention}")
            embed.set_image(url=random.choice(Укус[reaction]))
            await inter.response.send_message(content=member.mention, embed=embed)
        elif reaction == "Поцеловать":
            embed = disnake.Embed(title="Реакция: Поцелуй", description=f"{inter.author.mention} поцеловал(-а) {member.mention}")
            embed.set_image(url=random.choice(Поцелуй[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)        
        elif reaction in Поцелуй:    
            embed = disnake.Embed(title="Реакция: Поцелуй", description=f"{inter.author.mention} поцеловал(-а) {member.mention}")
            embed.set_image(url=random.choice(Поцелуй[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Любовь:
            embed = disnake.Embed(title="Реакция: Любовь", description=f"{inter.author.mention} выразил(-а) любовь к {member.mention}")
            embed.set_image(url=random.choice(Любовь[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed) 
        elif reaction in Ударить:
            embed = disnake.Embed(title="Реакция: Удар", description=f"{inter.author.mention} ударил(-а) {member.mention}")
            embed.set_image(url=random.choice(Ударить[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Обнять:
            embed = disnake.Embed(title="Реакция: Обнять", description=f"{inter.author.mention} обнял(-а) {member.mention}")
            embed.set_image(url=random.choice(Обнять[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Тыкнуть:
            embed = disnake.Embed(title="Реакция: Тыкнуть", description=f"{inter.author.mention} тыкнул(-а) {member.mention}")
            embed.set_image(url=random.choice(Тыкнуть[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Погладить:
            embed = disnake.Embed(title="Реакция: Погладить", description=f"{inter.author.mention} погладил(-а) {member.mention}")
            embed.set_image(url=random.choice(Погладить[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Лизнуть:
            embed = disnake.Embed(title="Реакция: Лизнуть", description=f"{inter.author.mention} лизнул(-а) {member.mention}")
            embed.set_image(url=random.choice(Лизнуть[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)
        elif reaction in Секс:
            embed = disnake.Embed(title="Реакция: Секс", description=f"{inter.author.mention} занялся(-ась) сексом с {member.mention}")
            embed.set_image(url=random.choice(Секс[reaction]))
            await inter.response.send_message(content=member.mention,embed=embed)                             
        else:
            await inter.response.send_message(f"Invalid operation: {reaction}", ephemeral=True)  

def setup(bot):
    bot.add_cog(Reactions(bot))

    
     


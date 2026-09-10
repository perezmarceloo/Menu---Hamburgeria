import discord
from discord.ext import commands
import pygame


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


cardapio = {
    "Refri": [":cup_with_straw: Refri de Cola", ":cup_with_straw: Refri de Laranja", ":cup_with_straw: Refri de Uva", ":cup_with_straw: Refri de Guaraná", ":cup_with_straw: Refri de Limão", ":cup_with_straw: Refri de Maça"],
    "Hamburgers": [":hamburger: Hamburguer de Frango", ":hamburger: Hamburguer de Carne", ":hamburger: Hamburguer de Vegetariano", ":hamburger: Hamburguer de Peixe", ":hamburger: Hamburguer de Bacon"],
    "Acompanhamento": [":fries: Batata Frita", ":onion: Anéis de Cebola", ":cheese: Palitos de Queijo", ":salad: Salada", ":chicken: Frango empanado"]
}


pedidos_em_andamento = {}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

@bot.command(name="cardapio")
async def mostrar_cardapio(ctx):
    """Exibe o cardápio completo no chat"""
    resposta = "**=== PARANÁ LANCHES - CARDÁPIO ===**\n\n"
    for categoria, itens in cardapio.items():
        resposta += f"**{categoria}:**\n"
        for item in itens:
            resposta += f"• {item}\n"
        resposta += "\n"
    
    resposta += "Para fazer um pedido, digite `!pedir`"
    await ctx.send(resposta)

@bot.command(name="pedir")
async def iniciar_pedido(ctx):
    """Inicia o fluxo de pedido passo a passo"""
    user_id = ctx.author.id
    
    
    pedidos_em_andamento[user_id] = {"etapa": "refri", "itens": {}}
    
    opcoes_refri = ", ".join(cardapio["Refri"])
    await ctx.send(
        f"Olá {ctx.author.mention}! Vamos montar seu pedido.\n"
        f"**1. Qual refrigerante você deseja?**\n*Opções:* {opcoes_refri}"
    )

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    user_id = message.author.id

    
    if user_id in pedidos_em_andamento and not message.content.startswith("!"):
        estado = pedidos_em_andamento[user_id]
        etapa = estado["etapa"]
        texto_usuario = message.content.strip()

        if etapa == "refri":
            estado["itens"]["Refri"] = texto_usuario
            estado["etapa"] = "hamburguer"
            opcoes_burgers = ", ".join(cardapio["Hamburgers"])
            await message.channel.send(
                f"Anotado! **2. Qual hambúrguer você deseja?**\n*Opções:* {opcoes_burgers}"
            )

        elif etapa == "hamburguer":
            estado["itens"]["Hamburguer"] = texto_usuario
            estado["etapa"] = "acompanhamento"
            opcoes_acomp = ", ".join(cardapio["Acompanhamento"])
            await message.channel.send(
                f"Anotado! **3. Qual acompanhamento você deseja?**\n*Opções:* {opcoes_acomp}"
            )

        elif etapa == "acompanhamento":
            estado["itens"]["Acompanhamento"] = texto_usuario
            
            # Resumo final do pedido
            resumo = (
                f"**=== PEDIDO CONCLUÍDO ({message.author.mention}) ===**\n"
                f"🥤 **Refrigerante:** {estado['itens']['Refri']}\n"
                f"🍔 **Hambúrguer:** {estado['itens']['Hamburguer']}\n"
                f"🍟 **Acompanhamento:** {estado['itens']['Acompanhamento']}\n\n"
                f"Obrigado por comprar no Paraná Lanches!"
            )
            await message.channel.send(resumo)
            
            
            del pedidos_em_andamento[user_id]

    
    await bot.process_commands(message)


bot.run("INSERIR TOKEN DO BOT")

from discord.ext import commands
from discord import utils
from discord import Intents
from discord import Embed
from discord import File
from scipy.misc import derivative
from numpy import sin, cos, tan, sqrt, exp, log
import matplotlib.pyplot as plt
import random 
import os
from dotenv import load_dotenv


plt.ioff()
intents = Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)
channel_repartition = 998625250554159305
log_bot = 998942314619736085

@bot.event
async def on_ready():
	print("Ready")

@bot.event
async def on_message(message):
	if message.content == "Salut StanBot":
		await message.channel.send(f"Salut {message.author.mention}")
	await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):

	channel_log = bot.get_channel(log_bot)
	channel_id = payload.channel_id
	emoji = payload.emoji
	guild = bot.get_guild(payload.guild_id)
	member = guild.get_member(payload.user_id)
	MPSI = utils.get(guild.roles, name="MPSI")
	PCSI = utils.get(guild.roles, name="PCSI")
	BL = utils.get(guild.roles, name="BL")
	roles = [MPSI, PCSI, BL]

	if payload.user_id != bot.user.id:

		#Gestion des roles PCSI et MPSI
		if channel_id == channel_repartition:

			channel = bot.get_channel(channel_id)
			msg = utils.get(await channel.history(limit=100).flatten(), author=bot.user)
			

			if str(emoji) == '🔵':	

				await msg.reactions[0].remove(member)

				for rl in roles:
					try:
						await member.remove_roles(rl)
					except Exception:
						pass

				await member.add_roles(MPSI)
				await member.send("Vous avez mainteant le rôle MPSI !")
				await channel_log.send(f"{member} a maintenant le rôle MPSI")

			elif str(emoji) == '🔴':

				await msg.reactions[1].remove(member)	

				for rl in roles:
					try:
						await member.remove_roles(rl)
					except Exception:
						pass
				
				await member.add_roles(PCSI)
				await member.send("Vous avez mainteant le rôle PCSI !")
				await channel_log.send(f"{member} a maintenant le rôle PCSI")

			elif str(emoji) == '🟢':


				await msg.reactions[2].remove(member)	
				
				for rl in roles:
					try:
						await member.remove_roles(rl)
					except Exception:
						pass
				
				await member.add_roles(BL)
				await member.send("Vous avez mainteant le rôle BL !")
				await channel_log.send(f"{member} a maintenant le rôle BL")




@bot.event
async def on_raw_reaction_remove(payload):

	channel_id = payload.channel_id
	emoji = payload.emoji
	guild = bot.get_guild(payload.guild_id)
	member = guild.get_member(payload.user_id)




@bot.command(pass_context = True)
async def rep(ctx):

	if ctx.message.author.guild_permissions.manage_messages == True:
		channel_log = bot.get_channel(log_bot)
		channel = bot.get_channel(channel_repartition)
		msg = utils.get(await channel.history(limit=100).flatten(), author=bot.user)

		if msg == None:

			embed = Embed(title="Choisissez votre filière en réagissant ci-dessous:", color=0xeee657)
			embed.add_field(name = "🔵", value = "Rôle => MPSI", inline = False)
			embed.add_field(name = "🔴", value = "Rôle => PCSI", inline = False)
			embed.add_field(name = "🟢", value = "Rôle => BL", inline = False)

			msg = await channel.send(embed = embed)

			await msg.add_reaction('🔵')
			await msg.add_reaction('🔴')
			await msg.add_reaction('🟢')

			await ctx.channel.send(f"Fait ! {ctx.message.author.mention} ", delete_after = 2)

	else:

		await ctx.channel.send(f"❌ Vous n'avez pas la permission requise {ctx.message.author.mention} ❌", delete_after = 3)
		await channel_log.send(f"{ctx.message.author} n'avait pas la permission pour exécuter la commande répartition : commande rejetée")






@bot.command(pass_context = True)
async def clear(ctx, limit=None):

	channel_log = bot.get_channel(log_bot)
	await channel_log.send(f"{ctx.message.author} a lancé une commande clear")

	if limit != None:
		if ctx.message.author.guild_permissions.manage_messages == True:
			hist = await ctx.channel.history(limit=int(limit)+1).flatten()
			for msg in hist:
				await msg.delete()

			await channel_log.send(f"{limit} élément(s) supprimé(s)")
		else:
			await ctx.channel.send(f"❌ Vous n'avez pas la permission requise {ctx.message.author.mention} ❌", delete_after = 3)
			await channel_log.send(f"{ctx.message.author} n'avait pas la permission : commande rejetée")
			await ctx.message.delete()
	else:
		await ctx.channel.send(f"❌ Il faut préciser une limite {ctx.message.author.mention} ❌", delete_after = 3)
		await channel_log.send(f"{ctx.message.author} a fait une erreur dans la saisie de la commande")
		await ctx.message.delete()






@bot.command(pass_context =True)
async def rand(ctx, min : int, max : int):
	if min < max:
		r = random.randint(min, max)
		await ctx.channel.send(f"{ctx.message.author.mention} Nombre aléatoire entre {min} et {max} >>> {r}")
	else:
		await ctx.channel.send(f"❌ Il faut que le minimum soit en premier {ctx.message.author.mention} ❌", delete_after = 3)
		await ctx.message.delete()





@bot.command(pass_context = True)
async def courbe(ctx, fct, mini : float, maxi : float, pas : float):

	if "ln" in fct:
		e = fct.split("ln")
		fct = "log".join(e)

	if pas >= 1:
		arrondi = 1
	else:
		arrondi = len(str(pas))-2

	x = []

	y = []
	abc = []
	ordo = []

	def fonc(x):
		return eval(fct)

	val = mini

	while val < maxi+pas:
		x.append(round(val,arrondi))
		val += pas


	for val in x:
		try:
			y.append(fonc(val))
		except Exception as err:
			y.append("VI")


	for i in range(0, len(x)):

		if y[i] == "VI":
			if ordo != []:
				plt.plot(abc, ordo, color = "yellow")
			abc = []
			ordo = []

		else:
			abc.append(x[i])
			ordo.append(y[i])

	plt.plot(abc, ordo, color = "blue")

	plt.title(f"Graphique de {fct}")

	name = f"g_{ctx.message.author}.png"
	plt.savefig(name)


	file = File(name, filename = name)
	await ctx.channel.send(file=file)
	os.remove(name)
	plt.cla()
	plt.clf()
	plt.close()


@bot.command(pass_context =True)
async def cbderiv(ctx, fct, mini : float, maxi : float, pas : float):

	if "ln" in fct:
		e = fct.split("ln")
		fct = "log".join(e)

	if pas >= 1:
		arrondi = 1
	else:
		arrondi = len(str(pas))-2

	x = []

	y_prime = []
	abcisse_deriv = []
	ordonnée_deriv = []	

	def fonc(x):
		return eval(fct)

	val = mini

	while val < maxi+pas:
		x.append(round(val,arrondi))
		val += pas

	for val in x:
		try:
			y_prime.append(derivative(fonc, val))

		except Exception as err:
			y_prime.append("VI")

	for i in range(0, len(x)):

		if y_prime[i] == "VI":
			if ordonnée_deriv != []:
				plt.plot(abcisse_deriv, ordonnée_deriv, color = "purple")
			abcisse_deriv = []
			ordonnée_deriv = []

		else:
			abcisse_deriv.append(x[i])
			ordonnée_deriv.append(y_prime[i])

	plt.plot(abcisse_deriv, ordonnée_deriv, color = "purple")

	plt.title(f"Graphique de ( {fct} )'")

	name = f"g'_{ctx.message.author}.png"
	plt.savefig(name)


	file = File(name, filename = name)
	await ctx.channel.send(file=file)
	os.remove(name)
	plt.cla()
	plt.clf()
	plt.close()




@bot.command(pass_context = True)
async def deriv(ctx, fct:str, val : int):

	def fonc(x):
		return eval(fct)

	deriv = derivative(fonc, val)

	await ctx.channel.send(f"{ctx.message.author.mention} La dérivée de la fonction f(x) = {fct} pour x = {val} est f'({val}) = {deriv}")



@bot.command(pass_context = True)
async def helpme(ctx):

	embed = Embed(title = "📒 __*DOCUMENTATION SUR **STANBOT***__ 📒", description = "Voici une petite documentation avec quelques informations sur des commandes utiles de **StanBot**\n")
	embed.add_field(name = "PREFIXE", value = "Le préfixe utilisé est le point d'exclamation **!**, à mettre accolé avant chaque commande\n", inline = False)
	embed.add_field(name = "clear *nb  messages*", value = "Cette commande permet de supprimer les nb derniers messages du fil sur lequel la commande est exécutée. Attention, cette commande nécessite la permission de gestion de messages\n", inline = False)
	embed.add_field(name = "courbe *fonction  minimum  maximum  pas*", value = "Cette commande permet d'obtenir la courbe de la fonction renseignée entre les bornes minimum et maximum\n", inline = False)
	embed.add_field(name = "deriv *fonction  valeur*", value = "Cette commande permet d'obtenir **f'**(valeur)\n", inline = False)
	embed.add_field(name = "cbderiv *fonction  minimum  maximum  pas*", value = "Cette commande se base sur le même principe que celui de la commande courbe, à la différence qu'elle renvoie la courbe de la fonction dérivée\n", inline = False)
	embed.add_field(name = "rand *minimum  maximum*", value = "Cette commande renvoie un nombre aléatoire entre les bornes minimum et maximum")
	embed.set_footer(text = f"En espérant que cela ait pu t'aider {ctx.message.author}")

	await ctx.channel.send(embed = embed)

bot.run(TOKEN)

import random, discord, requests, os
 
from PIL import Image

from animeApi import randomCharacter

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content.startswith('-hello'):
    await message.channel.send(message.author.mention + ' Hello!')

  if message.content.startswith('-pull'):

    i = 0
    charactersImg = {}
    msg = discord.Embed (
        title="Here is your pull master.", 
        description= message.author.mention, 
        color=0xc9c9c9
      )

    while i < 3:
      character = randomCharacter(random.randint(0,9999))
      msg.add_field (
      name= str(character['firstName'])+' '+str(character['lastName']), 
      value= character['media'], 
      inline= True
      )
      charactersImg["img-{0}".format(i)] = character['image']
      i += 1

    image1 = Image.open(requests.get(charactersImg['img-0'], stream=True).raw)
    image2 = Image.open(requests.get(charactersImg['img-1'], stream=True).raw)
    image3 = Image.open(requests.get(charactersImg['img-2'], stream=True).raw)

    image1 = image1.resize((200, 250))
    image2 = image2.resize((200, 250))
    image3 = image3.resize((200, 250))

    image1_size = image1.size
    image2_size = image2.size

    new_image = Image.new('RGB',(3*image1_size[0], image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0],0))    
    new_image.paste(image3,(image2_size[0],0))    
    new_image.save("images/merged_image.jpg","JPEG")
    
    msg.set_image(new_image)

    await message.channel.send(embed=msg)


client.run(os.getenv('TOKEN'))

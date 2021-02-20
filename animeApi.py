import requests 

url = 'https://graphql.anilist.co'

def randomCharacter(id):
  
  query = '''
  query ($id: Int) {
    Character (id: $id) {
      name {
        first 
        last
      }
      media {
        nodes {
          title {
            romaji
          }
        }
      }
      favourites
      image {
        large
      }
    }
  }
  '''
  res = requests.post(url, json={'query': query, 'variables': {'id': id}})

  try:
    res.raise_for_status()
    character = {
      'firstName': res.json()['data']['Character']['name']['first'],
      'lastName': res.json()['data']['Character']['name']['last'],
      'favourites': res.json()['data']['Character']['favourites'],
      'media': res.json()['data']['Character']['media']['nodes'][0]['title']['romaji'],
      'image': res.json()['data']['Character']['image']['large']
    }
    return character

  except requests.exceptions.HTTPError as e:
    return "Error: " + str(e)

  
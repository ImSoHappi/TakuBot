import requests

url = 'https://graphql.anilist.co'

def getStatistics():
    query = '''
      query {
        Character (sort: [ID_DESC]) {
          id
          name {
            full
          }
        }
        Anime: Media (type: ANIME, sort: [ID_DESC]) {
          id
          title {
            romaji
          }
        }
        Manga: Media (type: MANGA, sort: [ID_DESC]) {
          id
          title {
            romaji
          }
        }
        SiteStatistics {
          characters {
            nodes{
              count
            }
          }
          anime {
            nodes {
              count
            }
          }
          manga {
            nodes {
              count
            }
          }
        }
      }
      '''
    
    try:
      res = requests.post(url, json={'query': query})
      res.raise_for_status()
      return res

    except requests.exceptions.RequestException as e:
        return False

def getCharacter(id):
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
  
    try:
        res = requests.post(url, json={'query': query, 'variables': {'id': id}})
        res.raise_for_status()
        character = {
            'firstName': res.json()['data']['Character']['name']['first'],
            'lastName': res.json()['data']['Character']['name']['last'],
            'favourites': res.json()['data']['Character']['favourites'],
            'media': res.json()['data']['Character']['media']['nodes'][0]['title']['romaji'],
            'image': res.json()['data']['Character']['image']['large']
        }
        return character

    except requests.exceptions.RequestException as e:
        return False

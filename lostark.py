import requests
import pandas as pd
from google.colab import userdata
API_KEY = userdata.get("lostark_api")
ITEM_ID = '65203905'
url = f'https://developer-lostark.game.onstove.com/markets/items/{ITEM_ID}'

headers = {
    'Authorization': f'bearer {API_KEY}' ,
    'accept': 'application/json'
}
response = requests.get(url, headers=headers)
data = response.json()
df_1 = pd.DataFrame(data)



import requests
import os
import json
import math

CollectionName = "name".lower()



collection = requests.get(f"http://api.opensea.io/api/v1/collection/{CollectionName}?format=json")

if collection.status_code == 429:
    print("Server returned HTTP 429. Request was throttled. Please try again in about 5 minutes.")

if collection.status_code == 404:
    print("NFT Collection not found.\n\n(Hint: Try changing the name of the collection in the Python script, line 11.)")
    exit()

collectioninfo = json.loads(collection.content.decode())



if not os.path.exists('./images'):
    os.mkdir('./images')

if not os.path.exists(f'./images/{CollectionName}'):
    os.mkdir(f'./images/{CollectionName}')

if not os.path.exists(f'./images/{CollectionName}/image_data'):
    os.mkdir(f'./images/{CollectionName}/image_data')



count = int(collectioninfo["collection"]["stats"]["count"])



iter = math.ceil(count / 50)

print(f"\nBeginning download of \"{CollectionName}\" collection.\n")



stats = {
"DownloadedData": 0,
"AlreadyDownloadedData": 0,
"DownloadedImages": 0,
"AlreadyDownloadedImages": 0,
"FailedImages": 0
}


for i in range(iter):
    offset = i * 50
    data = json.loads(requests.get(f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}&limit=50&collection={CollectionName}&format=json").content.decode())

    if "assets" in data:
        for asset in data["assets"]:
          formatted_number = f"{int(asset['token_id']):04d}"

          print(f"\n#{formatted_number}:")

          
          if os.path.exists(f'./images/{CollectionName}/image_data/{formatted_number}.json'):
              print(f"  Data  -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedData"] += 1
          else:
                
                dfile = open(f"./images/{CollectionName}/image_data/{formatted_number}.json", "w+")
                json.dump(asset, dfile, indent=3)
                dfile.close()
                print(f"  Data  -> [\u2713] (Successfully downloaded)")
                stats["DownloadedData"] += 1

          
          if os.path.exists(f'./images/{CollectionName}/{formatted_number}.png'):
              print(f"  Image -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedImages"] += 1
          else:
            
            if not asset["image_original_url"] == None:
              image = requests.get(asset["image_original_url"])
            else:
              image = requests.get(asset["image_url"])

          
            if image.status_code == 200:
                file = open(f"./images/{CollectionName}/{formatted_number}.png", "wb+")
                file.write(image.content)
                file.close()
                print(f"  Image -> [\u2713] (Successfully downloaded)")
                stats["DownloadedImages"] += 1
            
            else:
                print(f"  Image -> [!] (HTTP Status {image.status_code})")
                stats["FailedImages"] += 1
                continue

print(f"""

Finished downloading collection.


Statistics
-=-=-=-=-=-

Total of {count} units in collection "{CollectionName}".

Downloads:

  JSON Files ->
    {stats["DownloadedData"]} successfully downloaded
    {stats["AlreadyDownloadedData"]} already downloaded

  Images ->
    {stats["DownloadedImages"]} successfully downloaded
    {stats["AlreadyDownloadedImages"]} already downloaded
    {stats["FailedImages"]} failed


You can find the images in the images/{CollectionName} folder.
The JSON for each NFT can be found in the images/{CollectionName}/image_data folder.
Press enter to exit...""")
input()

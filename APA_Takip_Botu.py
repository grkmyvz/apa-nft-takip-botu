# Kütüphaneler
import time
import json
import requests

# APA nftlerinin datasının bulunduğu json dosyası
with open('db/apa_database.json') as f:
    apaData = json.load(f)

# Moralis uygulamasından alınan api key. https://moralis.io/
headers = {
        'x-api-key' : '' # Bu kısma moralis apisini yapıştırın.
    }

# Bot ile ilgili gerekli ayarların bulunduğu kısım.
botActive = True
firstStart = True
apaContractAddress = "0x770a4c7f875fb63013a6db43ff6af9980fceb3b8"
waitTime = 5
lastTxTime = ""

def moralisRequest(query):
    apiURL = query
    response = requests.request("GET", apiURL, headers=headers)
    returnResponse = response.json()
    return returnResponse

while botActive:
    lastTxsRequest = moralisRequest("https://deep-index.moralis.io/api/v2/0x770a4c7f875fb63013a6db43ff6af9980fceb3b8?chain=avalanche&limit=20")["result"]
    if lastTxsRequest[0]["block_timestamp"] > lastTxTime:
        print("new transaction arrived. being checked")
        lastTxs = lastTxsRequest[::-1]
        for tx in lastTxs:
            txHash = tx["hash"]
            txData = moralisRequest("https://deep-index.moralis.io/api/v2/transaction/" + txHash + "?chain=avalanche")
            if txData["logs"] != [] and txData["block_timestamp"] > lastTxTime:
                if txData["to_address"] == apaContractAddress and len(txData["logs"][0]["data"]) == 706:
                    txLogDataHex = txData["logs"][0]["data"]
                    nftId = int(txLogDataHex[194:258],16)
                    nftPrice = int(txLogDataHex[258:322],16) / 10**18
                    nftData = apaData[str(nftId)]
                    print("Listing Update -- " + str(nftId) + " id APA nft is " + str(nftPrice) + " avax listed.")
                    print("Rarity : " + nftData["rarity"]) # Bu kısma apa databasesinde bulunan diğer özellikleri de yazdırabilirsiniz. Örneğin : "nftData["rarity"]" owner, token_id, color, fur, cloth, earring, glass, hat, necklace, mouth, rarity_point, rarity
                    print("-------------------------------------------------")
                elif txData["to_address"] == apaContractAddress and len(txData["logs"][0]["data"]) == 642:
                    txLogDataHex = txData["logs"][0]["data"]
                    nftId = int(txLogDataHex[194:258], 16)
                    print("Listing Canceled -- " + str(nftId) + " id APA nft is cancelled.")
                    print("-------------------------------------------------")
    lastTxTime = lastTxsRequest[0]["block_timestamp"]
    if firstStart == True:
        print("Last data okay. Tracking apa...")
        firstStart = False
    time.sleep(waitTime)

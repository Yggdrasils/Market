import time
import json
import requests

class market(object):
    
    def __init__(self):
        self.market_api_url = "https://market-api.radiocaca.com/nft-sales/"
        self.market_url = "https://market.radiocaca.com/#/market-place/"
        self.nft_category = {"Potion" : "15", "Diamond" : "16", "Egg" : "17"}
        self.payload = {"pageNo": "1", "pageSize": 10, "sortBy": "single_price", "order": "asc", "name": "", "saleType": "", "category": "", "tokenType": ""}

    def get_nft(self, name, number=20):
        self.payload["category"] = self.nft_category[name]
        self.payload["pageSize"] = number
        self.r = json.loads(requests.get(self.market_api_url, params=self.payload).text)
        self.nft_list = self.r["list"]
        for nft in self.nft_list:
            s = name + ": x" + str(nft["count"]).ljust(4) + "  unit price: " + str(int(nft["fixed_price"])//nft["count"]) + "  total price: " + str(nft["fixed_price"]).ljust(9) + "  url: " + self.market_url + str(nft["id"])
            print(s)

    def get_metamon(self, number=20):
        self.payload["category"] = "13"
        self.payload["pageSize"] = number
        self.r = json.loads(requests.get(self.market_api_url, params=self.payload).text)
        self.ids = [i["id"] for i in self.r["list"]]
        self.urls = [self.market_api_url+str(id) for id in self.ids]
        for url in self.urls:
            res = json.loads(requests.get(url).text)
            time.sleep(0.5)
            data = res["data"]
            properties = data["properties"]
            rarity = ""
            score = ""
            for i in properties:
                if i["key"] == "Rarity":
                    rarity = i["value"]
                if i["key"] == "Score":
                    score = i["value"]
            s = str(data["token_id"]) + " Metamon: " + rarity + "  score: " + score + "  price: " + str(data["total_price"]).ljust(7) + "  url: " + self.market_url
            print(s)

if __name__ == "__main__":
    my_market = market()
    my_market.get_nft("Diamond", 20)  # name = ["Potion", "Diamond", "Egg"]
    my_market.get_metamon(10)

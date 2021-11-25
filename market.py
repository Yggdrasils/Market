import time
import json
import requests

class market(object):
    
    def __init__(self):
        self.market_api_url = "https://market-api.radiocaca.com/nft-sales/"
        self.market_url = "https://market.radiocaca.com/#/market-place/"
        self.nft_category = {"N":13, "R":23, "SR":24, "SSR":25, "Potion":15, "Diamond":16, "Egg":17, "Kiss":"20", "MML":7, "MPB":10}
        self.payload = {"pageNo": "1", "pageSize": 10, "sortBy": "single_price", "order": "asc", "name": "", "saleType": "", "category": "", "tokenType": ""}

    def price_sort(self, sort=1):
        if sort == 1:
            self.payload["order"] = "asc"
        if sort == -1:
            self.payload["order"] = "desc"

    def get_1155_nft(self, name, number=20):
        self.payload["category"] = self.nft_category[name]
        self.payload["pageSize"] = number
        self.r = json.loads(requests.get(self.market_api_url, params=self.payload).text)
        self.nft_list = self.r["list"]
        for nft in self.nft_list:
            s = name + ": x" + str(nft["count"]).ljust(4) + "  unit price: " + str(int(nft["fixed_price"])//nft["count"]) + "  total price: " + str(nft["fixed_price"]).ljust(9) + "  url: " + self.market_url + str(nft["id"])
            print(s)

    def get_721_nft(self, name, number=20):
        self.payload["category"] = self.nft_category[name]
        self.payload["pageSize"] = number
        self.r = json.loads(requests.get(self.market_api_url, params=self.payload).text)
        self.nft_list = self.r["list"]
        for nft in self.nft_list:
            s = str(nft["token_id"]).ljust(7) + " " + name + "  price: " + str(nft["fixed_price"]).ljust(9) + "  url: " + self.market_url + str(nft["id"])
            print(s)

    def get_metamon(self, name, number=20):
        self.payload["category"] = self.nft_category[name]
        self.payload["pageSize"] = number
        self.r = json.loads(requests.get(self.market_api_url, params=self.payload).text)
        self.ids = [i["id"] for i in self.r["list"]]
        self.urls = [self.market_api_url+str(id) for id in self.ids]
        for url in self.urls:
            res = json.loads(requests.get(url).text)
            time.sleep(0.5)
            nft = res["data"]
            properties = nft["properties"]
            for i in properties:
                if i["key"] == "Rarity":
                    rarity = i["value"]
                if i["key"] == "Score":
                    score = i["value"]
                if i["key"] == "Level":
                    level = i["value"]
            s = str(nft["token_id"]) + " Metamon: " + rarity + "  level: " + level + "  score: " + score + "  price: " + str(nft["fixed_price"]).ljust(9) + "  url: " + self.market_url + str(nft["id"])
            print(s)

if __name__ == "__main__":
    my_market = market()
    my_market.price_sort = 1    # 1 is ascending order while -1 is descending order
    my_market.get_1155_nft("Diamond", 10)  # name = ["Potion", "Diamond", "Egg"]
    my_market.get_1155_nft("Egg", 10)
    my_market.get_1155_nft("Potion", 10)
    my_market.get_721_nft("MPB", 10)       # name = ["MPB", "MML", "Kiss"]
    my_market.get_metamon("R", 5)  # name = ["N", "R", "SR", "SSR"]

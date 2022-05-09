import requests
import bs4
from tqdm import tqdm
import json

def main():
    itemScrapped = 0
    classSelectors = ["Uniqueunique_listtitleWeapon","Uniqueunique_listtitleArmour","Uniqueunique_listtitleOther"]
    resultDict = {}


    print("poedb.tw - WebScrap start")
    site = requests.get("https://poedb.tw/us/Unique_item")
    html = bs4.BeautifulSoup(site.text, 'html.parser')

    for selector in classSelectors:
        itemUrlCssSelector = f'#{selector} > div:nth-child(1)'

        itemUrl = html.select_one(itemUrlCssSelector)

        siteBaseUrl = "https://poedb.tw{}"
        for item in tqdm(itemUrl.find_all('a',{"class": "item_unique"}, href=True)):
            itemSiteUrl = siteBaseUrl.format(item['href'])
            itemSiteHtml = requests.get(itemSiteUrl)
            itemSiteParse = bs4.BeautifulSoup(itemSiteHtml.text, 'html.parser')

            itemTypeSelector = ".ItemType"
            itemNameSelector = ".ItemName"
            itemImageSelector = ".itemboximage > img"


            itemName = itemSiteParse.select_one(itemNameSelector)
            itemType = itemSiteParse.select_one(itemTypeSelector)
            itemImage = itemSiteParse.select_one(itemImageSelector).attrs["src"]

            specificInfoTableCssSelector = ".page-content"
            rowDict = {'base:': itemType.text, 'name':itemName.text, 'icon': itemImage}
            itemSpecificInfoTable = itemSiteParse.select(specificInfoTableCssSelector)

            resultDict.update({"{}".format(itemName.text): rowDict})

            print(rowDict)
            itemScrapped += 1



    site = requests.get("https://poedb.tw/us/Cluster_Jewel")
    html = bs4.BeautifulSoup(site.text, 'html.parser')
    itemUrlCssSelector = f'#Deliriumunique_cluster_jewel > div:nth-child(1)'

    itemUrl = html.select_one(itemUrlCssSelector)

    siteBaseUrl = "https://poedb.tw{}"
    for item in tqdm(itemUrl.find_all('a',{"class": "item_unique"}, href=True)):
        itemSiteUrl = siteBaseUrl.format(item['href'])
        itemSiteHtml = requests.get(itemSiteUrl)
        itemSiteParse = bs4.BeautifulSoup(itemSiteHtml.text, 'html.parser')

        itemTypeSelector = ".ItemType"
        itemNameSelector = ".ItemName"
        itemImageSelector = ".itemboximage > img"

        itemName = itemSiteParse.select_one(itemNameSelector)
        itemType = itemSiteParse.select_one(itemTypeSelector)
        itemImage = itemSiteParse.select_one(itemImageSelector).attrs["src"]

        specificInfoTableCssSelector = ".page-content"
        rowDict = {'base:': itemType.text, 'name':itemName.text, 'icon': itemImage}
        itemSpecificInfoTable = itemSiteParse.select(specificInfoTableCssSelector)

        resultDict.update({"{}".format(itemName.text): rowDict})
        print(rowDict)
        itemScrapped += 1


    with open("uniqueBases.json", 'w') as json_file:
        print(json.dumps(resultDict), file=json_file)


main()

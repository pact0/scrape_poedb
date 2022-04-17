import requests
import bs4
from tqdm import tqdm
import json

def main():
    itemScrapped = 0

    print("poedb.tw - WebScrap start")
    site = requests.get("https://poedb.tw/us/Unique_item")
    html = bs4.BeautifulSoup(site.text, 'html.parser')

    itemUrlCssSelector = "#Uniqueunique_listtitleWeapon > div:nth-child(1)"

    itemUrl = html.select_one(itemUrlCssSelector)

    resultDict = {}
    siteBaseUrl = "https://poedb.tw{}"
    for item in tqdm(itemUrl.find_all('a',{"class": "item_unique"}, href=True)):
        itemSiteUrl = siteBaseUrl.format(item['href'])
        itemSiteHtml = requests.get(itemSiteUrl)
        itemSiteParse = bs4.BeautifulSoup(itemSiteHtml.text, 'html.parser')

        itemTypeSelector = ".ItemType"
        itemNameSelector = ".ItemName"

        itemName = itemSiteParse.select_one(itemNameSelector)
        itemType = itemSiteParse.select_one(itemTypeSelector)

        specificInfoTableCssSelector = ".page-content"
        rowDict = {'type:': itemType.text}
        itemSpecificInfoTable = itemSiteParse.select(specificInfoTableCssSelector)
        for tableItem in itemSpecificInfoTable[0].find_all('td'):
            if (tableItem.text.find("Art/") != -1):
                rowDict.update({'icon': tableItem.text})
                break

        resultDict.update({"{}".format(itemName.text): rowDict})
        itemScrapped += 1
    with open("outputFile.txt", 'w') as output_file:
        print(resultDict, file=output_file)
    with open("outputJson.json", 'w') as json_file:
        print(json.dumps(resultDict), file=json_file)


main()

import requests
import bs4
from tqdm import tqdm
import json

def main():
    itemScrapped = 0
    resultDict = {}
    pages = ["Claws","Daggers","Wands","One Hand Swords","Thrusting One Hand Swords","One Hand Axes","One Hand Maces","Sceptres","Rune Daggers",
        "Bows","Staves","Two Hand Swords","Two Hand Axes","Two Hand Maces","Warstaves","Fishing Rods",
        "Quivers","Shields",
        "Gloves","Boots","Body Armours","Helmets",
        "Amulets","Rings","Belts","Trinkets",
        "Jewels","Abyss Jewels"
    ]

    baseUrl = "https://poedb.tw/us/"


    for item in pages:
        page = baseUrl + ("_").join(item.split(" ")) + "#" + ("").join(item.split(" ")) + "Item"

        print(page)

        site = requests.get(page)
        html = bs4.BeautifulSoup(site.text, 'html.parser')

        selector = ("").join(item.split(" ")) + "Item"


        itemUrlCssSelector = f'#{selector} > div:nth-child(2)'

        itemUrl = html.select_one(itemUrlCssSelector)

        siteBaseUrl = "https://poedb.tw{}"

        for item in tqdm(itemUrl.find_all('a',{"class": "whiteitem"}, href=True)):
            itemSiteUrl = siteBaseUrl.format(item['href'])
            itemSiteHtml = requests.get(itemSiteUrl)
            itemSiteParse = bs4.BeautifulSoup(itemSiteHtml.text, 'html.parser')

            itemTypeSelector = ".ItemType"
            itemImageSelector = ".itemboximage > img"



            itemName = itemSiteParse.select_one(itemTypeSelector)
            itemType = itemSiteParse.select_one(itemTypeSelector)

            itemImage = itemSiteParse.select_one(itemImageSelector).attrs["src"]


            specificInfoTableCssSelector = ".page-content"
            rowDict = {'base:': itemType.text, 'icon': itemImage}

            itemSpecificInfoTable = itemSiteParse.select(specificInfoTableCssSelector)

            resultDict.update({"{}".format(itemName.text): rowDict})

            print(rowDict)
            itemScrapped += 1



    page = "https://poedb.tw/us/Flasks#Flask"

    print(page)

    site = requests.get(page)
    html = bs4.BeautifulSoup(site.text, 'html.parser')

    selector = "Flask"


    itemUrlCssSelector = f'#{selector} > div:nth-child(2)'

    itemUrl = html.select_one(itemUrlCssSelector)

    siteBaseUrl = "https://poedb.tw{}"

    for item in tqdm(itemUrl.find_all('a',{"class": "whiteitem"}, href=True)):
        itemSiteUrl = siteBaseUrl.format(item['href'])
        itemSiteHtml = requests.get(itemSiteUrl)
        itemSiteParse = bs4.BeautifulSoup(itemSiteHtml.text, 'html.parser')

        itemTypeSelector = ".ItemType"
        itemImageSelector = ".itemboximage > img"



        itemName = itemSiteParse.select_one(itemTypeSelector)
        itemType = itemSiteParse.select_one(itemTypeSelector)

        itemImage = itemSiteParse.select_one(itemImageSelector).attrs["src"]


        specificInfoTableCssSelector = ".page-content"
        rowDict = {'base:': itemType.text, 'icon': itemImage}

        itemSpecificInfoTable = itemSiteParse.select(specificInfoTableCssSelector)

        resultDict.update({"{}".format(itemName.text): rowDict})

        print(rowDict)
        itemScrapped += 1





    with open("rareBaseIcons.json", 'w') as json_file:
        print(json.dumps(resultDict), file=json_file)


main()

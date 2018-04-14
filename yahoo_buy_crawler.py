import pandas as pd
import requests as r
from bs4 import BeautifulSoup
import json
import csv


def yahoo_buy_crawler():
    url = "https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew?segmentId=999999&subId=464,536,23,70,583,9,1,56,35,51&t=1523689806655"
    content = json.loads(r.get(url).text, encoding="utf-8")

    #     find items price
    def mainitem_price(i):
        price_soup = BeautifulSoup(content['billboard']['panels'][i]["mainitem"]["price"], 'html5lib')
        if price_soup.select("span.shpprice")[0].text.isdigit():
            return (int(price_soup.select("span.shpprice")[0].text))
        else:
            return -1000

    def pditem_price(i, j):
        price_soup = BeautifulSoup(content['billboard']['panels'][i]['pditem'][j]["price"], 'html5lib')
        if price_soup.select("span.shpprice")[0].text.isdigit():
            return (int(price_soup.select("span.shpprice")[0].text))
        else:
            return -1000


    #     make label list

    list_of_dict = []
    list_of_label = []
    for i in content['billboard']['tabs']:
        list_of_dict.append({"label": i["label"], "items": []})
        list_of_label.append(i["label"])
    for i in content['billboard']['othertab']:
        list_of_dict.append({"label": i["label"], "items": []})
        list_of_label.append(i["label"])

    for z in list_of_label:
        print(z)
    # append items
    for i in range(10):
        list_of_dict[i]["items"].append(
            dict(name=content['billboard']['panels'][i]["mainitem"]["desc"], price=mainitem_price(i)))
        for j in range(4):
            list_of_dict[i]["items"].append(
                dict(name=content['billboard']['panels'][i]['pditem'][j]["desc"], price=pditem_price(i, j)))

            # make dataframe
    frames = []
    for i in list_of_dict:
        temp = pd.DataFrame.from_dict(i, orient='columns')
        frames.append(temp)
    df_temp = pd.concat(frames)
    df_temp["price"] = [x["price"] for x in df_temp["items"]]
    df_temp["name"] = [x["name"] for x in df_temp["items"]]
    df_temp = df_temp[["name", "price", "label"]]

    return df_temp

def main():
    df_temp = yahoo_buy_crawler()
    cata = input("Choose one catagory to make CSV, or choose 'ALL' to see all.")
    if cata != "ALL":
        cata_str = str(cata)
        df_part = df_temp[df_temp["label"]==cata_str]
        print(df_part.to_string())
        cata_name = str(cata).replace("/","_").strip()
        df_part.to_csv("goods_%s.csv"%cata_name, sep='\t',encoding="Big5")
    else:
        print(df_temp.to_string())
        df_temp.to_csv("goods_all.csv", sep='\t',encoding="Big5")

if __name__ == "__main__":
    main()


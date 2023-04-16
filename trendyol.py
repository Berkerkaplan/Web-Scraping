import requests

from bs4 import BeautifulSoup

import json

from fake_useragent import UserAgent


def getDataFromTrendyol(url, header,):
    try:
        response = requests.get(url,headers=header)
        print("Response status code:" + str(response.status_code))
        image_url = 'https://www.trendyol.com'

        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        #print(soup.prettify)

        products = soup.find_all("article", attrs={"class" : "component-item"})
        
        #print(products)
        with open("trendyol.json", "w") as f:
            for product in products:
                product_links = product.find_all("a")
                for product_link in product_links:
                    each_links = product_link['href']
                    categories = requests.get(each_links, headers=header)
                    #print("Response status categories:" + str(categories.status_code))
                    categories_html = BeautifulSoup(categories.content, "html.parser")
                    categories_detail = categories_html.find_all("div", attrs={"class" : "p-card-chldrn-cntnr card-border"})
                    #print("category " + str(categories_html))
                    for categorie_detail in categories_detail:
                        product_title = categorie_detail.find("span" , {"class" : "prdct-desc-cntnr-ttl"}).getText()
                        
                        product_price = categorie_detail.find("div", {"class" : "prc-box-dscntd"}).getText()
                        
                        try: 
                            product_price_2 = categorie_detail.find("div", {"class" : "prc-box-orgnl"}).getText()  
                        except Exception:
                            product_price_2 = "There is no discount"
                        #product_id = categorie_detail.find("div", {"class" : "p-card-wrppr with-campaign-view"}).getId()
                        product_brand = categorie_detail.find("span" , {"class" : "prdct-desc-cntnr-ttl"}).getText()
                        product_description = categorie_detail.find("span", {"class" : "prdct-desc-cntnr-name"}).getText()
                        product_image_endpoint = categorie_detail.a.get("href")
                        product_image_url = image_url + product_image_endpoint

                        data = {
                        "product_title" : product_title,
                        "product_price" : product_price,
                        "product_price_2" : product_price_2, 
                        "product_brand" : product_brand,
                        "product_description" : product_description,
                        "product_image" : product_image_url, 
                        }
                        json.dump(data, f)
                        f.write('\n' + '***********' + '\n')
    except requests.exceptions.RequestException as e:
        print(e)
      
     

getDataFromTrendyol(
    'https://www.trendyol.com/butik/liste/2/erkek',
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    )


import requests
from bs4 import BeautifulSoup
import time
import json


def parse_page(url):
    headers={"Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru,en;q=0.9,sr;q=0.8",
    "Cookie": "is_gdpr=0; yandexuid=5389104661604743805; _ym_uid=1604743815864509069; my=YwA=; yuidss=5389104661604743805; is_gdpr_b=COC+ehC2UigC; gdpr=0; i=yF4e3166JyKP80rUSSv4nh1AdUwU26V4OyOARsuTyRmdHAC9GyNxaGscpawldGrX7CzZw/s+xwqUq5rTcc0utaI/DvU=; ymex=1999865822.yrts.1684505822; yandex_login=oxanarublyovskaya; sae=0:53FC5F44-B6EF-4242-8524-80E0319E836A:p:23.7.2.767:w:d:RU:20201107; ys=svt.1#def_bro.1#wprid.1692261536551702-686292205951021043-balancer-l7leveler-kubr-yp-sas-150-BAL-7510#ybzcc.ru#newsca.native_cache; Session_id=3:1692261540.5.0.1684507361282:XPaXLg:14.1.2:1|1645265757.-1.2.3:1684507361|3:10274391.664239.itJsv1KXMKB1K-ng7STfcV68f9c; sessar=1.1181.CiAQ8X64FJY8nUuNnkF384zTY93Z4bW9c14-leH7DAPETQ.oXL8sIvaqtyQLXygdckiu8hGvGaq_sMaHGoLh_Vk8lc; sessionid2=3:1692261540.5.0.1684507361282:XPaXLg:14.1.2:1|1645265757.-1.2.3:1684507361|3:10274391.664239.fakesign0000000000000000000; yp=1692347918.uc.ru#1692347918.duc.ru#1716043362.cld.1985104#1693564816.hdrc.1#1991469490.multib.1#2007621540.pcs.1#1701528885.pgp.5_27833214#1706677009.szm.1:1366x768:1318x652#1999867361.udn.cDpveGFuYXJ1Ymx5b3Zza2F5YQ%3D%3D#1693587417.csc.1#1723797540.stltp.serp_bk-map_1_1692261540#1692434341.gpauto.44_121364:39_071792:140:1:1692261531; yabs-sid=1709093671692261541; _ym_isad=2; bh=EjkiTm90LkEvQnJhbmQiO3Y9IjgiLCJDaHJvbWl1bSI7dj0iMTE0IiwiWWFCcm93c2VyIjt2PSIyMyIaBSJ4ODYiIgwiMjMuNy4yLjc2NyIqAj8wOgkiV2luZG93cyJCCCIxMC4wLjAiSgQiNjQiUlMiTm90LkEvQnJhbmQiO3Y9IjguMC4wLjAiLCJDaHJvbWl1bSI7dj0iMTE0LjAuNTczNS4yNDgiLCJZYUJyb3dzZXIiO3Y9IjIzLjcuMi43NjciIg==",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.767 Yowser/2.5 Safari/537.36"}

    req = requests.get(url, headers=headers)
    bs = BeautifulSoup(req.text, "lxml")
    time.sleep(2)
    h3_tags = bs.find_all("h3")
    btn_prices = bs.find_all("div", class_="btns-prices")

    page_data = []
    for i, h3_tag in enumerate(h3_tags):
        name = h3_tag.find("a").text
        if i < len(btn_prices):
            price = btn_prices[i].find('ins').text
            page_data.append({"name": name, "price": price})
        else:
            page_data.append({"name": name, "price": "Цена не указана"})

    return page_data


def scrape_data(url, num_pages=2):
    all_data = []
    for page_num in range(1, num_pages + 1):
        page_url = f"{url}{page_num}"
        page_data = parse_page(page_url)
        all_data.extend(page_data)
     

    return all_data


def save_data(data, filename="data.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    base_url = "https://aloeapteka.ru/catalog/suxie-i-povrezhdennye-volosy-1002/?page_num="
    data = scrape_data(base_url, num_pages=2)
    save_data(data, "data.json")

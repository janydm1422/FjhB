
import datetime
import os
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import hmac,hashlib,urllib,base64,requests
def playwright_get_url(url, delay=0, headless=True):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=headless)
        try:
            page = browser.new_page()
            page.goto(url=url)
            import time
            time.sleep(20)
            html = page.inner_html("*")
        except:
            GET_PAGE_SOURCE_ERROR_MSG = "Get page source error!"
            raise Exception(GET_PAGE_SOURCE_ERROR_MSG)
        finally:
            browser.close()
        return BeautifulSoup(html, 'lxml')
      
def process_steamdb_result(steamdb_result,msg):
    for each_tr in steamdb_result.select(".app"):
        if "hidden" in each_tr.attrs.keys():
            continue
        steamdb_url = "N/A"
        tds = each_tr.find_all("td")
        tds_length = len(tds)
        if len(tds[tds_length - 3].contents) == 1:
            free_type = tds[tds_length - 3].contents[0]
        else:
            free_type = tds[tds_length - 3].contents[2].contents[0] + "Forever"
        start_time_str = str(tds[tds_length - 2].get("data-time"))
        end_time_str = str(tds[tds_length - 1].get("data-time"))
        url="htt"+"ps://stea"+"mdb.info/upco"+"ming/free/"
        steamdb_url = urljoin(url, str(tds[tds_length - 5].contents[1].get("href")))
        game_name = str(tds[tds_length - 5].find("b").contents[0])
        sub_id = str(tds[tds_length - 5].contents[1].get('href').split('/')[2])
        steam_url = str(tds[tds_length - 6].contents[1].get('href')).split("?")[0]
        msg=msg+"n:" + game_name+'|d'+'bu:'+steamdb_url+"|u:" + steam_url+'|t:'+free_type
    return msg

def main():
    url1="htt"+"ps://ste"+"amdb.info/upco"+"ming/fr"+"ee/"
    html = playwright_get_url(url=url1, delay=15, headless=True)
    from datetime import datetime;import pytz
    msg='采集时间：{}\n\n'.format(datetime.fromtimestamp(int(time.time()),pytz.timezone('Asia/Shanghai')).strftime('%Y{y}%m{m}%d{d}%H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒'))
    content=process_steamdb_result(steamdb_result=html,msg=msg)
    return content
      
if __name__ == "__main__":
    import hmac,hashlib,requests
    msg=main()
    with open (os.path.join(os.getcwd(), "README.md"), 'w', encoding='utf-8') as f:
        f.write(msg)
        print('修改成功!')

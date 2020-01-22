import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
import http.cookiejar
import urllib.request

df = pd.DataFrame(columns=['Quote', 'Tag', 'Author', 'Author_url', 'Publisher', 'Publisher_url'])
df.to_csv('quotes_login_scrap.csv', index=False)

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

form_data = {
    #'csrf_token': 'HFSwTtOnfhqjuCpKrsNyxYgzBaDRWXAMokcQdiUZJGeLlEmbVPvI',    # Not defined as it dynamically changes
    'username': 'angel.raj.01992@gmail.com',
    'password': 'Raju@12345'
}

with requests.session() as s:
    authentic_url = 'http://quotes.toscrape.com/login'
    r = s.get(authentic_url)
    page_soup = soup(r.content, 'html5lib')
   
# finding the csrf_token as it dynamically changes
    form_data['csrf_token'] = page_soup.find('input', attrs={'name':'csrf_token'})['value']
    r = s.post(authentic_url, data= form_data, headers= headers)
    login_page_soup = soup(r.content, 'html5lib')
#    print(login_page_soup)
    #print(r.content)

    _page = 1
    for _page in range (1,4):
        try:
            url = 'http://quotes.toscrape.com/page/'+ str(_page) +'/'
            req = s.get(url)
            q_soup = soup(req.content, 'html5lib')
          
            _table = q_soup.findAll('div', attrs={'class' : 'quote'})
       
            try:
                _publisher = q_soup.find('p', attrs={'class': 'text-muted'}).find('a').text
            except Exception:
                _publisher = 'NA'
                pass
            try:
                _publisher_url = q_soup.find('p', attrs={'class': 'text-muted'}).find('a')['href']
            except Exception:
                _publisher_url = 'NA'
                pass

            for _row in _table:
                try:
                    _quote = _row.find('span').text     # q_soup.findAll('div', attrs={'class' : 'quote'})[00].contents[1].text
                except Exception:
                    _quote = 'NA'
                    pass
                try:
                    _tag = _row.find('meta')['content']
                except Exception:
                    _tag = 'NA'
                    pass
                try:
                    _author = _row.find('small').text
                except Exception :
                    _author = 'NA'
                    pass
                try:
                    _author_url = _row.findAll('span')[1].find('a')['href']     
                except Exception:
                    _author_url = 'NA'
                    pass

                print('Quote : '+_quote+ '  : Tag : '+_tag+ '  : Author : '+_author+ '  :  Author_url :  '+_author_url+ '  :  Publisher :  '+_publisher+ '  :  Publisher_url :  ' +_publisher_url)

                try:
                    df = df.append(
                            {'Quote' : _quote, 'Tag' : _tag, 'Author' : _author, 'Author_url' : _author_url,
                             'Publisher' : _publisher, 'Publisher_url' : _publisher_url}, ignore_index=True)
                except Exception:
                    print('Not Added to DF')
                    pass
               
        except Exception:
            print("URL NOT FOUND :  FOR PAGE :  " +str(_page))
            pass
        print("COMPLETED PAGE :  " + str(_page))
        _page += 1



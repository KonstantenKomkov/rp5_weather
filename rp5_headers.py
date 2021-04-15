def get_header(phpsessid, browser):
    rp5 = {
        'Chrome': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '108',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={phpsessid}; located=1; extreme_open=false; full_'
                      f'table=1; tab_wug=1; ftab=2; tab_metar=1; zoom=11; i=6106%7C3708%7C4012%7C5174%7C6151; '
                      f'iru=6106%7C3708%7C4012%7C5174%7C6151; ru=%D0%9D%D0%BE%D1%80%D0%B8%D0%BB%D1%8C%D1%81%D0%BA'
                      f'%7C%D0%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B0%7C%D0%9A%D0%B8%D1%80%D0%BE%D0%B2+%28%D1%80%D0%B0%D0'
                      f'%B9%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9+%D1%86%D0%B5%D0%BD%D1%82%D1%80%29%7C%D0%9C%D0%B0%D0%BB%D0'
                      f'%BE%D1%8F%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B5%D1%86%7C%D0%9E%D0%B1%D0%BD%D0%B8%D0%BD'
                      f'%D1%81%D0%BA; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                      f'%D0%B2_%D0%9E%D0%B1%D0%BD%D0%B8%D0%BD%D1%81%D0%BA%D0%B5; tab_synop=2; format=xls; '
                      f'f_enc=ansi; lang=ru',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'},
        'Firefox': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'tab_synop=2; __utma=66441069.787260057.1615713964.1616872108.1618399838.3; '
                      f'__utmz=66441069.1618399838.3.2.utmcsr=yandex.ru|utmccn=(referral)|utmcmd=referral|utmcct=/; '
                      f'cto_bundle=n2gUNl9lZEFyNlVtQmhuQk84QXNmdHliRXVuNkpBU2glMkZHaFhXTUpDUzNjb085TVoxRmdndExnejVxUz'
                      f'VodEI3TDA2NEJJMldBQW5JdyUyQkd2dzNDZzE5OWl5YWxRSFJQVUZJbkU1dEE1U0pNSG5DSHpZQ2p0MHBHdkFpV3lIc'
                      f'XBEMDclMkZsVmYlMkJkQkJ6OEdOJTJGaXZBUTB4dUJ6TWN3JTNEJTNE; __utmb=66441069.7.10.1618399838; '
                      f'__utmt=1; extreme_open=false; __gads=ID=8c18f2d64afa91f2-22c8466915bb00f9:T=1618399837:RT='
                      f'1618399837:S=ALNI_MY3hQkYRVTh3Y2OwwZGFs-dJxR9kA; tab_metar=1; PHPSESSID={phpsessid}; '
                      f'i=3609%7C3609; iru=3609%7C3609; ru=%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B0%7C'
                      f'%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B0; last_visited_page=http%3A%2F%2Frp5.ru'
                      f'%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0'
                      f'%BB%D0%B5; __utmc=66441069; format=xls; f_enc=ansi; lang=ru',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'X-Requested-With': 'XMLHttpRequest'
        },
        'Opera': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={phpsessid}; i=3609; iru=3609; ru=%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB'
                      f'%D0%B0; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0'
                      f'%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B5; __utma=66441069.2058564896.1618400458.'
                      f'1618400458.1618400458.1; __utmc=66441069; __utmz=66441069.1618400458.1.1.utmcsr=yandex.ru|'
                      f'utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; extreme_open=false; __gads=ID='
                      f'641633653496891c-2277e3ec16bb0088:T=1618400457:RT=1618400457:S=ALNI_MbOXRCZKZ-4xFvhddq-wLOB1Lo'
                      f'VIA; lang=ru; tab_synop=1; format=xls; f_enc=ansi; __utmb=66441069.2.10.1618400458',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.'
                          '4389.90 Safari/537.36 OPR/75.0.3969.149 (Edition Yx)',
            'X-Requested-With': 'XMLHttpRequest'
        },
        'InternetExplorer': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={phpsessid}; i=3609; iru=3609; ru=%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB'
                      f'%D0%B0; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_'
                      f'%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B5; __utma=66441069.1198019390.1618400812'
                      f'.1618400812.1618400812.1; __utmb=66441069.2.10.1618400812; __utmc=66441069; __utmz=66441069.'
                      f'1618400812.1.1.utmcsr=yandex|utmccn=(organic)|utmcmd=organic|utmctr=rp5%20%D0%B9%D0%BE%D1%88'
                      f'%D0%BA%D0%B0%D1%80-%D0%BE%D0%BB%D0%B0; __utmt=1; extreme_open=false; __gads=ID='
                      f'470c761a5e850682-22e4827319bb00f1:T=1618400811:RT=1618400811:S=ALNI_MZ3pN9R84CXh5t2r56hJSNz'
                      f'FUtKKg; is_adblock=0; lang=ru; tab_synop=1; format=xls; f_enc=ansi',
            'Host': 'rp5.ru',
            'Referer': 'https://rp5.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest'
        },
        'Edge': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={phpsessid}; i=3609; iru=3609; ru=%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB'
                      f'%D0%B0; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_'
                      f'%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B5; __utmc=66441069; __utmz=66441069.'
                      f'1618407914.1.1.utmcsr=yandex.ru|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utma='
                      f'66441069.1581379392.1618407914.1618407914.1618407914.1; extreme_open=false; __gads=ID='
                      f'c061f780892a85c1-2227c4cd1cbb0061:T=1618407914:RT=1618407914:S=ALNI_MYRzVuT1SM7ecW3kjLXb5Zya'
                      f'VxgGw; cto_bundle=hemzUl9adTRiSVBqZ1dyQlMxNGRqMHQ0eXEzRyUyRmNiZWFINlhjekhxZGdTYkdMVlBXb0ljc'
                      f'09oQkhqUkU3JTJGVzkwSldsTCUyRlg5QVo0SGU4OFhIVVJkVnQ1YmpVRE9IelhEalElMkJjVkQlMkZPNmd3dU5qZTFObn'
                      f'NuZjkzNllXQlBEN0lyRW4zRW9MTnNsRjViUUlMckxzN2Z2VW5lREZBJTNEJTNE; lang=ru; tab_synop=1; format='
                      f'xls; f_enc=ansi; __utmb=66441069.2.10.1618407914',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
            'X-Requested-With': 'XMLHttpRequest'
        },
        'Yandex': {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={phpsessid}; i=3609; iru=3609; ru=%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB'
                      f'%D0%B0; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_'
                      f'%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B5; __utmc=66441069; __utmz=66441069.'
                      f'1618408280.1.1.utmcsr=yandex.ru|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; '
                      f'__utma=66441069.332888648.1618408280.1618408280.1618408280.1; extreme_open=false; __gads=ID='
                      f'c7facce91ec9beab-2267232117bb0050:T=1618408279:RT=1618408279:S=ALNI_MYRrIx-y-iibCFf5SdGBh'
                      f'Nivovuww; lang=ru; tab_synop=1; format=xls; f_enc=ansi; __utmb=66441069.2.10.1618408280',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }
    return rp5[browser]

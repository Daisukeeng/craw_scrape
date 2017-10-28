import requests
import lxml.html
import time

def craw():
    #まずは中央線各駅が一覧乗っているページURLを基に各駅のタグを取得
    baseurl='http://www.athome.co.jp/chintai/tokyo/chuo-line/'
    session=requests.Session()
    response=session.get(baseurl)
    html=lxml.html.fromstring(response.content)
    a_list=html.xpath('//li[@class]/label/span/a')  #各駅に飛ぶURLのaタグまで絞り込む


    #中央線各駅のURLと各駅名を取得
    for i in range(0, len(a_list)):
        station_url = a_list[i].get('href') #URLを取得
        station_name = a_list[i].text   #駅名を取得
        print('station: ' + station_name)

        k=1

        #各駅のリンクの先にあるページを取得
        while(True):
            #url = 'http://www.athome.co.jp'+station_url + 'page' + str(k)
            url = 'http://www.athome.co.jp{}page{}'.format(station_url,k)
            time.sleep(1)
            response_html=session.get(url)
            response_html.encoding='utf-8'

            #存在しないページのループ抜け
            if(response_html.status_code == 404):
                break



            #ファイルの保存
            #html_name = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_' + station_name + str(k) + '.html '
            html_name = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_{}{}.html '.format(station_name,k)
            with open(html_name, 'w',encoding='utf-8') as f:
                f.write(response_html.text)
            print('page_'+ station_name  + str(k))

            k+=1

craw()
from bs4 import BeautifulSoup
import re
import csv
import os.path


def scrape(response,listdate,station,i):
    #各物件に対し情報取得
    soup = BeautifulSoup(response, "html.parser")
    for a in soup.find_all('section',class_='p-property'):      #閲覧ページ内にある各物件のタグ

        name=a.find('span',class_='p-property__title-text')     #物件名取得
        rent=a.find('b',class_='p-property__information-rent')  #家賃取得


        """
        所有面積の取得
        所有面積の部分だけタグが複雑なので正規表現で取得
        """
        for c in a.find_all('dd'):
            temp = c.text
            menseki = re.search(r"\(.+m²\)" ,temp)

            if menseki != None:
                menseki2 = menseki.group().replace("(","").replace(")","").replace("m²","")

                listdate.append([station[i],name.text,rent.text,menseki2])

#CSVに保存
def save_csv(listdate):
    with open('Chuo_line2.csv','w',newline='') as f:
        f.write('最寄駅,物件名,家賃,専有面積(m2)\n')  #CSVファイルのヘッダー
        writer = csv.writer(f)
        writer.writerows(listdate)



def main():
    station = ["東京","神田","御茶ノ水","四ツ谷","新宿","中野","高円寺","阿佐ヶ谷",
               "荻窪","西荻窪","吉祥寺","三鷹","武蔵境","東小金井","武蔵小金井",
               "国分寺","西国分寺","国立","立川","日野","豊田","八王子","西八王子",
               "高尾"]
    listdate = []


    """
    中央線沿い24駅をrange(0,24)で回す
    iはstationリスト
    jは閲覧ページのページ番目
    """
    for i in range(0,24):
        print(station[i])
        j=1
        #file_path = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_' + station[i] + str(j) + '.html '
        file_path = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_{}{}.html '.format(station[i],j)


        #ファイルが存在するときに実行。存在しないときはループ抜けでi+1番目から再スタート
        while(os.path.isfile(file_path)):
            with open(file_path,'r',encoding='cp932') as f:
                response=f.read()

                scrape(response, listdate, station, i)


            #file_path = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_' + station[i] + str(j) + '.html '
            file_path = '/home/bpd-staff/work/DaisukeShiga/html_file/craw_{}{}.html '.format(station[i],j)
            print(station[i]+str(j))
            j+=1


    save_csv(listdate)


main()

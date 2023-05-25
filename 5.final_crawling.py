# 5. 생성된 검색어 리스트를 통해, 구글에 검색하여 2차 크롤링하는 코드 
 
import pandas as pd 
from gnews import GNews
import re
from datetime import date
import os

def make_folder(disaster,keyword):    
    new_folder = '재난유형_KEYWORD/{}/{}'.format(disaster,keyword)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")


if __name__=='__main__':
    disaster = '해양선박사고'
    file_name = '2023-05-18.csv'

    today = date.today()
    df = pd.read_csv('D:/WorkSpace/GNews/해양선박사고_csv_folder/사건리스트요약_검색/해양선박사고/keyword_list/{}/{}'.format(disaster,file_name), encoding='utf-8')

    for k in range(len(df)) :
        
        content_list = []
        publisher_list = []
        description_list = []
        published_date_list = []
        title_list = []
        url_list = []
        
        df_new = pd.DataFrame()
        df_new.reset_index(drop=True, inplace=True)

        keyword = df['keyword'][k]   
        keyword = keyword.replace('"','')
    
        google_news = GNews()
        json_resp = google_news.get_news(keyword)

        try :
            for i in range(len(json_resp)):
                    
                title = json_resp[i]['title']
                published_date = json_resp[i]['published date']
                description = json_resp[i]['description']
                url = json_resp[i]['url']
                
                try :                            
                    article = google_news.get_full_article(json_resp[i]['url']) 

                    title = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]+", " ", title)
                    print(title) 
                    print(keyword)
                    with open('재난유형_KEYWORD/{}/{}/{}.txt'.format(disaster,keyword, title), 'w', encoding = 'utf-8') as f :                     
                        f.write(article.text)
                        
                        content_list.append(article.text)
                        title_list.append(title)    
                        published_date_list.append(published_date)
                        description_list.append(description)
                        url_list.append(url)
                
                except :
                    continue    
        except :
            print("pass")       

            
        df_new['title'] = title_list
        df_new['published_date'] = published_date_list
        df_new['content'] =content_list   
        df_new['url'] = url_list 
        df_new['description'] = description_list

        make_folder(disaster,keyword)

        try : 
            df_new.to_csv('재난유형_KEYWORD/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8-sig', index=False)  

        except :
            df_new.to_csv('재난유형_KEYWORD/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8', index=False)     




            
            
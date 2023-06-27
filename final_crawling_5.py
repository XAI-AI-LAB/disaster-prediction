# 5. 생성된 검색어 리스트를 통해, 구글에 검색하여 2차 크롤링하는 코드 
 
import pandas as pd 
from gnews import GNews
import re
from datetime import date
import os
import traceback
import configparser


def make_folder(disaster,keyword):    
    new_folder = root_dir + '/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}/{}'.format(disaster, disaster, disaster, keyword)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")


def main():    
    google_news = GNews()

    disaster = '다중밀집시설붕괴'
    file_name = '{}_키워드리스트.csv'.format(disaster)

    today = date.today()
    df_ = pd.read_csv(root_dir + '/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}/{}'.format(disaster,disaster,disaster,file_name), encoding='utf-8')
    print(df_)

    for k in range(len(df_)) :  

        keyword = df_['keyword'][k]
        keyword = keyword.replace('"','')
        keyword = keyword.replace('-','')
        keyword = keyword.replace(':','')
        keyword = keyword.replace(';','')
        keyword = keyword.replace("'",'')
        keyword = keyword.replace(",",'')
        keyword = keyword.replace(".",'')
        keyword = keyword.replace("/",'')

        json_resp = google_news.get_news(keyword)

        df = pd.DataFrame()
        df.reset_index(drop=True, inplace=True)
        
        content_list = []
        description_list = []
        published_date_list = []
        title_list = []
        url_list = []

        make_folder(disaster,keyword)

        try :

            for i in range(len(json_resp)):
                    
                title = json_resp[i]['title']
                published_date = json_resp[i]['published date']
                description = json_resp[i]['description']
                url = json_resp[i]['url']
                
                try :    
                    article = google_news.get_full_article(json_resp[i]['url'])
                    title = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]+", " ", title)

                    with open(root_dir + '/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}/{}/{}.txt'.format(disaster,disaster,disaster,keyword,title), 'w', encoding = 'utf-8') as f : 
            
                        if article.text == None :
                            continue
                        
                        f.write(article.text)
                        
                        content_list.append(article.text)
                        title_list.append(title)    
                        published_date_list.append(published_date)
                        description_list.append(description)
                        url_list.append(url)
                        
                except :
                    continue  
        
            df['title'] = title_list
            df['published_date'] = published_date_list
            df['content'] =content_list   
            df['url'] = url_list 
            df['description'] = description_list


            try : 
                df.to_csv(root_dir + '/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}/{}/{}_{}.csv'.format(disaster, disaster, disaster, keyword, today, keyword), encoding='utf-8-sig', index=False)  

            except Exception :
                err = traceback.format_exc(limit=4)
                print(err)
                continue  
            
        except Exception :
            err = traceback.format_exc(limit=4)
            print(err)
            continue
        
        
if __name__ == '__main__':
    properties = configparser.ConfigParser() # 클래스 객체 생성
    properties.read('config.ini', encoding='utf-8') # 파일 읽기
    root_dir = properties.get('PATH', 'ROOT_DIR')
    main()
    
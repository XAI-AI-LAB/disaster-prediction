# 1.도로교통사고 키워드를 이용하여 구글 뉴스 기사 검색하여 엑셀 파일로 저장 
from gnews import GNews
import re
import pandas as pd 
import os
from datetime import date
import traceback
import configparser

def make_folder(disaster, keyword):
    new_folder = root_dir + '/재난유형/{}/{}'.format(disaster, keyword)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")
    
   
def main():
    # today  = date.today()
    google_news = GNews()

    disaster = '공사장사고' 
    keyword_list = ['공사장 사고', '공사장 추락'] 
        
    for k in range(len(keyword_list)) :
        keyword = keyword_list[k] 
        json_resp = google_news.get_news(keyword)

        df = pd.DataFrame()
        df.reset_index(drop=True, inplace=True)

        content_list = []
        description_list = []
        published_date_list = []
        title_list = []
        url_list = []

        make_folder(disaster, keyword)

        try :
            for i in range(len(json_resp)):
                    
                title = json_resp[i]['title']
                published_date = json_resp[i]['published date']
                description = json_resp[i]['description']
                url = json_resp[i]['url']
                
                try : 
                    article = google_news.get_full_article(json_resp[i]['url'])
                    title = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]+", " ", title)
                    with open( root_dir['ROOT_DIR'] + '/재난유형/{}/{}/{}.txt'.format(disaster, keyword, title), 'w', encoding = 'utf-8') as f : 
                
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

        except Exception :
            err = traceback.format_exc(limit=4)
            print(err)
            continue

        df['title'] = title_list
        df['published_date'] = published_date_list
        df['content'] =content_list   
        df['url'] = url_list 
        df['description'] = description_list

        try : 
            df.to_csv(root_dir + '/재난유형/{}/{}/{}.csv'.format(disaster, keyword, keyword), encoding='utf-8-sig', index=False)  

        except :
            df.to_csv(root_dir + '/재난유형/{}/{}/{}.csv'.format(disaster, keyword, keyword), encoding='utf-8', index=False)     


if __name__ == '__main__':
    properties = configparser.ConfigParser() # 클래스 객체 생성
    properties.read('config.ini', encoding='utf-8') # 파일 읽기
    root_dir = properties.get('PATH','ROOT_DIR')
    main()
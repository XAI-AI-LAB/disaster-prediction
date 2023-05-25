# 1-2.재난 유형 키워드를 입력받아 구글 뉴스 크롤링 (1.keyword.py와 결과 같음)

from gnews import GNews
import re
import pandas as pd 
import os
from datetime import date

def make_folder(disaster,keyword):    
    new_folder = '재난유형/{}/{}'.format(disaster,keyword)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")


if __name__ == '__main__':
    disaster = input("재난유형을 적어주세요.(ex.공사장사고) : ")
    input_string = input("띄워쓰기 단위로 재난 유형의 키워드를 적어 주세요.(ex.공사장 사고) :")    
    
    keyword_list_1 = input_string.split()
    keyword_list_2 = ['사고','사건','사고사례']
    
    today = date.today()
    google_news = GNews()

    for k in range(len(keyword_list_1)) :
        for q in range(len(keyword_list_2)) :

            keyword = keyword_list_1[k] + keyword_list_2[q]
            json_resp = google_news.get_news(keyword)

            df = pd.DataFrame()
            df.reset_index(drop=True, inplace=True)

            content_list = []
            publisher_list = []
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
                        print(title) 
                        print(keyword)
                        with open('재난유형/{}/{}/{}.txt'.format(disaster,keyword, title), 'w', encoding = 'utf-8') as f : 
                        
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
            except :
                print("pass")       

        
    df['title'] = title_list
    df['published_date'] = published_date_list
    df['content'] =content_list   
    df['url'] = url_list 
    df['description'] = description_list


    try : 
        df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8-sig', index=False)  

    except :
        df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8', index=False)     

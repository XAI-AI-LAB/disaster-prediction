# 1.도로교통사고 키워드를 이용하여 구글 뉴스 기사 검색하여 엑셀 파일로 저장 

from gnews import GNews
import re
import pandas as pd 
import os
from datetime import date

today  = date.today()

google_news = GNews()

disaster = '철도교통사고'

keyword_list_1 = ['충돌', '전복', '추돌', '추락', '화재', '폭발', '엔진', '고장', '이탈', '노후', '신호', '정비', '결함', '구조', '수색', '승객', '정지신호', '안전요원'] 
keyword_list_2 = ['열차', '레일', '선로', '궤도', '고속열차', '전환기', 'KTX', 'SRT', '전복', '탈선', '이탈', '기관사', '승강장', '교체공사', '승무원']

    
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


        new_folder = '재난유형/{}/{}'.format(disaster, keyword)

        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            print("폴더 생성 완료")
        else :
            print("폴더가 이미 존재합니다.")


        try :

            for i in range(len(json_resp)):
                    
                title = json_resp[i]['title']
                published_date = json_resp[i]['published date']
                description = json_resp[i]['description']
                url = json_resp[i]['url']
                
                try :
                        
                    article = google_news.get_full_article(json_resp[i]['url'])

                    title = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]+", " ", title)

                    with open('재난유형/{}/{}/{}.txt'.format(disaster, keyword, title), 'w', encoding = 'utf-8') as f : 
                
                        
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
    df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster, today, keyword), encoding='utf-8-sig', index=False)  

except :
    df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster, today, keyword), encoding='utf-8', index=False)     

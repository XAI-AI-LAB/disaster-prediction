# 4. chat gpt api 이용해서 나온 결과로 재수집 한 결과 재 검색하는 코드 사건 리스트 출력하기 위한 코드  

from gnews import GNews
import pandas as pd 
import re
import time
import os 
import glob
from datetime import date
import openai
from openai.error import RateLimitError


def make_folder(disaster, keyword) :    
    new_folder = '재난유형/{}/{}'.format(disaster, keyword)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")


def make_folder_2(disaster) :    
    new_folder = 'keyword_list/{}'.format(disaster)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")


def remove_special_chars(s):
    return ''.join(c for c in s if c.isalnum() or c.isspace())
    

if __name__ == "__main__" :
    
    openai.api_key ="sk-Z" 

    disaster = '화재'
    today = date.today()

    path = 'D:/WorkSpace/GNews/{}_csv_folder/사건리스트요약_검색/{}'.format(disaster,disaster) 
     
    extension = 'csv'
    os.chdir(path)
    files = glob.glob('*.{}'.format(extension))
    
    
    df = pd.DataFrame()
    keyword_list = []
    
    
    for k in range(len(files)):        
        google_news = GNews()

        df_list = pd.read_csv(path+'/'+files[k], encoding='utf-8')
        # chat gpt 내용으로 넣기 
        for j in range(len(df_list)):
            fileContents = df_list['article_list'][j]
            print(fileContents)
            
            time.sleep(20) # openai api 호출시간 오류로 인한 시간 텀 조정하기 
            
            for _ in range(5) :
                try :
                      
                    completion = openai.ChatCompletion.create(
                        model = "gpt-3.5-turbo",
                        messages = [
                            { "role": "system", "content": "당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신은 질문에 알맞는 대답을 정확하게 합니다." },
                            { "role": "user", "content": "당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신은 질문에 알맞는 대답을 정확하게 합니다." },
                            { "role": "assistant", "content": "'안녕하세요, 제게 물어보시면 질문에 맞는 결과를 출력해 드리도록 하겠습니다." },
                            { "role": "user", "content": fileContents},
                            { "role": "user", "content": "위 사건을 검색할 수 있는 키워드 하나만 알려줘" }
                        ]
                    )
                    break # If successful, break the loop 
                except RateLimitError :
                    print("Rate limit exceeded. Waiting for 60 seconds before retrying")
                    time.sleep(60)        
            
            print("============검색할 수 있는 키워드 =================")
            print(completion.choices[0].message.content)
            keyword = completion.choices[0].message.content
            
            remove_special_chars(keyword)
            print(remove_special_chars(keyword))
                             
            keyword_list.append(keyword)
            
    df['keyword'] = keyword_list
    
    
    make_folder_2(disaster)    
    df.to_csv('keyword_list/{}/{}.csv'.format(disaster,today), encoding='utf-8-sig', index=False)  

    
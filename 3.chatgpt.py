# NER 을 이용하여 추출된 엑셀파일 피해정보에서 피해 정보가 존재하는 파일만 추출하여 chat gpt 를 이용하여 내용 추출하는 코드 작성 
# 1) GNEWS 의 1.keyword.py  2) ner의 inference.py 3) Gnews - 3.chatgpt.py 
# NER 의 inference.py 에서 생성된 '재난유형_csv_folder' 속의 파일을 옮겨 가지고 온후, chatgpt.py 실행

import os 
import openai
import pandas as pd  
import glob

def make_folder(disaster):    
    new_folder = '사건리스트요약_검색/{}'.format(disaster)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("폴더 생성 완료")
    else :
        print("폴더가 이미 존재합니다.")



if __name__ == '__main__':
    
    global disaster
    disaster = '유해화학물질사고'

    path = '{}_csv_folder'.format(disaster) 
    
    extension = 'csv'
    os.chdir(path)
    files = glob.glob('*.{}'.format(extension))

    # 공연장안전사고_csv_folder 내부의 모든 csv 파일을 저장 
    for csv_file in files:
        # print(csv_file)
        try :
            openai.api_key ="sk-" 

            index_list = []
            content_list = []

            df_new = pd.DataFrame()
                    
            df = pd.read_csv("{}".format(csv_file),encoding='utf-8')
            # print(df)
            
            for i in range(len(df)) :
                try :
                    
                    if df['ner'][i] != '[]' :
                        
                        fileContents = df['file_content'].tolist()[i]
                        completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[         
                            { "role": "system", "content": "당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신은 질문에 알맞는 대답을 정확하게 합니다." },
                            { "role": "user", "content": "당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신은 질문에 알맞는 대답을 정확하게 합니다." },
                            { "role": "assistant", "content": "'안녕하세요, 제게 물어보시면 질문에 맞는 결과를 출력해 드리도록 하겠습니다." },
                            { "role": "user", "content": fileContents},
                            { "role": "user", "content": "위 사건에 관해 장소와 날짜와 재난유형 이렇게 키워드 3개만 딱 짧고 간결하게 띄워쓰기로 말해줘" }
                        ]
                        )

                        print(completion.choices[0].message.content)
    #                     # 날짜, 장소, 사고 내용 : 으로 요약한 부분
                        summarized_content = completion.choices[0].message.content                
                        content_list.append(summarized_content)

                except :
                    continue
                
                        
        except :
            continue
        
            
        df_new['article_list'] = content_list
        print(df_new)
        # print(df_new.shape)
        
        make_folder(disaster)
            
        try :     
            # df_new.to_csv('사건리스트요약_검색/{}/chatgpt정리_{}'.format(disaster,csv_file), encoding='euc-kr', index=False)  
            df_new.to_csv('사건리스트요약_검색/{}/chatgpt정리_{}'.format(disaster,csv_file), encoding='utf-8-sig', index=False)  

        except :
            # df_new.to_csv('사건리스트요약_검색/{}/{}_chatgpt정리.csv'.format(disaster,disaster), encoding='utf-8', index=False)    
            df_new.to_csv('사건리스트요약_검색/{}/chatgpt정리_{}'.format(disaster,csv_file), encoding='utf-8', index=False)    

## 유사도 분석에서 tensor 값이 0.6 이상인 텍스트 유사도 값만 csv 파일로 다시 저장하는 코드  

import configparser
import glob
import pandas as pd 
import re 

def main():
    disaster = '공연장안전사고'
    # 1.유사도 분석 파일을 df_csv 로 열기
    csv_folder_path = root_dir +'/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/'.format(disaster,disaster)
    csv_files = glob.glob(csv_folder_path+'*.csv')

    for file in csv_files:
        df_csv = pd.read_csv(file)
        print(df_csv)
        print(f"{file}===========================================")

    # 2. 유사도 분석 df['score'] 값의 형태를 숫자로 변형시키기 
        print(df_csv['score'])
        
        content_list = []
        score_list = []
        queries_list = []
        
        for p in range(len(df_csv)):
            
            tensor_value = df_csv['score'][p]
            number = float(re.findall('\d+\.\d+', tensor_value)[0])
            # print(number)
                                                                                                                            
            if number >= 0.6 :
                print(df_csv['summarized_article_content'][p])
                print(number)
                
    # 3. 0.6 이상인 contents 만 새로운 폴더 csv 파일에 저장하기
                content_list.append(df_csv['summarized_article_content'][p])
                queries_list.append(df_csv['queries'][p])
                score_list.append(number)
                    
            high_score_df = pd.DataFrame(columns=['summarized_article_content','queries','score'])
                        
            high_score_df['summarized_article_content'] = content_list
            high_score_df['queries'] = queries_list 
            high_score_df['score'] = score_list
 
            high_score_df.to_csv(root_dir + '/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/high_score_file/{}.csv'.format(disaster,disaster,file.split('\\')[-1].split('.csv')[0]), mode='w', encoding='utf-8-sig', index=False)                          
                                

if __name__ == '__main__':
    properties = configparser.ConfigParser()
    properties.read('config.ini')
    root_dir = properties.get('PATH', 'ROOT_DIR')
    main()
     
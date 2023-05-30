"""
# 파일명 : _01_keyword_2_modi.py
# 설명   : 1-2.재난 유형 키워드를 입력받아 구글 뉴스 크롤링 (1.keyword.py와 결과 같음)
# 개정이력 :
#    버젼    수정일자                   수정자              내용
#    1.0    2023-05-25                  성유기            신규 작성
#    1.0.1  2023-05-25                  김종완            수     정
"""

import os
import re
import argparse
import traceback
import pandas as pd 
from gnews import GNews
from datetime import date

#logging setting
from common import Logging_config
logging_instance = Logging_config()
logger = logging_instance.logging_setting()

# common
from common import make_folder
from common import createFolder
from common import DefineValues


"""
# 함수명   : parse_args
# 설명     : input parameter 
# return   : args
# 특이사항 : 
"""
def parse_args():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
    --saster : "재난유형을 적어주세요.(ex.공사장사고) : ",
    --input_string : "띄워쓰기 단위로 재난 유형의 키워드를 적어 주세요.(ex.공사장 사고) :"
    """
    )
    parser.add_argument("--disaster",      required=True, type=str, default=None, help="재난유형")
    parser.add_argument("--input_string",required=True, type=str, default=None, help="재난 유형의 키워드(띄어쓰기 단위)")

    args = parser.parse_args()

    return args


"""
# 함수명   : main
# 설명     : 
# return   : 
# 특이사항 :
"""
def main():
    args = parse_args()
    disaster     = args.disaster     # 재난유형
    input_string = args.input_string # 재난 유형 키워드

    logger.info(f"args disaster     : {disaster}")
    logger.info(f"args input_string : {input_string}")

    keyword_list_1 = input_string.split()        # 입력받은 재난 유형 키워드
    keyword_list_2 = DefineValues.KEYWORD_LIST   # ['사고','사건','사고사례']

    today = date.today()
    google_news = GNews()

    for k in range(len(keyword_list_1)) :     # 입력받은 재난유형
        for q in range(len(keyword_list_2)) : # 정의 해놓은 ['사고','사건','사고사례']
            keyword   = keyword_list_1[k] + keyword_list_2[q]
            json_resp = google_news.get_news(keyword)         # keyword google news 검색 response

            df = pd.DataFrame()
            df.reset_index(drop=True, inplace=True)

            content_list        = []
            publisher_list      = []
            description_list    = []
            published_date_list = []
            title_list          = []
            url_list            = []

            print("create folder")
            make_folder(disaster,keyword)

            try :
                for new_search_response in json_resp : 
                    article = google_news.get_full_article(new_search_response["url"])
                    title   = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]+", " ", new_search_response["title"])
                    logger.info(f"title   : {title}")   
                    logger.info(f"keyword : {keyword}")
                    

                    text_dir = f"./{DefineValues.MAIN_DIR}/{disaster}/{keyword}/{title}.txt"
                    createFolder(text_dir)
                    with open(text_dir,'w', encoding = 'utf-8') as f :
                        try : 
                            f.write(article.text)
                        except :
                            err = traceback.format_exc(limit=4)
                            logger.error(err)
                            continue

                        logger.info(f"write txt : {text_dir}")

                        content_list.append(article.text)
                        title_list.append(title)    
                        published_date_list.append(new_search_response["published date"])
                        description_list.append(new_search_response["description"])
                        url_list.append(new_search_response["url"])

            except Exception :
                err = traceback.format_exc(limit=4)
                logger.error(err)
                continue

    df['title']          = title_list
    df['published_date'] = published_date_list
    df['content']        = content_list   
    df['url']            = url_list 
    df['description']    = description_list

    try : 
        df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8-sig', index=False)  

    except :
        df.to_csv('before_encoding_csv/{}/{}_{}.csv'.format(disaster,today,keyword), encoding='utf-8', index=False)     

    return



if __name__ == '__main__':
    main()
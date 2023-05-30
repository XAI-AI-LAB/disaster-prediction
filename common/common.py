"""
# 파일명 : common.py
# 설명   : 공통함수
# 개정이력 :
#    버젼    수정일자                   수정자              내용
#    1.0    2023-05-25                  김종완            신규 작성
"""
import os
import pathlib



"""
# Class : DefineValues
# 설명  : 상수 정의
"""
class DefineValues :
    MAIN_DIR     = "disaster_type"
    KEYWORD_LIST = ['사고','사건','사고사례']



"""
# 함수명   : createFolder
# 설명    : 디렉터리가 없으면 디렉터리를 생성한다.
# return  : None
# 특이사항 :
"""
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            path = pathlib.Path(directory)
            if len(path.suffix) == 0 :
                os.makedirs(directory)
            else : 
                os.makedirs(os.path.dirname(directory))
            # logger.warning("Directory was created because directory dose not exist %s", os.path.abspath(directory))
            print("Directory was created because directory dose not exist %s", os.path.abspath(directory))
    except OSError:
        return
    


"""
# 함수명   : make_folder
# 설명     : 
# return   : 
# 특이사항 :
"""
def make_folder(disaster,keyword):    
    new_folder = f'./{DefineValues.MAIN_DIR}/{disaster}/{keyword}'
    createFolder(new_folder)

    return None
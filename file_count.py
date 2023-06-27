# 파일 갯수 파악하는 코드 
import os 
import pandas as pd 
import configparser

def count_event():
    files = os.listdir(folder_path)
    num_files = len(files)
    print("폴더 안에 있는 사건 폴더의 갯수: ", num_files)
    return num_files


def print_dir():    
    for root, dirs, files in os.walk(folder_path):  
        # print(dirs) # 사건 리스트로 출력 
        return dirs
    
    
def count_files():
    count = 0
    event_list = []
    count_list = []
    
    df = pd.DataFrame()
    df.reset_index(drop=True, inplace=True)
    
    for event_name in os.listdir(folder_path):
        path = folder_path + "/" + event_name
        try :
            count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            print(f"{event_name}, 폴더 내 파일 갯수: {count}")
            print(f"{event_name}, 폴더 내 text 갯수: {count-1}")
        except NotADirectoryError :
            continue
        
        event_list.append(event_name)
        count_list.append(count-1)

        
    df['folder_path'] = event_list
    df['txt_count'] = count_list
    count_total = sum(count_list)
    print(count_total)
 
    
    
    try : 
        df.to_csv('{}_갯수.csv'.format(disaster), encoding='utf-8-sig', index=False)  
        print("저장됨")
    except :
        print("저장안됨")
        
    return event_name, count-1 , count_total

    
if __name__ == "__main__":
    
    disaster_list = ['공사장사고', '공연장안전사고','다중밀집시설붕괴','도로교통사고','등산레저사고','물놀이사고','산불','유해화학물질사고','철도교통사고','항공기사고','해양선박사고','화재']
    
    for disaster in disaster_list :
        
        properties = configparser.ConfigParser()
        properties.read('config.ini', encoding='utf-8') 
        root_dir = properties.get('PATH','ROOT_DIR')
        
        folder_path = root_dir + '\{}_csv_folder\사건리스트요약_검색\{}\keyword_list\{}'.format(disaster,disaster,disaster)
        
        num_files = count_event()  
        
        dirs = print_dir()
        print(f'{disaster}의 사건의 총 갯수 : ', len(dirs))
            
        event_name, countt, count_total = count_files()

        print(f'{disaster}의 총 .txt 갯수 : ', count_total)
        print("count 완료")
        
        with open('{}_total_textfile_count.txt'.format(disaster), 'w') as f :
            f.write(str(count_total))




            
   
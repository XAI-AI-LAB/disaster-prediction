import os
import glob
import torch
import numpy as np
import onnxruntime as ort
from pathlib import Path
from transformers.convert_graph_to_onnx import convert
from transformers import PreTrainedTokenizerFast
from sentence_transformers import SentenceTransformer, util
import pandas as pd 
from datetime import date
# 시간 출력하는  datetime 알려줘

def mean_pooling(embeddings: np.ndarray, attention_mask: np.ndarray):

    input_mask_expanded = attention_mask[..., np.newaxis].astype(np.float32)
    sum_embeddings = np.sum(embeddings * input_mask_expanded, axis=1)
    sum_mask = input_mask_expanded.sum(axis=1)
    sum_mask = np.clip(sum_mask, a_min=1e-9, a_max=None)

    return sum_embeddings / sum_mask


if __name__ == "__main__":
    
    today = date.today()
    
    # models 폴더에 존재하는 파일 삭제하고 시작
    file_path = 'models/ko-sroberta-multitask.onnx'
    os.remove(file_path)
    
    # export to onnx
    output_dir = "models"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=False)
 
    output_fpath = os.path.join(output_dir, "ko-sroberta-multitask.onnx")
    convert(framework="pt", model="jhgan/ko-sroberta-multitask", output=Path(output_fpath), opset=12)

    # test run
    tokenizer = PreTrainedTokenizerFast.from_pretrained("jhgan/ko-sroberta-multitask")
    session = ort.InferenceSession(output_fpath)


    disaster = '공연장안전사고' # 공연장 안전사고 
    # 파일이 들어있는 폴더 경로
    folder_path = "D:/WorkSpace/ko-sentence-transformers/onnx/{}/".format(disaster)

    # 해당 폴더 내부에 있는 파일 리스트를 가져옵니다.
    folders = os.listdir(folder_path) # 폴더명이 나타남 
    
    # 폴더 내부에 있는 모든 파일 경로를 가져옵니다.
    folder_paths = [os.path.join(folder_path, folder) for folder in folders]  #  위의 폴더 명 까지의 경로가 나타남 
    # print(":================================================")
    # print(folder_paths)
    # print(len(folder_paths))  # 파일의 폴더 명 # 621
    # print(folder_paths[1])
    

    df = pd.read_csv('D:/WorkSpace/ko-sentence-transformers/onnx/{}/{}_키워드리스트_230614.csv'.format(disaster, disaster))
    print(df)
    for i in range(len(df)): 
        
        queries = df['summarized_article_content'][i]
        
        for j in range(len(df)):
            
            if df['keyword'][j] in folders :
                queries = df['summarized_article_content'][j]  # 기준이 되는 내용
                print("============================================queries 출력=====")
                print(queries)
                print("==============================================================")
                # 폴더명과 같은 내용의 폴더 속에 있는 모든 파일을 가져오기 
                files = glob.glob("D:/WorkSpace/ko-sentence-transformers/onnx/{}/".format(disaster)+df['keyword'][j]+"/"+'*.txt')  
            
        
        
        
            
                df_new = pd.DataFrame(columns=['summarized_article_content', 'queries','score'])
                # df_new = df_new.append({'summarized_article_content': file_contents, 'queries':queries, 'score': (corpus[idx].strip(), "%.4f" % (cosine[idx]))}, ignore_index=True)
                
        
        
        
        
        
        
                # files 속의 파일 내용 읽어서 각각 queries 와 비교하기  
                for k in range(len(files)):
                    with open(files[k], 'r', encoding='utf-8') as f :
                        file_contents = f.read()
                        
                        print("================================================================corpus 출력===== ====")
                        print(file_contents)
                        print("=================================================================================")
                        
                        corpus = file_contents
                                    
                        tokenized_corpus = tokenizer(corpus, return_tensors="pt", padding=True, truncation=True)
                        corpus_onnx = {k: v.cpu().detach().numpy() for k, v in tokenized_corpus.items()}

                        tokenized_queries = tokenizer(queries, return_tensors="pt", padding=True, truncation=True)
                        queries_onnx = {k: v.cpu().detach().numpy() for k, v in tokenized_queries.items()}

                        # run inference
                        corpus_embeddings, pooled_corpus = session.run(None, corpus_onnx)
                        corpus_embeddings = mean_pooling(corpus_embeddings, corpus_onnx["attention_mask"])

                        query_embeddings, pooled_queries = session.run(None, queries_onnx)
                        query_embeddings = mean_pooling(query_embeddings, queries_onnx["attention_mask"])

                        cos_scores = util.pytorch_cos_sim(query_embeddings, corpus_embeddings).cpu()

                        top_k = 1
                        
                        
    
                        for query, cosine in zip(queries, cos_scores):
                            print(query)
                            print(cosine)
                            top_results = np.argpartition(-cosine, range(top_k))[:top_k]
                            print(top_results)
                            print("-----현재 score 출력------")            
                            print("Query:", query)
                            
                            try : 
                                
                                for idx in top_results:
                                    
                                    print(top_results[idx])
                                    print(idx)  
                                    print(corpus[idx].strip(), "(Score: %.4f)" % (cosine[idx]))
                                    print(corpus[idx].strip(), "%.4f" % (cosine[idx])) # score value
                            except :
                                pass             
                            print("\n")
                        
                        
                        print("===========idx 오류================")
                        print(cosine)
                        
                        
                        # 새로운 데이터 프레임을 만들어 score 를 저장한다. 
                        df_new = df_new.append({'summarized_article_content': file_contents, 'queries':queries, 'score': (cosine)}, ignore_index=True)
                        df_new['summarized_article_content'][k] = file_contents   
                        df_new['queries'][k] = queries
                        # df_new['score'][k] = corpus[idx].strip(), "%.4f" % (cosine[idx])
                        df_new['score'][k] = cosine
                    
                    
                        try :
                            # 파일명에 j 대신에 keyword; df['keyword'][j]  로 넣기 
                            # 다음 파일 실행 부터 
                            
                            # df_new.to_csv('D:/WorkSpace/GNews/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}_{}_유사도SCORE.csv'.format(disaster,disaster,today,j), encoding='utf-8-sig', index=False)  
                            df_new.to_csv('D:/WorkSpace/GNews/{}_csv_folder/사건리스트요약_검색/{}/keyword_list/{}_{}_유사도SCORE.csv'.format(disaster,disaster,today,df['keyword'][j]), encoding='utf-8-sig', index=False)  
                        
                        except :
                            pass

                        
                        
                        
                        
                
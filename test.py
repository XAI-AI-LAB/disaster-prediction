# 4/11 이전 발생한 사건 모두 지우는 코드 
# 
import pandas as pd

df = pd.read_csv("LG 디스플레이 파주공장 화학물질 유출\LG 디스플레이 파주공장 화학물질 유출.csv")
print(df)
print(df.shape)
print(df.columns)


# # Index(['title', 'published_date', 'content', 'url', 'description'], dtype='object')


# 날짜 23-04-11을 datetime 형식으로 변환
df['published_date'] = pd.to_datetime(df['published_date'], format='%a, %d %b %Y %H:%M:%S %Z').dt.strftime('%Y-%m-%d, %H:%M')
df['published_date'] = pd.to_datetime(df['published_date'])

print("------날짜 확인하기----")
print(df['published_date'])


date_threshold = pd.to_datetime('2000-01-01')

# 필터링하여 새로운 데이터프레임 생성
new_df = df[df['published_date'] >= date_threshold]
new_df = df[df['published_date'] >= date_threshold]

print(new_df)

# csv 로 저장 
new_df.to_csv('LG 디스플레이 파주공장 화학물질 유출_시간단위변환.csv', index=False, encoding='utf-8-sig')

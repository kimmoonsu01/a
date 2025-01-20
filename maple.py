import pandas as pd
import requests
from google.colab import userdata

# API 키 가져오기
  
x_nxopen_api_key = userdata.get("x-nxopen-api-key")
headers = {
      'accept': 'application/json',
      'x-nxopen-api-key': f'{x_nxopen_api_key}'
  }

  # URL과 파리미터 설정
urlString = "https://open.api.nexon.com/maplestory/v1/"
params = 'history/starforce?count=100&date=2024-02-28'

  # API 요청 보내기
response = requests.get(urlString + params,headers=headers)
  # text로 변환
text = response.json()
text
  # # DataFrame 으로 변환
df = pd.DataFrame(text['starforce_history'])
success_fail_count = df.groupby(["before_starforce_count"])["item_upgrade_result"].value_counts().unstack(fill_value=0)


 # 실패 데이터가 없는 경우 기본값 추가
if "fail" not in success_fail_count.columns:
     success_fail_count["fail"] = 0

  # 성공 및 실패 확률 계산
success_fail_count["success_rate"] = (success_fail_count["성공"] / success_fail_count.sum(axis=1)) * 100
success_fail_count["success_rate"] = success_fail_count["success_rate"].round(2)
success_fail_count["fail_rate"] = 100 - success_fail_count["success_rate"]

  # 데이터 프레임 재구성
success_fail_count.reset_index(inplace=True)
success_fail_count.rename(columns={"before_starforce_count": "asd"}, inplace=True)
success = pd.DataFrame(success_fail_count)
success.rename(columns={"실패(유지)": "fail_"}, inplace=True)
success

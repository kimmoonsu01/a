import pandas as pd
import requests

# API 키 가져오기
x_nxopen_api_key = userdata.get("x-nxopen-api-key")
headers = {
    'accept': 'application/json',
    'x-nxopen-api-key': f'{x_nxopen_api_key}'
}

# URL과 파라미터 설정
urlString = "https://open.api.nexon.com/maplestory/v1/"

# 날짜 범위 설정
start_date = '2023-12-27'
end_date = '2025-01-17'

# 반복적으로 요청 보내기
all_data = []
current_date = pd.to_datetime(start_date)

while current_date <= pd.to_datetime(end_date):
    params = f'history/starforce?count=1000&date={current_date.strftime("%Y-%m-%d")}'
    response = requests.get(urlString + params, headers=headers)

    # 응답이 성공적인지 확인
    if response.status_code == 200:
        text = response.json()
        all_data.extend(text['starforce_history'])

    # 날짜를 하루씩 증가
    current_date += pd.Timedelta(days=1)

# DataFrame 으로 변환
df = pd.DataFrame(all_data)

# 실패 데이터를 추가하거나 기본값으로 실패 확률을 계산
success_fail_count = df.groupby(["before_starforce_count"])["item_upgrade_result"].value_counts().unstack(fill_value=0)

# 실패 데이터가 없는 경우 기본값 추가
if "실패" not in success_fail_count.columns:
    success_fail_count["실패"] = 0

# 성공 및 실패 확률 계산
success_fail_count["성공 확률 (%)"] = (success_fail_count["성공"] / success_fail_count.sum(axis=1)) * 100
success_fail_count["성공 확률 (%)"] = success_fail_count["성공 확률 (%)"].round(2)
success_fail_count["실패 확률 (%)"] = 100 - success_fail_count["성공 확률 (%)"]

# before_starforce_count를 '강화 단계'로 이름 변경
success_fail_count.rename_axis('강화 단계', axis='index', inplace=True)

# item_upgrade_result 컬럼을 '강화'로 이름 변경
success_fail_count.columns.name = '강화'

# 결과 확인
success_fail_count

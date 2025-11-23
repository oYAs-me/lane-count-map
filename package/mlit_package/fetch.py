# -*- coding: utf-8 -*-
# https://www.mlit-data.jp/api_docs/sources/rtc_yoy_diff.html からコピーし加筆

# APIをコールするソースをインポート
from package.mlit_package import api_caller, make_query
# 非同期処理を行うライブラリをインポート
import asyncio

# 交通調査基本区間番号のキーを定義
TRAFFIC_SECTION_NUM_KEY = "RTC:koutsuu_chousa_kihon_kukan_bangou"
# 抽出する必要があるキーのリストを定義
NEEDED_KEYS: list = [
  "DPF:year",  # 年度/年
  "DPF:last_update_datetime",  # 最新更新日
  "RTC:shasensuu",  # 車線数
  "RTC:fukuin_kousei_shadoubu_fukuin_m",  # 幅員構成 車道部幅員（ｍ）
  "RTC:fukuin_kousei_shadou_fukuin_m",  # 幅員構成 車道幅員（ｍ）
  "RTC:fukuin_kousei_chuuoutai_fukuinhaba_m",  # 幅員構成 中央帯幅員（ｍ）
  "RTC:koutsuu_anzen_shisetsunado_hodou_secchiritsu",  # 交通安全施設等 歩道設置率（％）
  "RTC:koutsuu_anzen_shisetsunado_ryougawa_hodou_secchiritsu",  # 交通安全施設等 両側歩道設置率（％）
  "RTC:koutsuu_anzen_shisetsunado_hodou_daihyou_fukuin_m",  # 交通安全施設等 歩道代表幅員（ｍ）
]

# extract_needed_dataの戻り値のインデックスを定義
INDEX = [TRAFFIC_SECTION_NUM_KEY] + NEEDED_KEYS

# fetchしてきたmetadataのうち、必要なデータのみを抽出する関数
def extract_needed_data(data: dict[str, str|int|float]) -> tuple[str|int|float, ...]:
  # まずは交通調査基本区間番号を取得し、タプルに格納
  extracted_data = (data[TRAFFIC_SECTION_NUM_KEY],)

  # 必要なデータのみを抽出し順次追加
  for name in NEEDED_KEYS:
    if name in data:
      extracted_data += (data[name],)

  # 交通調査基本区間番号と抽出したデータを返す
  return extracted_data


"""
作成した関数を使用してデータを取得する
-------------------------------------------------------------------------
make_search_queryを使用し、クエリ文を作成する
APIにリクエストを送信し、レスポンスを取得する
extract_needed_dataを使用し、必要なデータのみを抽出する
交通調査基本区間番号と抽出データのリストを返す
-------------------------------------------------------------------------
"""
def fetch_data(pref_name: str, page_first: int = 0, page_size: int = 30) -> set[tuple[str|int|float, ...]]:
  # データセットIDの定義: 令和3年度道路交通センサス
  DATASET_ID: str = 'rtc_2021'
    
  s_query = make_query.make_search_query(
      # dataset_id
      DATASET_ID,
      # pref_name
      pref_name=pref_name,
      # page_first
      page_first=page_first,
      # page_size
      page_size=page_size,
    )
  
  # 出力する変数の宣言
  status_code, reason = None, None
  extracted_data_set: set[tuple[str|int|float, ...]] = set()
  try:
    # APIにリクエストを送信し、レスポンスが返るまで待機する
    s_response, status_code, reason = asyncio.run(api_caller.post_query(s_query, 'search'))
    print(f"API request (status: {status_code}, reason: {reason}) {pref_name}: {page_first}-{page_first + page_size - 1}")

    # s_responseから必要なデータのみを抽出する
    for item in s_response["searchResults"]: # item = {id: str, title: str, year: str, metadata: {}, relatedData: []}
      data: dict = item["metadata"]
      # 先頭要素をtraffic_section_numに、残りをextracted_dataとして展開
      extracted_data = extract_needed_data(data) # item["metadata"]から必要なデータを抽出
      extracted_data_set.add(extracted_data)
    
  except Exception as e: # エラーが発生した場合
    raise Exception(f"error occurred. Stopping fetch loop. (status: {status_code}, reason: {reason})") from e
  
  # 抽出したデータを返す
  return extracted_data_set

# -*- coding: utf-8 -*-
# https://www.mlit-data.jp/api_docs/sources/rtc_yoy_diff.html からコピーし加筆

# 検索APIのクエリ文を作成する
# page_first: 全検索結果から何件目からのデータを取得するか
# page_size: 一度に取得する検索結果の件数
# pref_name: 都道府県名
# dataset_id: データセットのID
def make_search_query(dataset_id: str, pref_name: str = "東京都", page_first: int = 0, page_size: int = 10) -> str:
  query = f"""
  query {{
   search(
    first: {page_first},
    size: {page_size},
    attributeFilter: {{
     AND: [
      {{ attributeName: "DPF:catalog_id", is: "rtc" }},
      {{ attributeName: "DPF:dataset_id", is: "{dataset_id}" }},
      {{ attributeName: "DPF:prefecture_name", is: "{pref_name}" }}
     ]
    }}
   ) {{
    totalNumber
    searchResults {{
     id
     title
     year
     metadata
     relatedData {{
      id
      title
      dataset_id
     }}
    }}
   }}
  }}
  """
  return query

# データ取得検索APIのクエリ文を作成する
# data_set_id: データセットのID
# data_id: データのID
def make_data_query(data_set_id: str, data_id: str) -> str:
  query = f"""
  query {{
   data(
    dataSetID: "{data_set_id}",
    dataID: "{data_id}"
   ) {{
    totalNumber
    getDataResults {{
     id
     title
     year
     metadata
    }}
   }}
  }}
  """
  return query
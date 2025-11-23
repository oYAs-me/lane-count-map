# -*- coding: utf-8 -*-
# https://www.mlit-data.jp/api_docs/sources/rtc_yoy_diff.html からコピー

# 通信に必要なライブラリのインポート
import requests

# エンドポイントとAPIキーを定義しておく
from package.mlit_package import _api_key as api_key # _api_key.pyからAPIキーをインポート

END_POINT: str = 'https://www.mlit-data.jp/api/v1/'
API_KEY: str = api_key.API_KEY

# 実際にクエリをポストする
# queryStr: クエリ内容
# queryName: クエリ名
async def post_query(queryContents: str, queryName: str) -> tuple[dict, int, str]:
  # HTTPクエリー内容を作成
  request = {
    "url": END_POINT,
    "method": "post",
    "headers": {
      "Content-type": "application/json",
      "apikey": API_KEY
    },
    "data": {"query": queryContents}
  }

  # APIを呼び出して結果を準備する
  response = None
  try:
    response = requests.post(request["url"], headers=request["headers"], json=request["data"])
    response.raise_for_status() # HTTPエラーが発生した場合は例外を発生させる
    result: dict = response.json()["data"][queryName]
  except requests.exceptions.RequestException as error:
    print(f"Error data: {error}")
    result: dict = {}

  # response が未割り当ての場合に備えて安全な値を返す
  status_code = response.status_code if response is not None else -1
  reason = response.reason if response is not None else "Request Failed"
  return (result, status_code, reason)
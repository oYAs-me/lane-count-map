# -*- coding: utf-8 -*-

from package.mlit_package import fetch
from package import prefcode
import time, csv, os

# ある県のデータをすべて取得し、データを保存する関数
def fetch_all_data_prefecture(pref_name: str) -> None:
  # データを格納するリスト
  data: set[tuple[str|int|float, ...]] = set()

  page_first = 0
  page_size = 50
  data_len = 0

  # データをすべて取得するまでループ
  while True:
    # データを取得
    try:
      data.update(fetch.fetch_data(pref_name=pref_name, page_first=page_first, page_size=page_size))
      
      time.sleep(1) # 1秒待機（APIサーバーへの負荷軽減のため）
      page_first += page_size # 次のページへ
      
      # なぜかわからんがどこからかデータ数が伸びなくなるので、その場合は終了する（網羅できてるっぽい）
      if data_len == len(data):
        break
      else:
        data_len = len(data)
    except:
      break
  
  # 都道府県コードを取得
  pref_code = prefcode.get_prefcode(pref_name)
  if pref_code is None:
    raise ValueError(f"Invalid prefecture name: {pref_name}")
  
  # data/mlitディレクトリが存在しない場合、作成する
  save_dir = f"data/mlit/{pref_code}"
  os.makedirs(save_dir, exist_ok=True)

  # 取得したデータをCSVファイルとして保存する
  csv_file_path = os.path.join(save_dir, f"data_{pref_code}.csv")
  with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    # ヘッダー行を書き込む
    csv_writer.writerow(fetch.INDEX) # fetch.INDEXにヘッダー名が格納されている
    # データ行を書き込む
    for row in data:
      csv_writer.writerow(row)

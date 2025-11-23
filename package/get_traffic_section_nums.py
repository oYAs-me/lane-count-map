# -*- coding: utf-8 -*-

from package import prefcode
import os

# ある県の交通セクション番号一覧を取得する関数
def get_traffic_section_nums_of_prefecture(pref_code: int) -> list[int]:
  # data/mlitディレクトリ内のCSVファイルパスを構築
  csv_file_path = f"data/mlit/{pref_code}/data_{pref_code}.csv"
  # CSVファイルが存在しない場合、エラーを発生させる
  if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
  
  # CSVファイルを読み込み、交通セクション番号を抽出する
  with open(csv_file_path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
    traffic_section_nums = [int(line.split(",")[0]) for line in lines[1:]] # ヘッダー行を除く
  
  return traffic_section_nums
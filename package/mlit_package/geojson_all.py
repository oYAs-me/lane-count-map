# -*- coding: utf-8 -*-

from package.mlit_package import get_geojson
from package import get_traffic_section_nums, prefcode
import asyncio, os, time

# 指定された都道府県名に存在するすべての交通セクション番号のGeoJSONデータを取得し保存する関数
def fetch_all_geojson_prefecture(pref_name: str, init: int = 0) -> None:
  # 都道府県コードを取得
  pref_code = prefcode.get_prefcode(pref_name)
  if pref_code is None:
    raise ValueError(f"Invalid prefecture name: {pref_name}")
  
  # 県名から交通セクション番号のリストを取得
  traffic_section_nums = get_traffic_section_nums.get_traffic_section_nums_of_prefecture(pref_code)
  
  # 保存先が存在しない場合、作成する
  save_dir = f"data/mlit/{pref_code}/geojson"
  os.makedirs(save_dir, exist_ok=True)

  # 進捗確認用変数
  total = len(traffic_section_nums)

  # すべての交通セクション番号に対してGeoJSONデータを取得し保存する
  for i in range(init, total):
    try:
      geojson = asyncio.run(get_geojson.get_geojson_of_traffic_section_num(traffic_section_nums[i], pref_code))
      get_geojson.save_geojson(geojson, pref_code, traffic_section_nums[i], dircheck=False)
    except Exception as e:
      print(f"Error fetching/saving GeoJSON for traffic section number {traffic_section_nums[i]}: {e}")
      continue
    print(f"Progress: {i}/{total} ({i/total:.2%})")
    time.sleep(0.2) # 0.2秒待機（MLITサーバーへの負荷軽減のため）
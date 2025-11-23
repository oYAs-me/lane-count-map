# -*- coding: utf-8 -*-

from package import prefcode
import requests, os, json
import asyncio

# 指定された交通セクション番号のGeoJSONデータを取得する関数
async def get_geojson_of_traffic_section_num(traffic_section_num: int, pref_code: int) -> dict:
  # GeoJSONデータの存在するURLを構築
  URL = f"https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/census/{pref_code}/{traffic_section_num}.geojson"

  # GeoJSONデータを取得
  response = requests.get(URL)
  print(f"Fetching GeoJSON for traffic section number {traffic_section_num}, Status code: {response.status_code}")
  response.raise_for_status() # エラーがあれば例外を発生させる
  geojson: dict = response.json()["features"][0]# Feature型GeoJSONに変形

  geojson["properties"] = {"traffic_section_num": traffic_section_num} # プロパティを上書きする

  return geojson 


# GeoJSONデータを保存する関数
def save_geojson(geojson: dict, pref_code: int, traffic_section_num: int, dircheck: bool) -> None:
  # data/mlit/geojsonディレクトリが存在しない場合、作成する
  save_dir = os.path.join("data", "mlit", str(pref_code), "geojson")
  if dircheck:
    os.makedirs(save_dir, exist_ok=True)

  # GeoJSONデータをファイルとして保存する
  file_path = os.path.join(save_dir, f"{traffic_section_num}.geojson")
  with open(file_path, mode="w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

# GeoJSONとは何かを確認したいとき
# https://zenn.dev/koheimsoka/articles/d33a1f2de006a2
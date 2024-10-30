import requests
import csv
import json
import logging
import argparse
import sys
import glob
import os

# ログの設定
logging.basicConfig(filename='datadog_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 引数チェック
parser = argparse.ArgumentParser(description="Datadog Monitor Import/Export Script")
parser.add_argument("action", choices=["export", "import"], help="Specify 'export' to export monitors or 'import' to import monitors.")
parser.add_argument("file", help="File path for the export CSV or import JSON pattern.")
args = parser.parse_args()

# 引数が存在しない場合、エラーメッセージを表示して終了
if not args.action or not args.file:
    print("need import or export")
    sys.exit(1)

# APIキーとアプリケーションキーを手動で入力
DATADOG_API_KEY = input("Please enter your Datadog API Key: ")
DATADOG_APP_KEY = input("Please enter your Datadog Application Key: ")

# ヘッダー情報
headers = {
    'Content-Type': 'application/json',
    'DD-API-KEY': DATADOG_API_KEY,
    'DD-APPLICATION-KEY': DATADOG_APP_KEY
}

# モニターのエクスポート
def export_monitors(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # 1行目のヘッダー "id" をスキップ
            for row in csv_reader:
                monitor_id = row[0]
                response = requests.get(f'https://api.datadoghq.com/api/v1/monitor/{monitor_id}', headers=headers)
                if response.status_code == 200:
                    monitor_data = response.json()
                    # Unicodeエスケープを無効にしてファイル出力
                    with open(f'{monitor_id}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(monitor_data, json_file, indent=4, ensure_ascii=False)
                    logging.info(f"Successfully exported monitor ID: {monitor_id}")
                else:
                    logging.error(f"Failed to export monitor ID: {monitor_id}, Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error during export process: {e}")

# モニターのインポート
def import_monitors(json_pattern):
    try:
        # 指定されたパターンに一致するすべてのファイルを取得
        json_files = glob.glob(json_pattern)
        if not json_files:
            print("No JSON files found matching the pattern.")
            return

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as file:
                monitor_data = json.load(file)
                response = requests.post('https://api.datadoghq.com/api/v1/monitor', headers=headers, json=monitor_data)
                if response.status_code == 200 or response.status_code == 201:
                    logging.info(f"Successfully imported monitor from file: {json_file}")
                else:
                    logging.error(f"Failed to import monitor from file: {json_file}, Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error during import process: {e}")

# アクションの選択に応じて処理を実行
if args.action == "export":
    export_monitors(args.file)
elif args.action == "import":
    import_monitors(args.file)

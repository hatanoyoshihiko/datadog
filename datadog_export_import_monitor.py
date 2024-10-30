import csv
import json
import logging
import argparse
import sys
import glob
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.models import *

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

# Datadog APIクライアントの設定
configuration = Configuration()
configuration.api_key['apiKeyAuth'] = DATADOG_API_KEY
configuration.api_key['appKeyAuth'] = DATADOG_APP_KEY

# モニターのエクスポート
def export_monitors(csv_file):
    try:
        with ApiClient(configuration) as api_client:
            api_instance = MonitorsApi(api_client)
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # 1行目のヘッダー "id" をスキップ
                for row in csv_reader:
                    monitor_id = int(row[0])
                    monitor_data = api_instance.get_monitor(monitor_id)
                    with open(f'{monitor_id}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(monitor_data.to_dict(), json_file, indent=4, ensure_ascii=False)
                    logging.info(f"Successfully exported monitor ID: {monitor_id}")
    except Exception as e:
        logging.error(f"Error during export process: {e}")

# モニターのインポート
def import_monitors(json_pattern):
    try:
        with ApiClient(configuration) as api_client:
            api_instance = MonitorsApi(api_client)
            json_files = glob.glob(json_pattern)
            if not json_files:
                print("No JSON files found matching the pattern.")
                return

            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as file:
                    monitor_data = json.load(file)
                    api_instance.create_monitor(monitor_data)
                    logging.info(f"Successfully imported monitor from file: {json_file}")
    except Exception as e:
        logging.error(f"Error during import process: {e}")

# アクションの選択に応じて処理を実行
if args.action == "export":
    export_monitors(args.file)
elif args.action == "import":
    import_monitors(args.file)

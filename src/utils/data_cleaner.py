import csv
from collections import defaultdict
from datetime import datetime


def parse_datetime(dt_str):
    """
    日時文字列をdatetimeオブジェクトに変換

    Args:
        dt_str: 日時文字列 (例: "2025-10-02 16:00")

    Returns:
        datetime: datetimeオブジェクト
    """
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        # フォーマットが異なる場合の処理
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d")
        except ValueError:
            return datetime.min


def merge_duplicate_corporations(input_csv_path, output_csv_path):
    """
    同じ法人名のレコードをマージする

    - 同じ法人名のレコードを1つにまとめる
    - 更新日時は最新のものを使用
    - 活動内容は時系列順に結合

    Args:
        input_csv_path: 入力CSVファイルパス
        output_csv_path: 出力CSVファイルパス
    """
    # 法人名ごとにレコードを収集
    corp_records = defaultdict(list)

    with open(input_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            corp_name = row['法人名']
            corp_records[corp_name].append(row)

    print(f"入力レコード数: {sum(len(records) for records in corp_records.values())}件")
    print(f"ユニーク法人数: {len(corp_records)}社")

    # マージ処理
    merged_records = []
    duplicate_count = 0

    for corp_name, records in corp_records.items():
        if len(records) > 1:
            duplicate_count += 1

        # 日時でソート（古い順）
        records.sort(key=lambda x: parse_datetime(x['更新日時']))

        # 最新の日時を取得
        latest_datetime = records[-1]['更新日時']

        # 活動内容を結合（時系列順）
        activities = []
        for i, record in enumerate(records, 1):
            dt = record['更新日時']
            content = record['活動内容'].strip()

            if len(records) > 1:
                # 複数のログがある場合は日時を付与
                activities.append(f"[{dt}]\n{content}")
            else:
                activities.append(content)

        merged_activity = "\n\n---\n\n".join(activities)

        # マージされたレコードを作成
        merged_record = {
            '更新日時': latest_datetime,
            '法人名': corp_name,
            '活動内容': merged_activity
        }

        merged_records.append(merged_record)

    # 更新日時でソート（新しい順）
    merged_records.sort(key=lambda x: parse_datetime(x['更新日時']), reverse=True)

    # CSVに書き込み
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['更新日時', '法人名', '活動内容']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_records)

    print(f"\n✓ クレンジング完了")
    print(f"出力レコード数: {len(merged_records)}件")
    print(f"マージされた法人数: {duplicate_count}社")
    print(f"出力ファイル: {output_csv_path}")

import os
import csv
from bs4 import BeautifulSoup


def parse_html_to_csv(html_files, output_csv_path):
    """
    複数のHTMLファイルをパースして、1つのCSVファイルに変換

    Args:
        html_files: HTMLファイルパスのリスト
        output_csv_path: 出力CSVファイルパス
    """
    all_records = []

    for html_file in html_files:
        print(f"処理中: {os.path.basename(html_file)}")
        records = extract_records_from_html(html_file)
        all_records.extend(records)
        print(f"  抽出件数: {len(records)}件")

    # CSVに書き込み
    if all_records:
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['更新日時', '法人名', '活動内容']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)

        print(f"\n✓ 変換完了: {output_csv_path}")
        print(f"総件数: {len(all_records)}件")
    else:
        print("\n⚠ データが見つかりませんでした")


def extract_records_from_html(html_file_path):
    """
    単一のHTMLファイルからレコードを抽出

    Args:
        html_file_path: HTMLファイルパス

    Returns:
        list: 抽出されたレコードのリスト
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    records = []

    # テーブルの行を探す（class_には完全一致ではなく部分一致を使用）
    rows = soup.find_all('tr', class_=lambda x: x and 'recordlist-row-gaia' in x)

    for row in rows:
        try:
            # 法人名を抽出（クラスリストから検索）
            corp_name_cell = row.find('td', class_=lambda x: x and 'value-6446950' in x)
            corp_name = corp_name_cell.get_text(strip=True) if corp_name_cell else ""

            # 活動日時を抽出（更新日時として使用）
            datetime_cell = row.find('td', class_=lambda x: x and 'value-6446951' in x)
            activity_datetime = datetime_cell.get_text(strip=True) if datetime_cell else ""

            # 活動内容を抽出
            content_cell = row.find('td', class_=lambda x: x and 'value-6446959' in x)
            activity_content = content_cell.get_text(strip=True) if content_cell else ""

            # データが揃っている場合のみ追加
            if corp_name and activity_datetime and activity_content:
                records.append({
                    '更新日時': activity_datetime,
                    '法人名': corp_name,
                    '活動内容': activity_content
                })

        except Exception as e:
            print(f"    行の解析エラー: {e}")
            continue

    return records

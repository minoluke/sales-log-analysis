import os
import sys
import csv

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.data_cleaner import merge_duplicate_corporations
from src.utils.content_validator import ContentValidator


def cleanse_and_validate(input_path, output_path, excluded_path):
    """
    データのLLM検証とクレンジングを実行

    処理順序:
    1. LLM検証 - 商談ログとして有効なレコードのみを抽出
    2. 重複統合 - 同じ法人名のレコードを時系列順にまとめる

    Args:
        input_path: 入力CSVファイルパス
        output_path: 出力CSVファイルパス（有効データ）
        excluded_path: 除外CSVファイルパス（無効データ）
    """
    # Step 1: LLM検証でメール文面などを除外
    print("\nStep 1: LLMによる商談判定を実行中...")
    validator = ContentValidator()

    # 元データを読み込み
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        raw_records = list(reader)

    print(f"  元データ: {len(raw_records)}件")

    # 一括検証
    valid_records, excluded_records = validator.validate_batch(
        raw_records,
        show_progress=True
    )

    print(f"\n✓ LLM検証完了")
    print(f"  有効なレコード: {len(valid_records)}件")
    print(f"  除外されたレコード: {len(excluded_records)}件")

    # Step 2: 有効なレコードのみを重複統合
    print(f"\nStep 2: 有効なレコードを企業ごとに統合中...")
    temp_validated = output_path.replace(".csv", "_temp.csv")

    # 一時的に有効データを保存
    with open(temp_validated, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['更新日時', '法人名', '活動内容']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_records)

    # 重複統合を実行
    merge_duplicate_corporations(temp_validated, output_path)

    print(f"  最終データ保存: {output_path}")

    # Step 3: 除外データを保存（監査用）
    if excluded_records:
        with open(excluded_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['更新日時', '法人名', '活動内容', '除外理由']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(excluded_records)
        print(f"  除外データ保存: {excluded_path}")

    # 一時ファイルを削除
    if os.path.exists(temp_validated):
        os.remove(temp_validated)


def main():
    """
    人事データと小売データのクレンジングを実行

    処理順序:
    1. LLM商談判定 → 2. 企業統合
    """
    print("=" * 60)
    print("商談ログデータの処理")
    print("処理順序: LLM商談判定 → 企業統合")
    print("=" * 60)

    # 人事データのクレンジング
    print("\n【人事データ】")
    hr_input = "data/raw/人事/人事.csv"
    hr_output = "data/cleaned/人事_cleaned.csv"
    hr_excluded = "data/excluded/人事_excluded.csv"

    if os.path.exists(hr_input):
        cleanse_and_validate(hr_input, hr_output, hr_excluded)
    else:
        print(f"⚠ ファイルが見つかりません: {hr_input}")

    # 小売データのクレンジング
    print("\n" + "=" * 60)
    print("【小売データ】")
    retail_input = "data/raw/小売/小売.csv"
    retail_output = "data/cleaned/小売_cleaned.csv"
    retail_excluded = "data/excluded/小売_excluded.csv"

    if os.path.exists(retail_input):
        cleanse_and_validate(retail_input, retail_output, retail_excluded)
    else:
        print(f"⚠ ファイルが見つかりません: {retail_input}")

    print("\n" + "=" * 60)
    print("✓ 全ての処理が完了しました")
    print("=" * 60)


if __name__ == "__main__":
    main()

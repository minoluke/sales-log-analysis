import os
import sys
import csv

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.openai_utils import OpenAIClient
from src.prompts.analysis_prompts import HRAnalysisPrompts

# OpenAI クライアントを初期化
openai_client = OpenAIClient()
prompts = HRAnalysisPrompts()


def analyze_activity(activity_content):
    """
    活動内容を分析し、リクルートのサービスに関連する要素を抽出（人事版）

    Args:
        activity_content: 分析対象の活動内容

    Returns:
        dict: 分析結果（各観点の該当有無）
    """
    system_prompt = prompts.get_system_prompt()
    user_prompt = prompts.get_user_prompt(activity_content)

    result = openai_client.analyze_with_prompt(system_prompt, user_prompt)

    # エラー時はデフォルト値を返す
    if result is None:
        return openai_client.get_hr_default_error_response()

    return result


def main():
    # CSVファイルを読み込む（クレンジング済みデータ）
    csv_path = "data/cleaned/人事_cleaned.csv"
    results = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, 1):
            print(f"\n処理中: {i}件目 - {row['法人名']}")

            # 活動内容を分析
            analysis = analyze_activity(row['活動内容'])

            # 結果を保存（フラットな構造に）
            result = {
                "更新日時": row['更新日時'],
                "法人名": row['法人名'],
                "活動内容": row['活動内容'],
                "リクルートブランドから": analysis.get("リクルートブランドから", 0),
                "人材課題の解決方法として": analysis.get("人材課題の解決方法として", 0),
                "福利厚生として": analysis.get("福利厚生として", 0),
                "前払い・即払いサービスを元から検討していたから": analysis.get("前払い・即払いサービスを元から検討していたから", 0),
                "デジタル給与対応であるから": analysis.get("デジタル給与対応であるから", 0)
            }

            results.append(result)

            # 分析結果を表示
            print(f"分析完了: {row['法人名']}")
            for key, value in analysis.items():
                if value == 1:
                    print(f"  - {key}: 該当")

    # 結果をCSVファイルに保存
    output_path = "results/analysis_results_hr.csv"
    if results:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                "更新日時", "法人名", "活動内容",
                "リクルートブランドから", "人材課題の解決方法として", "福利厚生として",
                "前払い・即払いサービスを元から検討していたから", "デジタル給与対応であるから"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print(f"\n\n分析完了！結果を {output_path} に保存しました。")
    print(f"総件数: {len(results)}件")


if __name__ == "__main__":
    main()

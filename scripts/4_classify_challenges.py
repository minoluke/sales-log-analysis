import os
import sys
import csv

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.openai_utils import OpenAIClient
from src.prompts.analysis_prompts import ChallengeClassificationPrompts

# OpenAI クライアントを初期化
openai_client = OpenAIClient()
prompts = ChallengeClassificationPrompts()


def classify_challenges(activity_content):
    """
    活動内容を分析し、顧客が抱える課題を分類

    Args:
        activity_content: 分析対象の活動内容

    Returns:
        dict: 分類結果（各課題の該当有無）
    """
    system_prompt = prompts.get_system_prompt()
    user_prompt = prompts.get_user_prompt(activity_content)

    result = openai_client.analyze_with_prompt(system_prompt, user_prompt)

    # エラー時はデフォルト値を返す
    if result is None:
        return openai_client.get_challenge_default_error_response()

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
            classification = classify_challenges(row['活動内容'])

            # 結果を保存（フラットな構造に）
            result = {
                "更新日時": row['更新日時'],
                "法人名": row['法人名'],
                "活動内容": row['活動内容'],
                "特定の状況下での人材獲得の困難さ": classification.get("特定の状況下での人材獲得の困難さ", 0),
                "採用市場での競争激化": classification.get("採用市場での競争激化", 0),
                "外部労働力への依存と 直接雇用強化のニーズ": classification.get("外部労働力への依存と 直接雇用強化のニーズ", 0),
                "採用難への打ち手がない": classification.get("採用難への打ち手がない", 0),
                "若手を採用できない": classification.get("若手を採用できない", 0),
                "アルバイトパートの採用課題": classification.get("アルバイトパートの採用課題", 0),
                "シフトの欠員": classification.get("シフトの欠員", 0),
                "高い離職率・定着への課題": classification.get("高い離職率・定着への課題", 0),
                "若手の早期離職への課題": classification.get("若手の早期離職への課題", 0),
                "エンゲージメントの向上": classification.get("エンゲージメントの向上", 0),
                "福利厚生": classification.get("福利厚生", 0),
                "前払いニーズ": classification.get("前払いニーズ", 0)
            }

            results.append(result)

            # 分類結果を表示
            print(f"分類完了: {row['法人名']}")
            for key, value in classification.items():
                if value == 1:
                    print(f"  - {key}: 該当")

    # 結果をCSVファイルに保存
    output_path = "results/challenge_classification.csv"
    if results:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                "更新日時", "法人名", "活動内容",
                "特定の状況下での人材獲得の困難さ",
                "採用市場での競争激化",
                "外部労働力への依存と 直接雇用強化のニーズ",
                "採用難への打ち手がない",
                "若手を採用できない",
                "アルバイトパートの採用課題",
                "シフトの欠員",
                "高い離職率・定着への課題",
                "若手の早期離職への課題",
                "エンゲージメントの向上",
                "福利厚生",
                "前払いニーズ"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print(f"\n\n課題分類完了！結果を {output_path} に保存しました。")
    print(f"総件数: {len(results)}件")


if __name__ == "__main__":
    main()

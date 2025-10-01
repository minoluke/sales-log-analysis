import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# OpenAI クライアントを初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_activity(activity_content):
    """
    活動内容を分析し、リクルートのサービスに関連する要素を抽出
    """
    prompt = f"""
以下の営業商談ログを読んで、リクルート社の給与前払い・即払いサービスを提案する際に使えそうな要素が含まれているかを判断してください。

商談ログ:
{activity_content}

以下の観点で、この商談内容に該当する要素があるかを厳密に判定してください。
該当する要素が明確に読み取れる場合のみ1を返し、不明確な場合や関係ない内容の場合は0を返してください。

観点:
1. リクルートブランド: リクルートのブランド力や知名度が重要な要素になっていることが明確に読み取れる場合。
2. 人材課題の解決: 人材確保、採用、定着、離職防止などの人材に関する課題が商談内容に明確に含まれている場合
3. 福利厚生に効くこと: 従業員の福利厚生や満足度向上についてが商談内容に明確に含まれている場合
4. 前払い・即払いサービスを元から検討していた: 前払い・即払い自体を元々検討していた。それが明確に読み取れる場合のみ。
5. デジタル給与対応であること: デジタル給与のニーズが商談内容に明確に含まれている場合

重要: 商談内容と関係ない観点は必ず0にしてください。推測や一般論ではなく、商談ログに明確に書かれている内容のみで判断してください。

JSON形式で以下のように回答してください（1=該当する、0=該当しない）:
{{
  "リクルートブランド": 1 または 0,
  "人材課題の解決": 1 または 0,
  "福利厚生に効くこと": 1 または 0,
  "前払い・即払いサービスであること": 1 または 0,
  "デジタル給与対応であること": 1 または 0,
  "その他": 1 または 0
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは営業分析のエキスパートです。給与前払い・即払いサービスの商談ログを分析し、プロダクトのどの要素が顧客に刺さったか、何が商談のきっかけになったかを特定します。"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"分析エラー: {e}")
        return {
            "リクルートブランド": 0,
            "人材課題の解決": 0,
            "福利厚生に効くこと": 0,
            "前払い・即払いサービスであること": 0,
            "デジタル給与対応であること": 0,
            "その他": 0
        }

def main():
    # CSVファイルを読み込む
    csv_path = "log_data/小売.csv"
    results = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, 1):
            print(f"\n処理中: {i}件目 - {row['法人名']}")

            # 活動内容を分析
            analysis = analyze_activity(row['活動内容'])

            # 結果を保存
            result = {
                "更新日時": row['更新日時'],
                "法人名": row['法人名'],
                "活動内容": row['活動内容'],
                "分析結果": analysis
            }

            results.append(result)

            # 分析結果を表示
            print(f"分析完了: {row['法人名']}")
            for key, value in analysis.items():
                if value == 1:
                    print(f"  - {key}: 該当")

    # 結果をJSONファイルに保存
    output_path = "analysis_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n\n分析完了！結果を {output_path} に保存しました。")
    print(f"総件数: {len(results)}件")

if __name__ == "__main__":
    main()

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()


class OpenAIClient:
    """OpenAI APIクライアントのラッパークラス"""

    def __init__(self, api_key=None):
        """
        OpenAIクライアントを初期化

        Args:
            api_key: OpenAI APIキー（Noneの場合は環境変数から取得）
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def analyze_with_prompt(self, system_prompt, user_prompt, model="gpt-4o-mini", temperature=0.3):
        """
        プロンプトを使用してOpenAI APIで分析を実行

        Args:
            system_prompt: システムプロンプト
            user_prompt: ユーザープロンプト
            model: 使用するモデル名
            temperature: 生成の温度パラメータ

        Returns:
            dict: 分析結果（JSON形式）
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=temperature
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"分析エラー: {e}")
            return None

    def get_default_error_response(self):
        """
        エラー時のデフォルト応答を返す（小売版）

        Returns:
            dict: すべての項目が0の辞書
        """
        return {
            "リクルートブランド": 0,
            "人材課題の解決": 0,
            "福利厚生に効くこと": 0,
            "前払い・即払いサービスであること": 0,
            "デジタル給与対応であること": 0,
            "その他": 0
        }

    def get_hr_default_error_response(self):
        """
        エラー時のデフォルト応答を返す（人事版）

        Returns:
            dict: すべての項目が0の辞書
        """
        return {
            "リクルートブランドから": 0,
            "人材課題の解決方法として": 0,
            "福利厚生として": 0,
            "前払い・即払いサービスを元から検討していたから": 0,
            "デジタル給与対応であるから": 0
        }

    def get_challenge_default_error_response(self):
        """
        エラー時のデフォルト応答を返す（課題分類版）

        Returns:
            dict: すべての項目が0の辞書
        """
        return {
            "特定の状況下での人材獲得の困難さ": 0,
            "採用市場での競争激化": 0,
            "外部労働力への依存と 直接雇用強化のニーズ": 0,
            "採用難への打ち手がない": 0,
            "若手を採用できない": 0,
            "アルバイトパートの採用課題": 0,
            "シフトの欠員": 0,
            "高い離職率・定着への課題": 0,
            "若手の早期離職への課題": 0,
            "エンゲージメントの向上": 0,
            "福利厚生": 0,
            "前払いニーズ": 0
        }

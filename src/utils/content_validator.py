import json
from utils.openai_utils import OpenAIClient


class ContentValidator:
    """LLMを使って活動内容が商談ログとして適切かどうかを検証"""

    def __init__(self):
        self.client = OpenAIClient()

    def get_system_prompt(self):
        """
        システムプロンプトを取得

        Returns:
            str: システムプロンプト
        """
        return """あなたは商談ログの品質を判定するエキスパートです。
与えられた活動内容が、営業商談のログとして適切かどうかを判定してください。

以下のような内容は「適切でない」と判定してください：
- メールの文面や連絡事項のみ
- 自動送信されたメッセージやシステム通知
- 単なる日程調整のみの内容
- 空白や意味のない文字列
- 商談の実質的な内容が含まれていないもの

以下のような内容は「適切」と判定してください：
- 顧客との商談内容や会話の記録
- ヒアリング結果や提案内容
- 顧客の課題や要望
- 商談の進捗状況や次のアクション
- 商談に関する具体的な情報"""

    def get_user_prompt(self, activity_content):
        """
        ユーザープロンプトを取得

        Args:
            activity_content: 検証対象の活動内容

        Returns:
            str: ユーザープロンプト
        """
        return f"""
以下の活動内容が、営業商談のログとして適切かどうかを判定してください。

活動内容:
{activity_content}

判定基準：
- 商談の実質的な内容（顧客の課題、提案、ヒアリング結果など）が含まれていれば「適切」
- メールの文面のみ、日程調整のみ、自動通知などは「不適切」

JSON形式で以下のように回答してください：
{{
  "is_valid": true または false,
  "reason": "判定理由を簡潔に（30文字以内）"
}}
"""

    def validate_content(self, activity_content):
        """
        活動内容が商談ログとして適切かどうかを検証

        Args:
            activity_content: 検証対象の活動内容

        Returns:
            dict: {"is_valid": bool, "reason": str}
        """
        # 空白チェック
        if not activity_content or len(activity_content.strip()) < 10:
            return {
                "is_valid": False,
                "reason": "内容が空またはあまりにも短い"
            }

        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(activity_content)

        try:
            result = self.client.analyze_with_prompt(
                system_prompt,
                user_prompt,
                temperature=0.1  # より確実な判定のため低めに設定
            )

            if result and "is_valid" in result:
                return result
            else:
                # エラー時は保守的に有効と判定
                return {
                    "is_valid": True,
                    "reason": "検証エラーのため有効と判定"
                }

        except Exception as e:
            print(f"    検証エラー: {e}")
            # エラー時は保守的に有効と判定
            return {
                "is_valid": True,
                "reason": "検証エラーのため有効と判定"
            }

    def validate_batch(self, records, show_progress=True):
        """
        複数のレコードを一括検証

        Args:
            records: 検証対象のレコードリスト（dict形式）
            show_progress: 進捗表示するかどうか

        Returns:
            tuple: (valid_records, excluded_records)
        """
        valid_records = []
        excluded_records = []

        total = len(records)

        for i, record in enumerate(records, 1):
            if show_progress:
                # より詳細な進捗表示
                corp_name = record.get('法人名', 'Unknown')
                progress_bar = "=" * int(30 * i / total)
                progress_pct = int(100 * i / total)
                print(f"  [{progress_bar:<30}] {progress_pct}% ({i}/{total}) - {corp_name[:20]}", end="\r")

            validation_result = self.validate_content(record.get('活動内容', ''))

            if validation_result['is_valid']:
                valid_records.append(record)
            else:
                # 除外理由を追加
                record['除外理由'] = validation_result['reason']
                excluded_records.append(record)

        if show_progress:
            print()  # 改行

        return valid_records, excluded_records

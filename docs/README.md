# 商談ログ分析ツール

商談ログを分析し、顧客がどの要素に刺さったかを可視化するAIツール

> **🚀 すぐ使いたい方へ:** [QUICK_START.md](QUICK_START.md) で1分で使い方を把握できます

---

## 🚀 クイックスタート

### 1️⃣ セットアップ（初回のみ）

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# .envファイルを作成してAPIキーを設定
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

---

### 2️⃣ データ準備

#### 人事データの場合（HTMLから）

```bash
# Step 1: HTMLをCSVに変換
python convert_html_to_csv.py
```

**入力:** `log_data/人事/htmls/*.html`
**出力:** `log_data/人事/csv/人事.csv`

#### 小売データの場合

既にCSV形式のため変換不要。`log_data/小売/小売.csv`をそのまま使用。

---

### 3️⃣ データクレンジング + AI検証

```bash
python cleanse_data.py
```

**処理順序:** LLM商談判定 → 企業統合

**処理内容:**
1. **AIが商談ログとして不適切な内容を自動除外**
   - メール文面のみ → 除外
   - 日程調整のみ → 除外
   - 空白/無意味な内容 → 除外

2. **有効なレコードのみを企業ごとに統合**
   - 重複する法人を統合（時系列順に活動内容を結合）

**出力:**
- `log_data/人事/csv/人事_cleaned.csv` ← 有効データ
- `log_data/人事/csv/人事_excluded.csv` ← 除外データ（監査用）
- `log_data/小売/小売_cleaned.csv` ← 有効データ
- `log_data/小売/小売_excluded.csv` ← 除外データ（監査用）

---

### 4️⃣ 商談ログ分析

```bash
# 人事データの分析
python analyze_logs_hr.py

# 人事データの課題分類（新機能）
python classify_challenges.py

# 小売データの分析
python analyze_logs.py
```

**出力:**
- `analysis_results_hr.csv` ← 人事データの分析結果（訴求ポイント）
- `challenge_classification.csv` ← 人事データの課題分類結果（新機能）
- `analysis_results.csv` ← 小売データの分析結果

**分析観点（人事版）:**
1. リクルートブランドから
2. 人材課題の解決方法として
3. 福利厚生として
4. 前払い・即払いサービスを元から検討していたから
5. デジタル給与対応であるから

**分析観点（小売版）:**
1. リクルートブランド
2. 人材課題の解決
3. 福利厚生に効くこと
4. 前払い・即払いサービスであること
5. デジタル給与対応であること
6. その他

**課題分類（人事版のみ - 12項目）:**

採用・人材確保に関する課題：
- 特定の状況下での人材獲得の困難さ
- 採用市場での競争激化
- 外部労働力への依存と 直接雇用強化のニーズ
- 採用難への打ち手がない
- 若手を採用できない
- アルバイトパートの採用課題
- シフトの欠員

定着・労務・制度に関する課題：
- 高い離職率・定着への課題
- 若手の早期離職への課題
- エンゲージメントの向上
- 福利厚生
- 前払いニーズ

---

## 📊 実行例

```bash
# 人事データの完全実行フロー
python convert_html_to_csv.py    # HTMLをCSVに変換
python cleanse_data.py           # クレンジング + AI検証
python analyze_logs_hr.py        # 訴求ポイント分析
python classify_challenges.py    # 課題分類（新機能）

# 小売データの完全実行フロー（HTML変換不要）
python cleanse_data.py           # クレンジング + AI検証
python analyze_logs.py           # 商談ログ分析
```

---

## 📁 ファイル構成

```
商談ログ解析/
├── README.md                    ← このファイル
├── WORKFLOW.md                  ← 詳細ドキュメント
├── .env                         ← OpenAI APIキー（要作成）
├── requirements.txt
│
├── convert_html_to_csv.py       # HTML→CSV変換
├── cleanse_data.py              # クレンジング + AI検証
├── analyze_logs.py              # 小売データ分析
├── analyze_logs_hr.py           # 人事データ分析（訴求ポイント）
├── classify_challenges.py       # 人事データ課題分類（新機能）
│
├── utils/
│   ├── html_parser.py           # HTMLパーサー
│   ├── data_cleaner.py          # 重複統合
│   ├── content_validator.py     # AI検証
│   └── openai_utils.py          # OpenAI API
│
├── prompts/
│   └── analysis_prompts.py      # プロンプト管理
│
└── log_data/
    ├── 人事/
    │   ├── htmls/*.html         # 元データ
    │   └── csv/
    │       ├── 人事.csv         # 変換後
    │       ├── 人事_cleaned.csv # AI検証済み
    │       └── 人事_excluded.csv # 除外データ
    │
    └── 小売/
        ├── 小売.csv             # 元データ
        ├── 小売_cleaned.csv     # AI検証済み
        └── 小売_excluded.csv    # 除外データ
```

---

## 💡 使い方のポイント

### AI検証の効果

処理フロー:

```
【人事データ】
575件（元データ）
 → Step 1: AI商談判定 → ???件（有効） + 除外データ
 → Step 2: 企業統合 → ???件（最終）
```

**メリット:** 先にノイズを除外してから統合するため、より高品質なデータになります

### 除外データの確認

`*_excluded.csv`を確認することで、AIがどのような判断をしたか監査できます。

```csv
更新日時,法人名,活動内容,除外理由
2024-01-15 10:00,株式会社〇〇,打ち合わせ日程調整のメール,日程調整のみの内容
```

### API料金の目安

- gpt-4o-mini使用
- **小売データ（10件）:** 約 $0.01〜$0.02
- **人事データ（575件）:** 約 $0.60〜$1.00

**注:** 元データ数に対してAPI呼び出しが発生します（LLM商談判定のため）

---

## ⚙️ 設定変更

### 分析モデルの変更

`utils/openai_utils.py:22` を編集:

```python
# デフォルト: gpt-4o-mini（高速・低コスト）
# 高精度が必要な場合: gpt-4o
model="gpt-4o"
```

### 分析観点のカスタマイズ

`prompts/analysis_prompts.py` でプロンプトを編集可能。

---

## 🐛 トラブルシューティング

### エラー: `ModuleNotFoundError`

```bash
pip install -r requirements.txt
```

### エラー: `openai.AuthenticationError`

`.env`ファイルを確認:

```bash
cat .env
# OPENAI_API_KEY=sk-... ← 正しいAPIキーが設定されているか
```

### HTMLが見つからない

人事データのHTMLは `log_data/人事/htmls/` に配置してください。

### 分析結果が全て0

- クレンジング済みデータ(`*_cleaned.csv`)を使用しているか確認
- プロンプトが適切か `prompts/analysis_prompts.py` を確認

---

## 📚 詳細情報

より詳しい仕様や処理の流れは [WORKFLOW.md](WORKFLOW.md) を参照してください。

---

## 🔧 必要な環境

- Python 3.8以上
- OpenAI APIキー
- インターネット接続（API通信用）

---

**作成日:** 2025年10月
**使用AI:** GPT-4o-mini（分析・検証用）

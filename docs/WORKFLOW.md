# 商談ログ分析ワークフロー

## 📋 処理フロー

### 1. HTMLからCSVへの変換（人事データのみ）

```bash
python convert_html_to_csv.py
```

**入力:** `log_data/人事/htmls/*.html`
**出力:** `log_data/人事/csv/人事.csv`

HTMLファイルから「更新日時」「法人名」「活動内容」を抽出してCSVに変換します。

---

### 2. データクレンジング + LLM検証（必須）

```bash
python cleanse_data.py
```

**処理順序:** LLM商談判定 → 企業統合

**処理内容:**
1. **LLM商談判定:** 商談ログとして不適切な内容を自動除外
   - メールの文面のみ → 除外
   - 日程調整のみ → 除外
   - 自動送信メッセージ → 除外
   - 空白や無意味な文字列 → 除外
   - **商談の実質的内容のみを抽出**

2. **企業統合:** 有効なレコードのみを企業ごとに統合
   - 同じ法人名のレコードを1つにまとめる
   - 更新日時は最新のものを使用
   - 活動内容は時系列順に結合（`---`で区切り）

**人事データ:**
- 入力: `log_data/人事/csv/人事.csv` (575件)
- 出力: `log_data/人事/csv/人事_cleaned.csv` (LLM検証後)
- 除外: `log_data/人事/csv/人事_excluded.csv` (監査用)

**小売データ:**
- 入力: `log_data/小売/小売.csv` (10件)
- 出力: `log_data/小売/小売_cleaned.csv` (LLM検証後)
- 除外: `log_data/小売/小売_excluded.csv` (監査用)

---

### 3. 商談ログ分析

#### 人事データの分析

```bash
python analyze_logs_hr.py
```

**入力:** `log_data/人事/csv/人事_cleaned.csv`
**出力:** `analysis_results_hr.csv`

**分析観点（5項目）:**
1. リクルートブランドから
2. 人材課題の解決方法として
3. 福利厚生として
4. 前払い・即払いサービスを元から検討していたから
5. デジタル給与対応であるから

#### 課題分類（人事データのみ）

```bash
python classify_challenges.py
```

**入力:** `log_data/人事/csv/人事_cleaned.csv`
**出力:** `challenge_classification.csv`

**分類観点（12項目）:**

**採用・人材確保に関する課題（7項目）:**
1. 特定の状況下での人材獲得の困難さ
2. 採用市場での競争激化
3. 外部労働力への依存と 直接雇用強化のニーズ
4. 採用難への打ち手がない
5. 若手を採用できない
6. アルバイトパートの採用課題
7. シフトの欠員

**定着・労務・制度に関する課題（5項目）:**
1. 高い離職率・定着への課題
2. 若手の早期離職への課題
3. エンゲージメントの向上
4. 福利厚生
5. 前払いニーズ

#### 小売データの分析

```bash
python analyze_logs.py
```

**入力:** `log_data/小売/小売_cleaned.csv`
**出力:** `analysis_results.csv`

**分析観点（6項目）:**
1. リクルートブランド
2. 人材課題の解決
3. 福利厚生に効くこと
4. 前払い・即払いサービスであること
5. デジタル給与対応であること
6. その他

---

## 📁 ファイル構成

```
商談ログ解析/
├── convert_html_to_csv.py      # HTML→CSV変換
├── cleanse_data.py             # データクレンジング + LLM検証
├── analyze_logs.py             # 小売データ分析
├── analyze_logs_hr.py          # 人事データ分析
├── utils/
│   ├── html_parser.py          # HTMLパーサー
│   ├── data_cleaner.py         # 重複統合
│   ├── content_validator.py    # LLM検証
│   └── openai_utils.py         # OpenAI API
├── prompts/
│   └── analysis_prompts.py     # プロンプト管理
└── log_data/
    ├── 人事/
    │   ├── htmls/              # 元データ（HTML）
    │   └── csv/
    │       ├── 人事.csv        # 変換後データ
    │       ├── 人事_cleaned.csv # LLM検証済み（有効データ）
    │       └── 人事_excluded.csv # 除外データ（監査用）
    └── 小売/
        ├── 小売.csv            # 元データ
        ├── 小売_cleaned.csv    # LLM検証済み（有効データ）
        └── 小売_excluded.csv   # 除外データ（監査用）
```

**注:** `validate_content.py`はスタンドアロン実行用（非推奨）。通常は`cleanse_data.py`に統合されています。

---

## 🔧 セットアップ

```bash
pip install -r requirements.txt
```

`.env`ファイルにOpenAI APIキーを設定:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 📊 処理結果

### 人事データ
```
575件（元データ）
  ↓ Step 1: LLM商談判定
???件（有効なレコード） + 除外データ
  ↓ Step 2: 企業統合
???件（最終データ）
```

- 入力: 575件
- 除外データ → `人事_excluded.csv`（LLM判定）
- **最終データ → `人事_cleaned.csv`**（LLM検証 + 企業統合済み）

### 小売データ
```
10件（元データ）
  ↓ Step 1: LLM商談判定
???件（有効なレコード） + 除外データ
  ↓ Step 2: 企業統合
???件（最終データ）
```

- 入力: 10件
- 除外データ → `小売_excluded.csv`（LLM判定）
- **最終データ → `小売_cleaned.csv`**（LLM検証 + 企業統合済み）

**注意:**
- 先にLLM検証でメール文面などを除外してから企業統合するため、より高品質なデータになります
- API呼び出し回数は元データ数（575件 or 10件）分発生します

# ⚡ クイックスタート（1分で理解）

## 💻 セットアップ

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_api_key" > .env
```

---

## 🎯 使い方（3ステップ）

### 人事データの場合

```bash
python convert_html_to_csv.py    # ①HTMLをCSVに変換
python cleanse_data.py           # ②AI商談判定→企業統合
python analyze_logs_hr.py        # ③訴求ポイント分析
python classify_challenges.py    # ④課題分類（新機能）
```

### 小売データの場合

```bash
python cleanse_data.py           # ①AI商談判定→企業統合
python analyze_logs.py           # ②商談ログ分析
```

---

## 📤 出力ファイル

| ファイル | 内容 |
|---------|------|
| `人事_cleaned.csv` | AI検証済みの有効な商談ログ |
| `人事_excluded.csv` | メール文面など除外データ |
| `analysis_results_hr.csv` | **訴求ポイント分析結果（人事版）** |
| `challenge_classification.csv` | **課題分類結果（人事版・新機能）** |
| `小売_cleaned.csv` | AI検証済みの有効な商談ログ |
| `小売_excluded.csv` | メール文面など除外データ |
| `analysis_results.csv` | **分析結果（小売版）** |

---

## 📊 分析結果の見方

**analysis_results_hr.csv の例:**

| 法人名 | リクルートブランドから | 人材課題の解決方法として | 福利厚生として | ... |
|--------|:---:|:---:|:---:|-----|
| 株式会社A | 1 | 1 | 0 | ... |
| 株式会社B | 0 | 1 | 1 | ... |

- **1** = その要素が商談で刺さった
- **0** = その要素は関係なかった

---

## 🔍 データの流れ

```
[HTML]
  ↓ convert_html_to_csv.py
[CSV（元データ）]
  ↓ cleanse_data.py
  ├─ Step 1: AI商談判定（メール文面などを除外）
  └─ Step 2: 企業統合（有効データのみをまとめる）
[CSV（クリーンデータ）]
  ↓ analyze_logs_hr.py / analyze_logs.py
[分析結果CSV]
```

**ポイント:** 先にノイズを除外してから統合 = 高品質なデータ

---

## 💰 API料金

- 小売: 約 $0.01〜0.02（10件）
- 人事: 約 $0.60〜1.00（575件）

**注:** 元データ数に対してAPI呼び出しが発生

---

## 📚 詳しく知りたい

- [README.md](README.md) - 完全ガイド
- [WORKFLOW.md](WORKFLOW.md) - 技術詳細

---

**所要時間:** 人事データ（289件）で約10〜15分

import os
import sys
import glob

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.html_parser import parse_html_to_csv


def main():
    """人事データのHTMLファイルをCSVに変換"""
    # HTMLファイルのディレクトリ
    html_dir = "data/raw/人事/htmls"

    # CSVの出力先
    output_csv = "data/raw/人事/人事.csv"

    # HTMLファイルをすべて取得
    html_files = sorted(glob.glob(os.path.join(html_dir, "*.html")))

    if not html_files:
        print(f"⚠ HTMLファイルが見つかりません: {html_dir}")
        return

    print(f"HTMLファイル数: {len(html_files)}件\n")

    # HTML to CSV変換
    parse_html_to_csv(html_files, output_csv)


if __name__ == "__main__":
    main()

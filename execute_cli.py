from data_module import CSVColumnSummer
from plot_module import Plotter
import argparse
from main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSVのカラムを合計し、グラフを作成するコマンドラインツール")

    # 必須引数
    parser.add_argument("csv_file_path", 
                        help="入力するCSVファイルのパス"
                        )
    
    parser.add_argument("-d","--delimiter", 
                        default=",", 
                        help="区切り文字（デフォルト: ,）"
                        )

    # オプション引数
    parser.add_argument("-n","--new_data_name",
                        default="synthetic wave", 
                        help="追加するカラム名（デフォルト: synthetic wave）"
                        )

    parser.add_argument("-s","--save_path", 
                        default='./added_data.csv', 
                        help="結果CSVの保存パス（デフォルト: ./added_data.csv）"
                        )
    
    parser.add_argument("-g","--save_graph", 
                        action="store_true", 
                        help="グラフをファイルとして保存するかどうか"
                        )
    
    parser.add_argument("-f",
                        default=True,
                        action="store_false", 
                        help="設定時、NaNを'-fv'で埋めしない"
                        )
    
    parser.add_argument("-fv","--fillna_value",
                        default=0, 
                        type=float,
                        help="NaNを埋める値（デフォルト: 0）"
                        )
    
    parser.add_argument("-fmt","--format",
                        default='%8g', 
                        help="CSV出力時の数値フォーマット（デフォルト: %8g）。\
                            有効数字8桁、指数表記対応、末尾の不要なゼロは自動的に省略されます。"
                        )
    
    parser.add_argument("-img","--save_graph_name","--image_name",
                        default=None, 
                        help="グラフの保存名（デフォルト: None）"
                        )

    args = parser.parse_args()

    main(
        csv_file_path=args.csv_file_path,
        delimiter=args.delimiter,
        save_path=args.save_path,
        new_data_name=args.new_data_name,
        save_graph=args.save_graph,
        fillna=args.fillna,
        fillna_value=args.fillna_value,
        fmt=args.fmt,
        image_name=args.save_graph_name
    )
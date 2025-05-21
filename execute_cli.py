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

    args = parser.parse_args()

    main(
        csv_file_path=args.csv_file_path,
        delimiter=args.delimiter,
        save_path=args.save_path,
        new_data_name=args.new_data_name,
        save_graph=args.save_graph,
    )
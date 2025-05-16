from data_module import CSVColumnSummer
from plot_module import Ploter
import argparse
from main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV 컬럼 합산 및 그래프 그리기")

    # 필수 인자
    parser.add_argument("csv_file_path", 
                        help="입력 CSV 파일 경로"
                        )
    
    parser.add_argument("-d","--delimiter", 
                        default=",", 
                        help="구분자 (기본: ,)"
                        )

    # 옵션 인자
    parser.add_argument("-n","--new_data_name", 
                        default="synthetic wave", 
                        help="추가 컬럼명 (기본: synthetic wave)"
                        )

    parser.add_argument("-s","--save_path", 
                        default='./added_data.csv', 
                        help="결과 CSV 저장 경로 (기본: ./added_data.csv)"
                        )
    
    parser.add_argument("-g","--save_graph", 
                        action="store_true", 
                        help="그래프를 파일로 저장할지 여부"
                        )

    args = parser.parse_args()

    main(
        csv_file_path=args.csv_file_path,
        delimiter=args.delimiter,
        save_path=args.save_path,
        new_data_name=args.new_data_name,
        save_graph=args.save_graph,
    )
from csv_module import *

if __name__ == "__main__":
    # option
    loader = 'np'  # np or pd
    delimiter = ','  # 구분자

    # example_file_path = '../sample_waves_invalid.csv' # invalid data
    example_file_path = '../sample_waves_space.csv' # space data
    # example_file_path = '../sample_waves_stringed.csv' # string data (문자열 데이터가 포함됨)


    example_file_path = validate_csv_path(example_file_path)
    data = load_csv_file(example_file_path, delimiter=delimiter, loader=loader)

    print(data)
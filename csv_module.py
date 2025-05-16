import os
import numpy as np
import pandas as pd

class InvalidFileTypeError(Exception):
    """CSV파일이 아닐 경우"""
    pass

class CSVFileReadError(Exception):
    """CSV파일을 읽어오지 못할 경우"""
    pass


def load_csv_file(csv_path, delimiter=',', loader = 'np'):
    """
    CSV파일을 읽어온다.
    :param csv_path: CSV파일 경로
    :param delimiter: CSV파일 구분자
    :param loader: np, pd
    :return: CSV파일 데이터
    """
    
    def _load_csv_with_numpy(csv_path, delimiter=','):
        """
        numpy로 CSV파일을 읽어온다.
        :param csv_path: CSV파일 경로
        :param delimiter: CSV파일 구분자
        :return: CSV파일 데이터
        """
        data = None
        try:    
            data = np.genfromtxt(csv_path, delimiter=delimiter, skip_header=True, filling_values=0)
        except Exception as e:
            print(e)
        return data

    def _load_csv_with_pandas(csv_path, delimiter=','):
        """
        pandas로 CSV파일을 읽어온다.
        :param csv_path: CSV파일 경로
        :param delimiter: CSV파일 구분자
        :return: CSV파일 데이터
        """
        data = None
        try:    
            data = pd.read_csv(csv_path, delimiter=delimiter)
        except Exception as e:
            print(e)
        return data

    csv_path = validate_csv_path(csv_path)

    if loader.startswith('np') or loader.endswith('np'):
        try:
            data = _load_csv_with_numpy(csv_path, delimiter)
        except Exception as e:
            print(e)
            print("load error for pandas")
        

    if loader.startswith('pd') or loader.endswith('pd'):
        try:
            data = _load_csv_with_pandas(csv_path)
        except Exception as e:
            print(e)
            print("load error for pandas")

    if data is None:
        raise CSVFileReadError("Error reading CSV file: {}".format(csv_path))
    
    return data


def validate_csv_path(csv_path):
    """
    파일의 경로를 체크한다
    """
    if not csv_path.endswith('.csv'):
        raise InvalidFileTypeError("File must be a CSV file.")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    return csv_path

if __name__ == "__main__":
    # Example usage
    example_file_path = '../sample_waves.csv'
    example_file_path = validate_csv_path(example_file_path)
    data = load_csv_file(example_file_path, delimiter=',', loader='np')

    print(data)
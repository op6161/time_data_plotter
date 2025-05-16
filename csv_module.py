import os
import numpy as np
import pandas as pd

class InvalidFileTypeError(Exception):
    """CSV파일이 아닐 경우"""
    pass

class CSVFileReadError(Exception):
    """CSV파일을 읽어오지 못할 경우
    Attributes:
        filepath (str): CSV파일 경로
        original_exception (Exception): 원래 발생한 예외
        message (str): 오류 메시지
    """
    def __init__(self, filepath, original_exception=None):
        self.filepath = filepath
        self.original_exception = original_exception
        self.message = f"CSV 파일을 읽을 수 없습니다: {filepath}"
        if original_exception:
            self.message += f" (원인: {original_exception})"
        super().__init__(self.message)

    def __str__(self):
        return self.message
    pass


def load_csv_file(csv_path, delimiter=',', loader = 'np', fillna=True, fillna_value=0):
    """
    CSV파일을 읽어온다.
    Args:
        csv_path (str): CSV파일의 경로
        delimiter (str): CSV파일 구분자  default: ','
        loader (str): np, pd 중 선택    default: 'np'

    Returns:
        data (np.ndarray or pd.DataFrame): CSV파일 데이터

    Raises:
        CSVFileReadError: CSV파일을 읽어오지 못할 경우
        InvalidFileTypeError: CSV파일이 아닐 경우

    Example:
        data = load_csv_file('data.csv', delimiter=',', loader='np')
        data = load_csv_file('data.csv', delimiter=',', loader='pd')
    """
    
    def _load_csv_with_numpy(csv_path, delimiter, fillna=True ,fillna_value=0):
        """
        numpy로 CSV파일을 읽어온다.
        Args:
            csv_path (str): CSV파일의 경로
            delimiter (str): CSV파일 구분자  default: ','

        Returns:
            data (np.ndarray): CSV파일 데이터
        """
        args = {
            'delimiter': delimiter,
            'skip_header': 1,
            }
        if fillna:
            args['filling_values'] = fillna_value
        
        data = np.genfromtxt(csv_path, **args)
        return data

    def _load_csv_with_pandas(csv_path, delimiter):
        """
        pandas로 CSV파일을 읽어온다.
        Args:
            csv_path (str): CSV파일의 경로
            delimiter (str): CSV파일 구분자  default: ','

        Returns:
            data (pd.DataFrame): CSV파일 데이터
        """
        data = pd.read_csv(csv_path, delimiter=delimiter, skiprows=1)
        return data

    csv_path = validate_csv_path(csv_path)

    if loader.startswith('np') or loader.endswith('np'):
        data = _load_csv_with_numpy(csv_path, delimiter, fillna=fillna, fillna_value=fillna_value)    
    if loader.startswith('pd') or loader.endswith('pd'):
        data = _load_csv_with_pandas(csv_path, delimiter)

    if data.shape == (0,):
        raise CSVFileReadError("Error reading CSV file: {}".format(csv_path), data.shape)
    elif np.isnan(data).all():
        raise CSVFileReadError("Error reading CSV file: {}".format(csv_path) + " (only NaN values found)")
    
    return data


def validate_csv_path(csv_path):
    """ 
    CSV파일 경로를 검증한다.
    Args:
        csv_path (str): CSV파일의 경로

    Returns:
        csv_path (str): 검증된 CSV파일 경로

    Raises:
        InvalidFileTypeError: CSV파일이 아닐 경우
        FileNotFoundError: 파일을 찾을 수 없을 경우
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
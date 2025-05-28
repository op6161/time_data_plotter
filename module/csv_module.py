import os
import numpy as np
import pandas as pd

class InvalidFileTypeError(Exception):
    """CSVファイルでない場合に発生する例外"""
    pass

class CSVFileReadError(Exception):
    """CSVファイルの読み込みに失敗した場合に発生する例外
    Attributes:
        filepath (str): CSVファイルのパス
        original_exception (Exception): 元の例外
        message (str): エラーメッセージ
    """
    def __init__(self, filepath, original_exception=None):
        self.filepath = filepath
        self.original_exception = original_exception
        self.message = f"Cannot read CSV file: {filepath}"
        if original_exception:
            self.message += f" (Reason: {original_exception})"
        super().__init__(self.message)

    def __str__(self):
        return self.message


def load_csv_file(csv_path, delimiter=',', loader = 'np', fillna=True, fillna_value=0):
    """
    CSVファイルを読み込みます。
    Args:
        csv_path (str): CSVファイルのパス
        delimiter (str): CSVファイルの区切り文字（デフォルト: ','）
        loader (str): 'np'または'pd'を指定（デフォルト: 'np'）

    Returns:
        data (np.ndarray または pd.DataFrame): 読み込んだCSVファイルのデータ

    Raises:
        CSVFileReadError: CSVファイルの読み込みに失敗した場合に発生します
        InvalidFileTypeError: ファイルがCSVファイルでない場合に発生します

    Example:
        data = load_csv_file('data.csv', delimiter=',', loader='np')
        data = load_csv_file('data.csv', delimiter=',', loader='pd')
    """
    def _load_csv_with_numpy(csv_path, delimiter, fillna=True ,fillna_value=0):
        """
        numpyでCSVファイルを読み込みます。
        Args:
            csv_path (str): CSVファイルのパス
            delimiter (str): CSVファイルの区切り文字（デフォルト: ','）

        Returns:
            data (np.ndarray): 読み込んだCSVファイルのデータ
        """
        args = {
            'delimiter': delimiter,
            'skip_header': 1,
            }
        if fillna:
            args['filling_values'] = fillna_value
        
        try:
            data = np.genfromtxt(csv_path, **args)
            return data
        except Exception as e1:
            try:
                args.pop('skip_header', None)
                data = np.genfromtxt(csv_path, **args)
                return data
            except Exception as e2:
                 raise CSVFileReadError(csv_path, e2)

    def _load_csv_with_pandas(csv_path, delimiter):
        """
        pandasでCSVファイルを読み込みます。
        Args:
            csv_path (str): CSVファイルのパス
            delimiter (str): CSVファイルの区切り文字（デフォルト: ','）

        Returns:
            data (pd.DataFrame): 読み込んだCSVファイルのデータ
        """
        
        try:
            data = pd.read_csv(csv_path, delimiter=delimiter, skiprows=1)
            return data
        except Exception as e1:
            try:
                data = pd.read_csv(csv_path, delimiter=delimiter)
                return data
            except Exception as e2:
                 raise CSVFileReadError(csv_path, e2)

    csv_path = validate_csv_path(csv_path)

    if loader in ['np', 'numpy']:
        data = _load_csv_with_numpy(csv_path, delimiter, fillna=fillna, fillna_value=fillna_value)    
        if data.shape == (0,):
            raise CSVFileReadError(csv_path, "Empty Array")
        elif data.size  == 0:
            raise CSVFileReadError(csv_path, "Only NaN values found")
        
    elif loader in ['pd', 'pandas']:
        data = _load_csv_with_pandas(csv_path, delimiter)
        if data.empty:
            raise CSVFileReadError(csv_path, "Empty DataFrame")
        elif data.isnull().all().all():
            raise CSVFileReadError(csv_path, "Only NaN values found")
    else:
        raise ValueError("Invalid loader specified. Use 'np' or 'pd'")
    
    return data


def validate_csv_path(csv_path):
    """ 
    CSVファイルのパスを検証します。
    Args:
        csv_path (str): CSVファイルのパス

    Returns:
        csv_path (str): 検証済みのCSVファイルのパス

    Raises:
        InvalidFileTypeError: ファイルがCSVファイルでない場合に発生します
        FileNotFoundError: ファイルが見つからない場合に発生します
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
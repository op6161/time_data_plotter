import os
import numpy as np
import pandas as pd
import logging
import sys

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
        self.message = f"CSVファイル読みに失敗しました: {filepath}"
        if original_exception:
            self.message += f" (理由: {original_exception})"
        super().__init__(self.message)

    def __str__(self):
        return self.message


def load_csv_file(csv_path, delimiter: str =',', loader: str = 'np', fillna=True, fillna_value=0):
    """
    CSVファイルを読み込みます。
    Args:
        delimiter (str): CSVファイルの区切り文字（デフォルト: ','）
        loader (str): 'np'または'pd'を指定（デフォルト: 'np'）

    Returns:
        data (np.ndarray または pd.DataFrame): 読み込んだCSVファイルのデータ

    Raises:
        CSVFileReadError: CSVファイルの読み込みに失敗した場合に発生します
        InvalidFileTypeError: ファイルがCSVファイルでない場合に発生します

    Example:
        data = load_csv_file('data.csv', delimiter=',', loader='np')
    """
    def _load_csv_with_numpy(csv_path, delimiter, fillna=True ,fillna_value=0):
        """
        numpyでCSVファイルを読み込みます。
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
        
        # headerがない場合は、skip_headerを削除して再度読み込み
        except Exception as e1:
            try:
                args.pop('skip_header', None)
                data = np.genfromtxt(csv_path, **args)
                return data
            
            # それでも読み込みに失敗した場合は、CSVFileReadErrorを発生
            except Exception as e2:
                 raise CSVFileReadError(csv_path, e2)

    def _load_csv_with_pandas(csv_path, delimiter):
        """
        pandasでCSVファイルを読み込みます。
        """
        try:
            data = pd.read_csv(csv_path, delimiter=delimiter, skiprows=1)
            return data
        
        # headerがない場合は、skip_headerを削除して再度読み込み
        except Exception as e1:
            try:
                data = pd.read_csv(csv_path, delimiter=delimiter)
                return data
            # それでも読み込みに失敗した場合は、CSVFileReadErrorを発生
            except Exception as e2:
                 raise CSVFileReadError(csv_path, e2)

    csv_path = validate_csv_path(csv_path)

    # numpyをloaderに指定した場合
    if loader in ['np', 'numpy']:
        data = _load_csv_with_numpy(csv_path, delimiter, fillna=fillna, fillna_value=fillna_value)    
        if data.shape == (0,):
            logging.error(f"CSVファイルが空です：{csv_path}")
            raise CSVFileReadError(csv_path, "arrayが空です")
        elif data.size  == 0:
            logging.error(f"Nan値のみが含まれています：{csv_path}")
            raise CSVFileReadError(csv_path, "Nan値のみが含まれています")
    # pandasをloaderに指定した場
    elif loader in ['pd', 'pandas']:
        data = _load_csv_with_pandas(csv_path, delimiter)
        if data.empty:
            logging.error(f"CSVファイルが空です：{csv_path}")    
            raise CSVFileReadError(csv_path, "DataFrameが空です")
        elif data.isnull().all().all():
            logging.error(f"Nan値のみが含まれています：{csv_path}")
            raise CSVFileReadError(csv_path, "Nan値のみが含まれています")
    else:
        logging.error(f"loaderは'np'または'pd'を指定してください。: loader: {loader}")
        raise ValueError("loaderは'np'または'pd'を指定してください。")

    logging.info(f"データロード完了、CSVファイルのパス：{csv_path}")
    return data, load_header(csv_path, delimiter=delimiter)


def load_header(csv_path, delimiter: str = ','):
    """
    現在ロードされているデータのヘッダー情報を返します。

    Args:

    Returns:
        str: 要求された形式のヘッダー文字列

    Raises:
        ValueError: データがロードされていない場合に発生します。
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        header_line = f.readline().strip()
    header = list(header_line.split(delimiter))
    header = ','.join(header)
    return header


def validate_csv_path(csv_path):
    """ 
    CSVファイルのパスを検証します。

    Raises:
        InvalidFileTypeError: ファイルがCSVファイルでない場合に発生します
        FileNotFoundError: ファイルが見つからない場合に発生します
    """
    if not csv_path.endswith('.csv'):
        logging.error(f"CSVファイルではありません。: {csv_path}")
        raise InvalidFileTypeError("CSVファイルではありません。拡張子を確認してください。")
    if not os.path.exists(csv_path):
        logging.error(f"ファイルが存在しません。: {csv_path}")
        raise FileNotFoundError(f"ファイルが存在しません。: {csv_path}") 
    return csv_path

if __name__ == "__main__":
    # Example usage
    example_file_path = '../sample_waves.csv'
    example_file_path = validate_csv_path(example_file_path)
    data = load_csv_file(example_file_path, delimiter=',', loader='np')

    print(data)
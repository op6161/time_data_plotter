import os
import numpy as np
import pandas as pd


class FileTypeError(Exception):
    """CSV파일이 아닐 경우"""
    pass

class CSVFileReadError(Exception):
    """CSV파일을 읽어오지 못할 경우"""
    pass


def csv_file_load(file_path, delimiter=',', how = 'np'):
    """
    CSV파일을 읽어온다.
    :param file_path: CSV파일 경로
    :param delimiter: CSV파일 구분자
    :param how: np, pd
    :return: CSV파일 데이터
    """
    
    def csv_file_load_np(file_path, delimiter=','):
        """
        numpy로 CSV파일을 읽어온다.
        :param file_path: CSV파일 경로
        :param delimiter: CSV파일 구분자
        :return: CSV파일 데이터
        """
        data = None
        try:    
            data = np.genfromtxt(file_path, delimiter=delimiter, skip_header=True, filling_values=0)
        except Exception as e:
            print(e)
        return data

    def csv_file_load_pd(file_path, delimiter=','):
        """
        pandas로 CSV파일을 읽어온다.
        :param file_path: CSV파일 경로
        :param delimiter: CSV파일 구분자
        :return: CSV파일 데이터
        """
        data = None
        try:    
            data = pd.read_csv(file_path, delimiter=delimiter)
        except Exception as e:
            print(e)
        return data

    if path_error_check(file_path):
        pass

    if how.startswith('np') or how.endswith('np'):
        try:
            data = csv_file_load_np(file_path, delimiter)
        except Exception as e:
            print(e)
            print("load error for pandas")
        

    if how.startswith('pd') or how.endswith('pd'):
        try:
            data = csv_file_load_pd(file_path)
        except Exception as e:
            print(e)
            print("load error for pandas")

    if data is None:
        raise CSVFileReadError("Error reading CSV file: {}".format(file_path))
    
    return data


def path_error_check(file_path):
    """
    파일의 경로를 체크한다
    """
    if not file_path.endswith('.csv'):
        raise FileTypeError("File must be a CSV file.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path
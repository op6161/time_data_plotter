import numpy as np
from .csv_module import load_csv_file
import os
from typing import Dict, Any, Optional

class CSVColumnSummer:
    """
    このクラスはCSVファイルからデータをロードし、各行ごとに選択された列の値の合計を新しい列として追加し、
    追加されたデータを新しいCSVファイルとして保存する機能を提供します。
    Attributes:
        timestamps (np.ndarray): CSVファイルのタイムスタンプデータ配列。
        data (np.ndarray): CSVファイルのタイムデータを除いたその他のデータ配列。
        csv_header (str): CSVファイルのヘッダー行。
        num_columns (int): データの列数（タイムデータを除く）。
        num_data (int): データの行数。
        combined_data (np.ndarray): 新しく生成された列を含む全データ配列。
        added_column (np.ndarray): 新しく生成された単一列データ配列。
        added_header (str): 新しく生成された単一列のヘッダー値。

    Methods:
        set_config(**kwargs): CSVColumnSummerクラスのオプションを設定します。
            delimiter: str : CSVファイルの区切り文字 デフォルト: ','
            fmt: str : 保存時のCSVファイルのフォーマット デフォルト: '%.8g'
        show_config(): 現在設定されているオプションを表示します。
        add_sum_column(sum_target=None, timestamp=True): 選択した列の合計を新しい列として追加します。
        save_data(save_path="./added_data.csv", header="AddedData", sum_target=None, timestamp=True): 生成された列を含むデータを新しいCSVファイルとして保存します。
        get_data(): ロードされたデータを返します。
        get_header(): ロードされたデータのヘッダーを返します。
    """

    # - delimiter: str : CSVファイルの区切り文字 デフォルト: ','
    # - fmt: str : 保存するCSVファイルのフォーマット設定　ディフォルト：'%8g'
    # - loader: str : データロード方法を指定、'np' または 'pd'
    # - added_header: str : 新しく生成されるデータ列のヘッダー名
    DEFAULT_OPTIONS = {
        'delimiter': ',',
        'fmt': '%8g',
        'loader': 'np',
        'added_header': 'AddedData',
    }

    def __init__(self, path: str = None, options: Optional[Dict[str, Any]] = None):
        """
        Args:
        options: Dict[str, Any] : オプションの辞書
        例:
        path: str : データを含むCSVファイルのパス
        delimiter: str : CSVファイルで使用される区切り文字（デフォルト: ','）
        
        """    
        # クラス初期化
        self.timestamps: Optional[np.ndarray] = None
        self.data: Optional[np.ndarray] = None
        self.csv_header: Optional[str] = None
        self.num_columns: Optional[int] = None
        self.num_raws: Optional[int] = None
        
        self.combined_data = None
        self.added_column = None

        self.process_options = self.DEFAULT_OPTIONS.copy()

        if options:
            # optionsが指定されている場合は、オプションを更新
            self.set_options(**options)
        
        print("CSVColumnSummer initialized") # txt log
        print("CSVColumnSummer.options:", self.options) # txt log

        if path is not None:
            self.load_data(path)
    
    def set_options(self, **kwargs):
        """
        クラスのオプションを設定します。

        Args:
            **kwargs: オプションのキーワード引数
                delimiter (str): CSVファイルの区切り文字 デフォルト: ','
                fmt (str): 保存時のCSVファイルのフォーマット デフォルト: '%.8g'
                loader (str): 'np'または'pd'を指定（デフォルト: 'np'）
                added_header (str): 新しく生成された列のヘッダー名（デフォルト: 'AddedData'）
        """
        if not kwargs:
            raise ValueError("オプションを指定してください。")
        
        for key, value in kwargs.items():
            if key in self.process_options:
                self.process_options[key] = value
            else:
                raise ValueError(f"{key}はオプションに存在しません。allowed_options：　{self.process_options.keys()}")
            
        print(f"options updated: {self.process_options}")


    def load_data(self, path) -> None:
        """
        指定したパスのCSVファイルをロードし、クラス内部の変数にデータを保存します。
        """
        loader = self.process_options.get('loader', 'np')
        delimiter = self.process_options.get('delimiter', ',')
        
        data, header_line = load_csv_file(path, delimiter=delimiter,loader=loader)
        num_columns = len(data[0])

        self.timestamps = data[:,0]
        self.data = data[:,1:]
        self.csv_header = header_line
        self.num_columns = num_columns-1
        self.num_data = len(self.timestamps)


        print(f"CSVColumnSummer.data Loaded from {path}") # txt log
        print(f"CSVColumnSummer.data Number of columns: {self.num_columns}, (without timestamp)") # txt log
        print(f"CSVColumnSummer.data Number of lows: {self.num_data}") # txt log

        self.combined_data = self._get_combined_data()

    def _data_check(self) -> None:
        """
        loadが1回以上実行され、dataが生成されているかを確認します。

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        if self.data is None or self.timestamps is None:
            raise ValueError("データがロードされていません。loadメソッドを実行してください。")

    def show_config(self):
        """
        クラス内の現在設定されている保存/ロードオプションを表示します。
        """
        print("CSVColumnSummer Configuration:")
        for key, value in self.options.items():
            print(f"{key}: {value}")
        print("==="*10) # txt log


    def _get_combined_data(self, sum_target=None):
        """
        各行ごとにデータの選択された列の値を合計し、新しい列を生成します。
        新しく生成された列は既存データの最後の列に追加されます。
        結果にタイムスタンプデータを含めるかどうかを選択できます。
        """        
        data = self.data

        # 合計する列のインデックスが指定されていない場合は全ての列を合計
        if sum_target is None:
            sum_row = data.sum(axis=1)
        # 合計する列のインデックスが指定されている場合はその列のみを合計
        else:
            selected_data = data[:, sum_target]
            sum_row = selected_data.sum(axis=1)
        
        # 1次元配列を2次元に変換
        sum_row = sum_row.reshape(-1, 1)  
        # 新しいテータと既存データを結合
        combined_data = np.hstack((data, sum_row))
        return combined_data

    def save_data(self, 
                save_path="./added_data.csv", 
                header='new_data'): 
        """
        新しく生成されたデータと結合データをCSVファイルとして保存します。
        """
        self._data_check()
        save_path = save_path_check(save_path)
        combined_data = self.combined_data
        
        header = self.csv_header + ',' +  header
        self.added_header = header

        np.savetxt(save_path, combined_data, delimiter=',',  header=self.added_header, fmt=self.process_options['fmt'])
        print(f"生成されたデータが {save_path}に保存されました。 新しい列データのheader: {header}")
        return combined_data, header
    
    def get_data(self, combined=True):
        """
        ロードされたデータとタイムスタンプを返します。

        Args:
            combined (bool): Trueの場合、選択した列の合計が追加されたデータを返します。
                             Falseの場合、元のデータのみを返します。

        Returns:
            tuple: (x_data, y_data)
                x_data (np.ndarray): 要求された形式のデータ配列
                y_data (np.ndarray): タイムスタンプ配列

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        self._data_check()

        if combined:
            x_data = self.combined_data
        else:
            x_data = self.data
        y_data = self.timestamps
        return x_data, y_data


def save_path_check(path):
    """
    指定されたパスをsys.pathに追加します。
    """
    save_dir = os.path.dirname(path)
    # pathのディレクトリがない場合、ディレクトリを作成
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"Directory created: {save_dir}")  # txt log
    return path


if __name__ == "__main__":
    # Example usage
    example_file_path = '../sample_waves.csv'
    summer = CSVColumnSummer()
    summer.set_config( 
        fmt = '%.8g', 
        fillna = False, 
        fillna_value=0)
    summer.load(example_file_path)
    summer.save_combined('../test_result.csv')
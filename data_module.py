import numpy as np
from csv_module import load_csv_file
import os

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
            fillna: bool : ロード時にnan値を置換するかどうか デフォルト: True
            fillna_value: int : ロード時にnan値を置換する値 デフォルト: 0
            fmt: str : 保存時のCSVファイルのフォーマット デフォルト: '%.8g'
        show_config(): 現在設定されているオプションを表示します。
        add_sum_column(sum_target=None, timestamp=True): 選択した列の合計を新しい列として追加します。
        save_data(save_path="./added_data.csv", header="AddedData", sum_target=None, timestamp=True): 生成された列を含むデータを新しいCSVファイルとして保存します。
        get_data(): ロードされたデータを返します。
        get_header(): ロードされたデータのヘッダーを返します。
    """
    def __init__(self, path= None, delimiter=',',fmt='%8g',fillna=True, fillna_value=0):
        """
        path: str : データを含むCSVファイルのパス
        delimiter: str : CSVファイルで使用される区切り文字（デフォルト: ','）
        """    
        # クラス初期化
        self.timestamps = None
        self.data = None
        self.csv_header = None
        self.num_columns = None
        self.num_data = None
        
        self.combined_data = None
        self.added_column = None
        self.added_header = "AddedData"

        # ディフォルトのオプション
        self.options = {
            'delimiter': delimiter,
            'fmt': fmt,
            'fillna': fillna,
            'fillna_value': fillna_value,
        }
        self.__options_load = {
            'delimiter': delimiter,
            'fillna': fillna,
            'fillna_value':fillna_value,
        }
        self.__options_save = {
            'fmt': fmt,
        }
        
        print("CSVColumnSummer initialized") # txt log
        print("CSVColumnSummer.options:", self.options) # txt log

        if path is not None:
            self.load(path)
    
    def load(self, path, no_header =False):
        """
        指定したパスのCSVファイルをロードし、クラス内部の変数にデータを保存します。

        Args:
            path (str): ロードするCSVファイルのパス
            no_header (bool): Trueの場合はヘッダーを読み込まず、Falseの場合は最初の行をヘッダーとして読み込みます

        動作:
            - load_csv_file関数を利用してデータを読み込みます。
            - データの最初の列をtimestampsとして、残りをdataとして分離します。
            - ヘッダーが必要な場合はファイルの最初の行を読み込みcsv_headerに保存します。
            - 列数と行数をそれぞれnum_columns, num_dataに保存します。
        """

        data = load_csv_file(path, **self.__options_load)
        num_columns = len(data[0])

        if not no_header:
            #　データがヘッダーを含まないため、ヘッダーを別途読み込む
            with open(path, 'r', encoding='utf-8') as f:
                header_line = f.readline().strip()

        self.timestamps = data[:,0]
        self.data = data[:,1:]
        self.csv_header = header_line
        self.num_columns = num_columns-1
        self.num_data = len(self.timestamps)

        print(f"CSVColumnSummer.data Loaded from {path}") # txt log
        print(f"CSVColumnSummer.data Number of columns: {self.num_columns}, (without timestamp)") # txt log
        print(f"CSVColumnSummer.data Number of lows: {self.num_data}") # txt log

    
    def __data_check(self):
        """
        loadが1回以上実行され、dataが生成されているかを確認します。

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Please call 'load('file_path')' before accessing the data.")

    def set_config(self,**kwargs):
        """
        クラス内の演算オプションを設定します。

        Args:
            delimiter (str): CSVファイルの区切り文字 デフォルト: ','
            fillna (bool): ロード時にnan値を置換するかどうか デフォルト: True
            fillna_value (int): ロード時にnan値を置換する値 デフォルト: 0
            fmt (str): 保存時のCSVファイルのフォーマット デフォルト: '%.8g'

        Raises:
            ValueError: 定義されていないオプションを設定した場合に発生します。
        """
        allowed_options = self.options.keys()

        for key, value in kwargs.items():
            if key in allowed_options:
                if key in self.options:
                    self.options[key] = value

                if key in self.__options_load:
                    self.__options_load[key] = value
                if key in self.__options_save:
                    self.__options_save[key] = value
                
            else:
                raise ValueError(f"Invalid option: {key}. Allowed options are: {allowed_options}")
  
        print("data_module set config completed") # txt log
        self.show_config() # txt log

    def show_config(self):
        """
        クラス内の現在設定されている保存/ロードオプションを表示します。
        """
        print("CSVColumnSummer Configuration:")
        for key, value in self.options.items():
            print(f"{key}: {value}")
        print("===")

    def add_sum_column(self, sum_target=None, timestamp=True):
        """
        各行ごとにデータの選択された列の値を合計し、新しい列を生成します。
        新しく生成された列は既存データの最後の列に追加されます。
        結果にタイムスタンプデータを含めるかどうかを選択できます。

        Args:
            sum_target (list): 合計する列のインデックスリスト デフォルト: None（全ての列）
            timestamp (bool): 結果にタイムスタンプを含めるかどうか デフォルト: True
        
        Returns:
            np.ndarray : 既存データに新しい列が追加された配列

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """        
        self.__data_check()
        data_arr = self.data
        if timestamp:
            data_arr = np.hstack((self.timestamps.reshape(-1, 1), data_arr))

        if sum_target is None:
            row_sum = data_arr.sum(axis=1)
        else:
            selected_data = data_arr[:, sum_target]
            row_sum = selected_data.sum(axis=1)
        
        row_sum = row_sum.reshape(-1, 1)  # Reshape to make it a column vector
        combined_data = np.hstack((data_arr,row_sum))
        return combined_data

    
    def save_combined(self, 
                      save_path="./added_data.csv", 
                      header='new_data', 
                      sum_target = None,
                      timestamps=True,): 
        """
        新しく生成されたデータと結合データをCSVファイルとして保存します。

        Args:
            save_path (str): 保存するファイルのパス
            header (str): 生成された列のヘッダー名
            sum_target (list): 合計する列のインデックスリスト デフォルト: None（全ての列）
            timestamps (bool): 結果にタイムスタンプを含めるかどうか デフォルト: True

        Return:
            tuple: (combined_data, header)
                combined_data (np.ndarray): 既存データに新しい列が追加された配列
                header (str): 保存されたCSVファイルのヘッダー

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        self.__data_check()
        save_path = save_path_check(save_path)
        combined_data = self.add_sum_column(sum_target, timestamp=timestamps)
        
        header = self.csv_header + ',' +  header
        self.added_header = header

        np.savetxt(save_path, combined_data, delimiter=',',  header=self.added_header, **self.__options_save)
        print(f"CSVColumnSummer.combined_data saved to {save_path} with header: {header}") # txt log
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
        self.__data_check()

        if combined:
            x_data = self.add_sum_column(timestamp=False)
        else:
            x_data = self.data
        y_data = self.timestamps
        return x_data, y_data

    def get_header(self, combined=True):
        """
        現在ロードされているデータのヘッダー情報を返します。

        Args:
            combined (bool): Trueの場合、既存のCSVヘッダーと追加された列のヘッダー（added_header）を結合して返します。
                             Falseの場合、既存のCSVヘッダーのみを返します。

        Returns:
            str: 要求された形式のヘッダー文字列

        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        self.__data_check()
        if combined:
            header = self.csv_header+','+self.added_header
        else:
            header = self.csv_header
        return header


def save_path_check(path):
    """
    指定されたパスをsys.pathに追加します。

    Args:
        path (str): 追加するパス

    Returns:
        None
    """
    save_dir = os.path.dirname(path)
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
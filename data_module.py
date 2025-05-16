import numpy as np
from csv_module import load_csv_file

class CSVColumnSummer:
    """
    이 클래스는 CSV파일에서 데이터를 로드하고, 각 행별 선택된 열들의 값 합계를 새로운 열에 추가하며,
    추가된 데이터를 새로운 CSV파일로 저장하는 기능을 제공합니다.
    Attributes:
        timestamps (np.ndarray): CSV파일의 timestamps data Array.
        data (np.ndarray): CSV파일의 time data를 제외한 나머지 data Array.
        csv_header (str): CSV파일의 헤더 라인.
        num_columns (int): 데이터의 열의 개수.(time data 제외)
        num_data (int): 데이터 행의 개수.
        combined_data (np.ndarray): 새롭게 생성된 열을 포함한 전체 데이터 Array.
        added_column (np.ndarray): 새롭게 생성된 단일 열 데이터 Array.
        added_header (str): 새롭게 생성된 단일 열의 헤더 값.

    Methods:
        set_config(**kwargs): CSVColumnSummer Class의 옵션을 설정합니다.
            delimiter: str : CSV파일의 구분자 default: ','
            fillna: bool : load시 nan값을 대체할지 여부 default: True
            fillna_value: int : load시 nan값을 대체할 값 default: 0
            fmt: str : save시 CSV파일의 포맷 default: '%.8g'
            comments: str : save시 CSV파일의 주석 default: '#'
        show_config(): 현재 설정된 옵션을 출력합니다.
        add_sum_column(sum_target=None, timestamp=True): 선택된 열의 합계를 새로운 열로 추가합니다.
        save_data(save_path="./added_data.csv", header="AddedData", sum_target=None, timestamp=True): 생성된 열을 포함한 데이터를 새로운 CSV파일로 저장합니다.
        get_data(): load된 데이터를 내보낸다.
        get_header(): load된 데이터의 header를 내보낸다
    """
    def __init__(self, path= None, delimiter=',',fmt='%8g',fillna=True, fillna_value=0, comments='#'):
        """
        path: str : path to the CSV file containing the data
        delimiter: str : delimiter used in the CSV file default: ','
        """    
        # 객체 내에서 사용될 변수 정의
        self.timestamps = None
        self.data = None
        self.csv_header = None
        self.num_columns = None
        self.num_data = None
        
        self.combined_data = None
        self.added_column = None
        self.added_header = "AddedData"

        # 기본 옵션
        self.options = {
            'delimiter': delimiter,
            'fmt': fmt,
            'fillna': fillna,
            'fillna_value': fillna_value,
            'comments': comments
        }
        self.__options_load = {
            'delimiter': delimiter,
            'fillna': fillna,
            'fillna_value':fillna_value
        }
        self.__options_save = {
            'delimiter': delimiter,
            'fmt': fmt,
            'comments': comments
        }
        
        # 요청 시 즉시 CSV파일 로드
        if path is not None:
            self.load(path)
    
    def load(self, path, no_header =False):
        """
        지정한 경로의 CSV 파일을 로드하여 클래스 내부 변수에 데이터를 저장합니다.

        Args:
            path (str): 로드할 CSV 파일 경로
            no_header (bool): True일 경우 헤더를 읽지 않음, False일 경우 첫 줄을 헤더로 읽음

        동작:
            - load_csv_file 함수를 이용해 데이터를 불러옵니다.
            - 데이터의 첫 번째 열은 timestamps로, 나머지는 data로 분리합니다.
            - 헤더가 필요하면 파일의 첫 줄을 읽어 csv_header에 저장합니다.
            - 열과 행의 개수를 각각 num_columns, num_data에 저장합니다.
        """
        # csv로드
        data = load_csv_file(path, **self.__options_load)
        # 객체에서 사용할 data 추출
        num_columns = len(data[0])

        if not no_header:
            # 데이터가 header를 포함하지 않기 때문에, header를 따로 읽어오기
            with open(path, 'r', encoding='utf-8') as f:
                header_line = f.readline().strip()

        self.timestamps = data[:,0]
        self.data = data[:,1:]
        self.csv_header = header_line
        self.num_columns = num_columns-1
        self.num_data = len(self.timestamps)
        # print(f"Loaded data shape: {self.data.shape} (타임스탬프 제외)") 
    
    def __data_check(self):
        """
        load가 1회이상 실행되어 data가 생성되었는지 확인

        Raises:
            ValueError: 데이터가 로드되지 않은 경우 예외를 발생시킵니다.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Please call 'load('file_path')' before accessing the data.")

    def set_config(self,**kwargs):
        """
        클래스 내의 연산 옵션을 설정한다.
        Args:
            delimiter(str): CSV파일의 구분자 default: ','    
            fillna(bool): load시 nan값을 대체할지 여부 default: True    
            fillna_value(int): load시 nan값을 대체할 값 default: 0
            fmt(str): save시 CSV파일의 포맷 default: '%.8g'
            comments(str): save시 CSV파일의 주석 default: '#'

        Raises:
            ValueError: 정의되지 않은 옵션을 설정한 겨웅, 예외를 발생시킵니다.
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
        ## debug
        # print("set config completed:")
        # self.show_config()

    def show_config(self):
        """
        클래스 내의 현재 설정된 저장/로드 옵션을 출력한다.
        """
        print("CSVColumnSummer Configuration:")
        for key, value in self.options.items():
            print(f"{key}: {value}")
        print("===")

    def add_sum_column(self, sum_target=None, timestamp=True):
        """
        행 별로 데이터의 선택된 열의 값을 합하여 새로운 열을 생성한다.
        새로 생성된 열은 기존 데이터의 마지막 열에 추가된다.
        결과값에 타임스탬프 데이터를 포함할지 여부를 선택할 수 있다.

        Args:
            sum_target(list): 값을 합할 열의 인덱스 리스트 default:None(전체)
            timestamp(bool): 결과값에 timestamp를 포함할지 여부 default:True
        
        Returns:
            np.ndarray : 기존 데이터에 새로운 열이 추가된 array

        Raises:
            ValueError: 데이터가 로드되지 않은 경우 예외를 발생시킵니다.
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
                      header=None, 
                      sum_target = None,
                      timestamps=True,): 
        """
        새로 생성된 데이터와 결합된 데이터를 CSV 파일로 저장한다
        Args:
            save_path: str : 저장할 파일 경로
            title: str : 생성된 열의 헤더 이름
            sum_target: list : 값을 합할 열의 인덱스 리스트 default:None(전체)
            timestamps: bool : 결과값에 timestamp를 포함할지 여부 default:True

        Return:
            ndarray
            str

        Raises:
            ValueError: 데이터가 로드되지 않은 경우 예외를 발생시킵니다.
        """
        self.__data_check()
        combined_data = self.add_sum_column(sum_target, timestamp=timestamps)
        header = self.csv_header + ',' +  header
        if header is not None:
            self.added_header = header

        np.savetxt(save_path, combined_data, header=self.added_header, **self.__options_save)
        print(f"Data saved to {save_path} with header: {header}")
        return combined_data, header
    
    def get_data(self, combined=True):
        """
        로드된 데이터와 타임스탬프를 반환합니다.

        Args:
            combined (bool): True일 경우, 선택된 열의 합계가 추가된 데이터를 반환합니다.
                             False일 경우, 원본 데이터만 반환합니다.

        Returns:
            tuple: (x_data, y_data)
                x_data (np.ndarray): 요청한 형태의 데이터 배열
                y_data (np.ndarray): 타임스탬프 배열

        Raises:
            ValueError: 데이터가 로드되지 않은 경우 예외를 발생시킵니다.
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
        현재 로드된 데이터의 헤더 정보를 반환합니다.

        Args:
            combined (bool): True일 경우, 기존 CSV 헤더와 추가된 열의 헤더(added_header)를 결합하여 반환합니다.
                             False일 경우, 기존 CSV 헤더만 반환합니다.

        Returns:
            str: 요청한 형태의 헤더 문자열

        Raises:
            ValueError: 데이터가 로드되지 않은 경우 예외를 발생시킵니다.
        """
        self.__data_check()
        if combined:
            header = self.csv_header+','+self.added_header
        else:
            header = self.csv_header
        return header

if __name__ == "__main__":
    # Example usage
    example_file_path = '../sample_waves.csv'
    summer = CSVColumnSummer()
    summer.set_config( 
        comments = '#', 
        fmt = '%.8g', 
        fillna = False, 
        fillna_value=0)
    summer.load(example_file_path)
    summer.save_combined('../test_result.csv')
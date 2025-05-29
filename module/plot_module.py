import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import logging
import sys

class Plotter:
    """
    時系列データを可視化し、さまざまな属性を設定できるクラスです。
    x_dataは2次元配列で、各列が異なる時系列データ（例：wave1, wave2, ...）を表します。
    y_dataは1次元配列で、時系列データのタイムスタンプを表します。
    y_dataを基準にx_dataを縦に並べてグラフとして出力します。
    
    例えばx_dataが [wave1, wave2, wave3, wave4]のような場合、

    [wave1のグラフ]
    [wave2のグラフ]
    [wave3のグラフ]
    [wave4のグラフ]
    の順で出力されます。
    
    Attributes:
        axes (list): サブプロットのAxesオブジェクトのリスト
        fig (matplotlib.figure.Figure): プロット用のFigureオブジェクト
        x_data (np.ndarray): 各列が異なるデータ系列（例：wave1, wave2, ...）を表す2次元配列
        y_data (np.ndarray): x_dataに対応するx軸データ（時系列の場合はタイムスタンプ）
        labels (list or dict): 各プロットのラベルリストまたは辞書
            例：labels = {0: 'wave1', 5: 'wave6', -1: 'wave50'} 
            * セットしないcolumnは、順番にあわせて自動的に wave1, wave2, ...とラベル付けされます。
            例：labels = ['wave1', 'wave2', ..., -1: 'wave50']
            * 入力がリストの場合はリストの長さはx_dataの列数と一致する必要があります。
        title (str): プロットのタイトル
        xlabel (str): X軸のラベル
        
    Methods:
        set_plot(x_data, y_data, labels=None, title='Plot', xlabel='Time'):
            指定したデータとラベルでプロットを設定する
        draw_plot():
            プロットを表示する
        save_plot(name, fmt='.png'):
            指定した名前と形式でプロットをファイルに保存する
    """
    def __init__(self, x_data=None, y_data=None, labels=None, title='Plot', xlabel='Time'):
        
        self.axes = None
        self.fig = None

        self.x_data = x_data
        self.y_data = y_data
        self.labels = labels
        self.title = title
        self.xlabel = xlabel
        logging.info("クラスPlotterが初期化されました。") # txt log
        
        if x_data is not None and y_data is not None:
            self.set_plot(x_data,y_data,labels,title,xlabel)
        
        

    def set_plot(self, x_data, y_data, labels=None, title='Plot', xlabel='Time'):
        """
        指定したデータとラベルでプロットを設定します。
        Args:
            x_data (np.ndarray): プロットのx軸データ。
            y_data (np.ndarray): プロットのy軸データ。
            labels (list): 各プロットのラベルリスト。
            title (str): プロットのタイトル。
            xlabel (str): x軸のラベル。
        
        Raises:
            ValueError: x_dataは2次元配列、y_dataは1次元配列である必要があります。
            ValueError: x_dataの行数とy_dataの長さが一致していません。
        """
        def _plot_single_subplot(gs, idx, fig, x_data, y_data, label, color, sharex=None):
            """
            指定したデータとラベルで単一のサブプロットを作成します。
            引数:
                gs (matplotlib.gridspec.GridSpec): Figure用のGridSpecオブジェクト。
                idx (int): サブプロットのインデックス。
                fig (matplotlib.figure.Figure): プロット用のFigureオブジェクト。
                x_data (np.ndarray): プロットのx軸データ。
                y_data (np.ndarray): プロットのy軸データ。
                label (str): プロットのラベル。
                color (str): 線の色。
                sharex (matplotlib.axes.Axes, optional): x軸を共有するAxesオブジェクト。デフォルトはNone。
            """
            ax = fig.add_subplot(gs[idx], sharex=sharex)
            ax.plot(x_data, y_data, color=color)
            ax.tick_params(axis='x', direction='in', length=4, width=1, top=True)
            ax.tick_params(axis='y', direction='in', labelsize=8)
            ax.legend([label], loc='center left', bbox_to_anchor=(0.995, 0.885), fontsize=8)
            ax.margins(y=0.2)
            # print(f"{label} plot created.")
            return ax

        # 入力データの検証
        if x_data.ndim != 2 or y_data.ndim != 1:
            logging.error("x_dataは２次元配列で、y_dataは１次元配列である必要があります。")
            raise ValueError("x_data must be a 2D array and y_data must be a 1D array.")
        if x_data.shape[0] != y_data.shape[0]:
            logging.error("x_dataとy_dataの長さが一致していません。")
            raise ValueError("The number of rows in x_data must match the length of y_data.")
        
        # 既存のプロットがあれば閉じる
        if self.fig is not None:
            self.close_plot()

        cols = x_data.shape[1]
        fig = plt.figure(figsize=(10, cols))
        fig.suptitle(title)
        fig.canvas.manager.set_window_title(title)
        fig.supxlabel(xlabel)
        gs = gridspec.GridSpec(cols, 1, height_ratios=[0.8] * cols, hspace=0)

        axes = []
        color_map = plt.get_cmap('tab10')
        color_list = [color_map(i % color_map.N) for i in range(cols)]

        if labels is None:
            labels = [f"wave{i+1}" for i in range(cols)]
            
        elif type(labels) is dict:
            backup_labels = labels.copy()
            labels = [f"wave{i+1}" for i in range(cols)]
            for key, value in backup_labels.items():
                labels[key] = value
                
        elif type(labels) is list:
            if len(labels) != cols:
                logging.error("labels数とx_dataの列数が一致していません。")
                raise ValueError("The length of labels must match the number of columns in x_data. Use a dictionary to specify labels for specific columns.")

        for i in range(cols):
            sharex = axes[0] if i > 0 else None
            label = labels[i]
            color = color_list[i]

            ax = _plot_single_subplot(gs, i, fig, y_data, x_data[:, i], label, color, sharex)
            axes.append(ax)
        
        self.fig  = fig
        self.axes = axes

        self.x_data = x_data
        self.y_data = y_data
        self.labels = labels
        self.title = title
        self.xlabel = xlabel

        logging.info("プロットが設定されました。")
        logging.info(f"x_data shape: {x_data.shape}, y_data shape: {y_data.shape}")
        logging.info(f"labels: {labels}, title: {title}, xlabel: {xlabel}")

        return fig, axes
    

    def __data_check(self) -> None:
        """
        データがロードされているかを確認し、ロードされていない場合は例外を発生させます。
        Raises:
            ValueError: データがロードされていない場合に発生します。
        """
        if self.fig is None:
            logging.error(f"plot_module: {sys._getframe(1).f_code.co_name}():データがロードされていません。'set_plot()'を先に呼び出してください。")
            raise ValueError("Data is not loaded. Please call 'set_plot()' before accessing the data.")
        
    def draw_plot(self) -> None:
        """
        プロットを表示します。
        """
        self.__data_check()
        plt.show()
        logging.info("設定されたプロットを新しいウィンドウに描画しました。") # txt log

    def save_plot(self, name, fmt='.png'):
        """
        指定した名前と形式でプロットをファイルに保存します。
        Args:
            name (str): 保存するファイル名。
            fmt (str): ファイルの形式（例：'.png', '.jpg'）。デフォルトは'.png'。
        """
        self.__data_check()
        if not fmt.startswith('.'):
            fmt = '.' + fmt
        self.fig.savefig(name+fmt)
        logging.info(f"プロットイメージが'{name+fmt}'に保存されました。") # txt log

    def close_plot(self):
        """
        プロットを閉じます。
        """
        self.__data_check()

        plt.close(self.fig)
from module.data_module import CSVColumnSummer
from module.plot_module import Plotter
import logging
import os

# ログの設定
if not os.path.exists('./log'):
    os.makedirs('./log', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('log/app.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main(
        csv_file_path, 
        delimiter = ',',
        new_data_name = "synthetic wave", 
        save_path = './added_data.csv', 
        save_graph = False,
        # fillna = True,
        # fillna_value = 0,
        fmt = '%8g',
        image_name = None):
    logging.info(f"csv_file_path: {csv_file_path}")
    # summer = CSVColumnSummer(csv_file_path,{'delimiter':delimiter,'fillna':fillna,'fillna_value':fillna_value, 'fmt':fmt})
    summer = CSVColumnSummer(csv_file_path,{'delimiter':delimiter, 'fmt':fmt})
    x_data, y_data = summer.get_data()
    summer.save_data(header = new_data_name, save_path = save_path)
    summer.set_options(fmt=fmt)

    plotter = Plotter()
    plotter.set_plot(x_data,y_data,labels={-1: new_data_name})
    
    if save_graph:
        save_graph_name = save_path.split('.csv')[0] if image_name is None else image_name
        plotter.save_plot(save_graph_name)

    plotter.draw_plot()


    logging.info("実行が完了しました。")  # txt log


if __name__ == "__main__":
    file_path = "../sample_waves.csv"
    main(file_path, save_graph=True)
from data_module import CSVColumnSummer
from plot_module import Plotter

def main(
        csv_file_path, 
        delimiter = ',',
        new_data_name = "synthetic wave", 
        save_path = './added_data.csv', 
        save_graph = False,
        fillna = True,
        fillna_value = 0,
        fmt = '%8g',
        image_name = None):
    
    summer = CSVColumnSummer(csv_file_path, delimiter=delimiter,fillna=fillna,fillna_value=fillna_value)
    x_data, y_data = summer.get_data()
    summer.save_combined(header = new_data_name, save_path = save_path)
    summer.set_config(fmt=fmt)

    plotter = Plotter()
    plotter.set_plot(x_data,y_data)

    if save_graph:
        save_graph_name = save_path.split('.csv')[0] if image_name is None else image_name
        plotter.save_plot(save_graph_name)

    plotter.draw_plot()


if __name__ == "__main__":
    file_path = "../sample_waves.csv"
    main(file_path, save_graph=True)
from data_module import CSVColumnSummer
from plot_module import Plotter

def main(
        csv_file_path, 
        delimiter = ',',
        new_data_name = "synthetic wave", 
        save_path = './added_data.csv', 
        save_graph = False):
    
    summer = CSVColumnSummer(csv_file_path, delimiter=delimiter)
    x_data, y_data = summer.get_data()
    summer.save_combined(header = new_data_name, save_path = save_path)

    plotter = Plotter()
    plotter.set_plot(x_data,y_data)

    if save_graph:
        save_graph_name = save_path.split('.csv')[0]
        plotter.save_plot(save_graph_name)

    plotter.draw_plot()


if __name__ == "__main__":
    file_path = "../sample_waves.csv"
    main(file_path, save_graph=True)
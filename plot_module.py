import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Ploter:
    def __init__(self, x_data=None, y_data=None, labels=None, title='Plot', xlabel='Time'):
        self.axes = None
        self.fig = None

        if x_data is not None and y_data is not None:
            self.set_plot(x_data,y_data,labels,title,xlabel)


    def set_plot(self, x_data, y_data, labels=None, title='Plot', xlabel='Time'):
        def _plot_single_subplot(gs, idx, fig, x_data, y_data, label, color, sharex=None):
            ax = fig.add_subplot(gs[idx], sharex=sharex)
            ax.plot(x_data, y_data, color=color)
            ax.tick_params(axis='x', direction='in', length=4, width=1, top=True)
            ax.tick_params(axis='y', direction='in', labelsize=8)
            ax.legend([label], loc='center left', bbox_to_anchor=(0.995, 0.885), fontsize=8)
            ax.margins(y=0.2)
            return ax
    
        cols = x_data.shape[1]
        fig = plt.figure(figsize=(10, cols))
        fig.suptitle(title)
        fig.canvas.manager.set_window_title(title)
        fig.supxlabel(xlabel)
        gs = gridspec.GridSpec(cols, 1, height_ratios=[0.8] * cols, hspace=0)

        axes = []
        color_list = ['orange', 'gray', 'blue', 'cyan', 'green', 'red', 'purple', 'pink']

        for i in range(cols):
            sharex = axes[0] if i > 0 else None
            label = labels[i] if labels else f"wave{i+1}"
            color = color_list[i % len(color_list)]

            ax = _plot_single_subplot(gs, i, fig, y_data, x_data[:, i], label, color, sharex)
            axes.append(ax)
        
        self.fig  = fig
        self.axes = axes
        return fig, axes
    

    def __data_check(self):
        if self.fig is None:
            raise ValueError("Data is not loaded. Please call 'set_plot()' before accessing the data.")
        
    def draw_plot(self):
        self.__data_check()
        plt.show()

    def save_plot(self, name, fmt='.png'):
        self.__data_check()
        if not fmt.startswith('.'):
            fmt = '.' + fmt
        self.fig.savefig(name+fmt)





# def set_plot(x_data, y_data, labels=None, title='Plot', xlabel='Time'):
#     def _plot_single_subplot(gs, idx, fig, x_data, y_data, label, color, sharex=None):
#             ax = fig.add_subplot(gs[idx], sharex=sharex)
#             ax.plot(x_data, y_data, color=color)
#             ax.tick_params(axis='x', direction='in', length=4, width=1, top=True)
#             ax.tick_params(axis='y', direction='in', labelsize=8)
#             ax.legend([label], loc='center left', bbox_to_anchor=(0.995, 0.885), fontsize=8)
#             ax.margins(y=0.2)
#             return ax
    
#     cols = x_data.shape[1]
#     fig = plt.figure(figsize=(10, cols))
#     fig.suptitle(title)
#     fig.supxlabel(xlabel)
#     gs = gridspec.GridSpec(cols, 1, height_ratios=[0.8] * cols, hspace=0)

#     axlist = []
#     color_list = ['orange', 'gray', 'blue', 'cyan', 'green', 'red', 'purple', 'pink']

#     for i in range(cols):
#         sharex = axlist[0] if i > 0 else None
#         label = labels[i] if labels else f"wave{i+1}"
#         color = color_list[i % len(color_list)]

#         ax = _plot_single_subplot(gs, i, fig, y_data, x_data[:, i], label, color, sharex)
#         axlist.append(ax)

#     return fig, axlist

# def show_plot():
#     plt.show()

# def save_plot(fig, name, fmt = 'png'):
#     save_name = name.split('.csv')[0]+fmt
#     fig.savefig(save_name)
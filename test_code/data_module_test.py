import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from data_module import *

file_path = '../../sample_waves.csv'
summer = CSVColumnSummer(file_path)
# summer.show_config()
# print(summer.data)

# new_data =summer.add_sum_column()
# print(new_data)

summer.save_combined(header="synthetic wave")


x,y = summer.get_data()
from data_module import CSVColumnSummer

file_path = '../sample_waves.csv'
summer = CSVColumnSummer(file_path)
# summer.show_config()
# print(summer.data)

# new_data =summer.add_sum_column()
# print(new_data)

summer.save_combined(header="synthetic wave")


x,y = summer.get_data()
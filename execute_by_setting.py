import yaml
from main import main

def load_config(config_path="config.yaml"):
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config = load_config("config.yaml")
    main(
        csv_file_path = config["csv_file_path"],
        delimiter = config.get("delimiter", ","),
        new_data_name = config.get("new_data_name", "synthetic wave"),
        save_path = config.get("save_path", "./added_data.csv"),
        save_graph = config.get("save_graph", False)
    ) 
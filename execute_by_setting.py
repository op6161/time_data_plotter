import yaml
from main import main

def load_config(config_path="config.yaml"):
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":

    config_path = "config.yaml"
    
    config = load_config(config_path)
    main(
        csv_file_path = config["csv_file_path"],
        delimiter = config.get("delimiter"),
        new_data_name = config.get("new_data_name"),
        save_path = config.get("save_path"),
        save_graph = config.get("save_graph"),
        fillna = config.get("fillna"),
        fillna_value = config.get("fillna_value"),
        fmt = config.get("fmt"),
        image_name = config.get("save_graph_name"),
    ) 
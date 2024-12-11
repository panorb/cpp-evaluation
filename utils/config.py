import tomllib

def load_config():
    config = {
        "trace_initialdir": "",
        "sensor_initialdir": "",
        "background_image_initialdir": "",
        "default_project": ""
    }

    try:
        with open("config.toml", mode='rb') as file:
            file_config = tomllib.load(file).get("config", {})
            config.update(file_config)
    except FileNotFoundError:
        print(f"Config file (config.toml) not found. Using defaults.")

    return config


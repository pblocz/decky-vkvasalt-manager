import configparser as cfg


def parse_config(path):
    section = "CONFIG"
    config = cfg.ConfigParser()  # allow_unnamed_section=True)  # Only works in python 3.13+, but decky uses 3.11

    with open(path, 'r', encoding='utf-8') as f:
        config_string = f"[{section}]\n" + f.read()

    config.read_string(config_string)
    section = config[section]

    data = {}
    for key in section:
        try:
            data[key] = section.getint(key, raw=True)
            continue
        except ValueError:
            ...

        try:
            data[key] = section.getfloat(key, raw=True)
            continue
        except ValueError:
            ...

        try:
            data[key] = section.getboolean(key, raw=True)
            continue
        except ValueError:
            ...

        data[key] = section.get(key, raw=True).strip('"')

    return data


if __name__ == "__main__":  
    path = "../vkBasalt.conf"
    parsed_config = parse_config(path)
    print(parsed_config)


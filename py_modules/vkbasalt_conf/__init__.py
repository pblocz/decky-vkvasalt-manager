import configparser as cfg


def parse_config(path):
    config = cfg.ConfigParser(allow_unnamed_section=True)
    config.optionxform=str
    config.read(path)
    section = config[cfg.UNNAMED_SECTION]

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


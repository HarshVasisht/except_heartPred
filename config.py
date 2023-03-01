import yaml
def read_yaml(path_yaml):
    with open(path_yaml, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
import csv
import json


def num(val):
    try:
        return int(val)
    except ValueError:
        return float(val)


def load_tsv(filename):
    with open(filename, "r") as tsv:
        header = tsv.readline().strip().split("\t")
        return list(csv.DictReader(tsv, fieldnames=header, delimiter="\t"))


# save data in a single json file
def save_json_single(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


# save data in individual json files
def save_json_multi(data, output_path, filename_prop="slug"):
    for item in data:
        with open("{}/{}.json".format(output_path, item[filename_prop]), "w") as f:
            json.dump(item, f, indent=2, sort_keys=True)


def load_data(tsv_filename, output_path, transform, *, multi=False):
    data = transform(load_tsv(tsv_filename))
    if multi:
        save_json_multi(data, output_path)
    else:
        save_json_single(data, output_path)

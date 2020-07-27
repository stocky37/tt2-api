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


def save_json(data, output_dir, filename_prop="slug"):
    for item in data:
        with open("{}/{}.json".format(output_dir, item[filename_prop]), "w") as f:
            json.dump(item, f, indent=2, sort_keys=True)


def load_data(tsv_filename, output_dir, transform):
    data = load_tsv(tsv_filename)
    save_json(transform(data), output_dir)

import json

import numpy as np
import pandas
import pandas as pd
from pandas import *
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
from scipy.stats import kendalltau

header = ['correlation_items', 'r', 'p']


def prepare_result_csv(correlation_item, r, p, save_path):
    data = {
        'correlation_item': correlation_item,
        'r': r,
        'p': p
    }
    df = pandas.DataFrame(data)
    df.to_csv(save_path, index=False)


def write_output_csv(rows, output_file):
    all_content = '\n'.join(rows)
    with open(output_file, "w") as text_file:
        text_file.write(all_content)


def compute_ttest_energy_vs_smell_count(data, metrics, save_path):
    print("To-DO")


def load_json(file):
    with open(file, 'r') as j:
        return json.loads(j.read())


def compute_ttest_for_whole_dataset(metric, project_json):
    projects_map = load_json(project_json)
    user_base_path = "/Users/mrhmisu"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    files = []
    for p in projects_map:
        input_energy_smell_pair_json_path = output_base_path + "/" + p + "/" + p + "-testcase-loc-smell-energy.csv"
        files.append(input_energy_smell_pair_json_path)

    frame = pd.concat((pd.read_csv(f) for f in files))
    frame.to_csv(output_base_path + "/" + "ttest-inputs-" + metric + "-smelly-non-smelly.csv", index=False)
    # TO DO
    # compute_ttest_energy_vs_smell_count()


def compute_ttest_for_each_project(metric):
    projects_map = load_json('projects.json')
    user_base_path = "/Users/mrhmisu"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    for p in projects_map:
        print("Processing :" + p)
        input_energy_smell_pair_json_path = output_base_path + "/" + p + "/" + p + "-energy-smell-testcase-tuple.csv"
        tuple_data = read_csv(input_energy_smell_pair_json_path)
        output_correlation_save_path = output_base_path + "/" + p + "/" + p + "-" + metric + "-correlation.csv"
        # TO DO
        # compute_ttest_energy_vs_smell_count()


if __name__ == '__main__':
    met = "energy"
    # compute_ttest_for_each_project(met)
    compute_ttest_for_whole_dataset(met, "projects.json")

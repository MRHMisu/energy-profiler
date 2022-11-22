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


def compute_correlation_energy_vs_test_smell(data, metrics, save_path):
    """
       If the p-value is low (generally less than 0.05), then your correlation is statistically significant,
       and you can use the calculated Pearson coefficient. If the p-value is not low (generally higher than 0.05),
       then your correlation is not statistically significant (it might have happened just by chance) and
       you should not rely upon your Pearson coefficient.
    """
    # calculate correlation coefficient and p-value between x and y

    headers = ['TC', 'LOC', 'SC', 'E', 'P', 'T', 'ESLoc', 'PSLoc', 'TSLoc', 'AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT',
               'MNT', 'CTL', 'EmT', 'GF', 'IgT', 'SE', 'VT', 'DT', 'RO', 'DA', 'EH', 'CI', 'RP', 'LT']

    correlation_metric = 'ESLoc'
    if metrics == "energy":
        correlation_metric = 'ESLoc'
    if metrics == "power":
        correlation_metric = 'PSLoc'
    if metrics == "time":
        correlation_metric = 'TSLoc'

    r_values = []
    p_values = []

    correlation_items = ['LOC', 'SC', 'AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT', 'MNT', 'CTL', 'EmT', 'GF', 'IgT',
                         'SE', 'VT', 'DT',
                         'RO', 'DA', 'EH', 'CI', 'RP', 'LT']

    for ct in correlation_items:
        r, p = kendalltau(np.array(data[correlation_metric].tolist()), np.array(data[ct].tolist()))
        r_values.append(round(r, 3))
        p_values.append(round(p, 3))

    prepare_result_csv(correlation_items, r_values, p_values, save_path)


def load_json(file):
    with open(file, 'r') as j:
        return json.loads(j.read())


def compute_correlation_for_whole_dataset(metric):
    projects_map = load_json('projects.json')
    user_base_path = "/Users/mrhmisu"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    files = []
    for p in projects_map:
        input_energy_smell_pair_json_path = output_base_path + "/" + p + "/" + p + "-energy-smell-testcase-tuple.csv"
        files.append(input_energy_smell_pair_json_path)

    frame = pd.concat((pd.read_csv(f) for f in files))
    compute_correlation_energy_vs_test_smell(frame, metric, "energy-smell-correlation.csv")


def compute_correlation_for_each_project(metric):
    projects_map = load_json('projects.json')
    user_base_path = "/Users/mrhmisu"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    for p in projects_map:
        print("Processing :" + p)
        input_energy_smell_pair_json_path = output_base_path + "/" + p + "/" + p + "-energy-smell-testcase-tuple.csv"
        tuple_data = read_csv(input_energy_smell_pair_json_path)
        output_correlation_save_path = output_base_path + "/" + p + "/" + p + "-" + metric + "-correlation.csv"
        compute_correlation_energy_vs_test_smell(tuple_data, metric,
                                                 output_correlation_save_path)


if __name__ == '__main__':
    # energy_smell_pairs_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/gson/gson-energy-smell-testcase-tuple.csv"
    # # metrics, Energy, Power and Time
    # save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/gson/correlation_result.csv"
    # compute_correlation_energy_vs_test_smell(energy_smell_pairs_save_path, "Energy", save_path)
    # print("")
    met = "energy"
    # met = "power"
    # met = "time"

    # compute_correlation_for_each_project(met)
    compute_correlation_for_whole_dataset(met)

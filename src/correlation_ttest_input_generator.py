import json

from src.energy_log_processor import generate_median_energy_result_json
from src.energy_smell_pair_map_processor import generate_energy_smelly_pairs_in_csv, \
    generate_energy_smelly_and_non_smelly_pairs_in_csv

from src.smell_report_processor import generate_testcase_and_smell_count_json


def generate_correlation_inputs(projects_map, input_path, output_path):
    number_of_run = 5
    for p in projects_map:
        jnose_prefix = projects_map[p]
        testcase_path = input_path + "/" + "testcase/with-loc/" + p + "-testcases-loc.txt"
        energy_log_path = input_path + "/" + "energy-log/" + p
        smells_path = input_path + "/" + "smell/" + p + "/" + p + "-smell-by-testsmell.csv"

        input_energy_json_path = output_path + "/" + p + "/" + p + "-energy-testcase-pair.json"
        input_smell_json_path = output_path + "/" + p + "/" + p + "-smell-testcase-pair.json"

        output_energy_smelly_pair_json_path = output_path + "/" + p + "/" + p + "-energy-smell-testcase-tuple.csv"
        output_energy_smell_and_non_smelly_pair_json_path = output_path + "/" + p + "/" + p + "-testcase-loc-smell-energy.csv"

        generate_median_energy_result_json(testcase_path, number_of_run, energy_log_path, input_energy_json_path)
        generate_testcase_and_smell_count_json(smells_path, jnose_prefix, input_smell_json_path)
        generate_energy_smelly_pairs_in_csv(input_energy_json_path, input_smell_json_path,
                                            output_energy_smelly_pair_json_path)
        generate_energy_smelly_and_non_smelly_pairs_in_csv(input_energy_json_path, input_smell_json_path,
                                                           output_energy_smell_and_non_smelly_pair_json_path)

    # run_correlation_analyzer()


def load_json(file):
    with open(file, 'r') as j:
        return json.loads(j.read())


if __name__ == '__main__':
    projects = load_json('projects.json')
    user_base_path = "/Users/mrhmisu"
    input_base_path = user_base_path + "/energy-profiler-experiment/dataset"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    generate_correlation_inputs(projects, input_base_path, output_base_path)

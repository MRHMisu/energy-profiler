import json

from src.energy_log_processor import generate_median_energy_result_json
from src.energy_smell_pair_map_processor import generate_energy_smell_pairs_in_csv

from src.smell_report_processor import generate_testcase_and_smell_count_json


def run_analysis(projects_map, input_path, output_path):
    number_of_run = 5
    for p in projects_map:
        jnose_prefix = projects_map[p]
        testcase_path = input_path + "/" + "testcase/with-loc/" + p + "-testcases-loc.txt"
        energy_log_path = input_path + "/" + "energy-log/" + p
        smells_path = input_path + "/" + "smell/" + p + "/" + p + "-smell-by-testsmell.csv"

        output_energy_json_path = output_path + "/" + p + "/" + p + "-energy-testcase-pair.json"
        output_smell_json_path = output_path + "/" + p + "/" + p + "-smell-testcase-pair.json"
        output_energy_smell_pair_json_path = output_path + "/" + p + "/" + p + "-energy-smell-testcase-tuple.csv"

        generate_median_energy_result_json(testcase_path, number_of_run, energy_log_path, output_energy_json_path)
        generate_testcase_and_smell_count_json(smells_path, jnose_prefix, output_smell_json_path)
        generate_energy_smell_pairs_in_csv(output_energy_json_path, output_smell_json_path,
                                           output_energy_smell_pair_json_path)

    # run_correlation_analyzer()


def load_json(file):
    with open(file, 'r') as j:
        return json.loads(j.read())


if __name__ == '__main__':
    projects = load_json('projects.json')
    user_base_path = "/Users/mrhmisu"
    input_base_path = user_base_path + "/energy-profiler-experiment/dataset"
    output_base_path = user_base_path + "/Repositories/test-smells/energy-profiler/output"
    run_analysis(projects, input_base_path, output_base_path)

import json

import pandas
import statistics
import math


def get_mean(data):
    n = len(data)
    mean = sum(data) / n
    return mean


def get_variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n
    return variance


def get_standard_deviation(data):
    var = get_variance(data)
    std_dev = math.sqrt(var)
    return std_dev


def get_median(data):
    return statistics.median(data)


def get_overall_result_for_a_single_run(file_path):
    energy_metrics = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        # retrieve the average values end of the files
        energy_metrics['time'] = float(lines[-14].split(" = ")[1][:-2])
        energy_metrics['power'] = float(lines[-9].split(" = ")[1][:-2])
        energy_metrics['energy'] = float(lines[-11].split(" = ")[1][:-2])
    return energy_metrics


def get_overall_result_for_all_run(base_path, testcase_name, num_run):
    overall_energy_metrics = {'testcase': testcase_name, 'median_elapsed_time': 0, 'median_power': 0,
                              'median_energy_consumed': 0, 'average_elapsed_time': 0, 'average_power': 0,
                              'average_energy_consumed': 0}
    time = []
    power = []
    energy = []

    for i in range(1, num_run + 1):
        file_path = base_path + "/" + testcase_name + "-" + str(i) + ".csv"
        energy_metrics = get_overall_result_for_a_single_run(file_path)
        time.append(energy_metrics['time'])
        power.append(energy_metrics['power'])
        energy.append(energy_metrics['energy'])

    overall_energy_metrics['median_elapsed_time'] = get_median(time)
    overall_energy_metrics['median_power'] = get_median(power)
    overall_energy_metrics['median_energy_consumed'] = get_median(energy)
    overall_energy_metrics['average_elapsed_time'] = get_mean(time)
    overall_energy_metrics['average_power'] = get_mean(power)
    overall_energy_metrics['average_energy_consumed'] = get_mean(energy)

    return overall_energy_metrics


def get_all_testcase_names_and_loc(path):
    name_loc = {}
    with open(path, "r") as file:
        lines = set(file.read().splitlines())
        for line in lines:
            name = line.split(",")[0].strip()
            loc = line.split(",")[1]
            name_loc[name] = loc
    return name_loc


def get_average_energy_result_csv(testcase_path, num_of_run, eng_report_path, save_path):
    testcase = []
    loc = []
    average_elapsed_time = []
    average_power = []
    average_energy_consumed = []

    median_elapsed_time = []
    median_power = []
    median_energy_consumed = []

    testcases_names_loc = get_all_testcase_names_and_loc(testcase_path)
    for tc in testcases_names_loc:
        avg_result = get_overall_result_for_all_run(eng_report_path, tc, num_of_run)
        testcase.append(avg_result['testcase'])
        loc.append(testcases_names_loc[tc])
        median_elapsed_time.append(avg_result['median_elapsed_time'])
        median_power.append(avg_result['median_power'])
        median_energy_consumed.append(avg_result['median_energy_consumed'])
        average_elapsed_time.append(avg_result['average_elapsed_time'])
        average_power.append(avg_result['average_power'])
        average_energy_consumed.append(avg_result['average_energy_consumed'])
    data = {
        'testcase': testcase,
        'loc': loc,
        'median_elapsed_time': median_elapsed_time,
        'median_power': median_power,
        'median_energy_consumed': median_energy_consumed,
        # 'average_elapsed_time': average_elapsed_time,
        # 'average_power': average_power,
        # 'average_energy_consumed': average_energy_consumed
    }
    df = pandas.DataFrame(data)
    df.to_csv(save_path, index=False)


def get_average_energy_result_json(testcase_path, num_of_run, eng_report_path, save_path):
    testcase_map = {}
    testcases_names_loc = get_all_testcase_names_and_loc(testcase_path)
    for tc in testcases_names_loc:
        avg_result = get_overall_result_for_all_run(eng_report_path, tc, num_of_run)
        testcase_map[tc] = {
            'loc': testcases_names_loc[tc],
            'median_elapsed_time': avg_result['median_elapsed_time'],
            'median_power': avg_result['median_power'],
            'median_energy_consumed': avg_result['median_energy_consumed'],
            'average_elapsed_time': avg_result['average_elapsed_time'],
            'average_power': avg_result['average_power'],
            'average_energy_consumed': avg_result['average_energy_consumed']
        }
    save_to_json(testcase_map, save_path)


def save_to_json(map, path):
    json_string = json.dumps(map)
    with open(path, "w") as text_file:
        text_file.write(json_string)
    print("Saving Done")


def get_header():
    headers = []
    headers.append("Testcase")
    headers.append("System Time")
    headers.append("RDTSC")
    headers.append("Elapsed Time (sec)")
    headers.append("CPU Utilization(%)")
    headers.append("CPU Frequency_0(MHz)")
    headers.append("CPU Min Frequency_0(MHz)")
    headers.append("CPU Max Frequency_0(MHz)")
    headers.append("CPU Requsted Frequency_0(MHz)")
    headers.append("Processor Power_0(Watt)")
    headers.append("Cumulative Processor Energy_0(Joules)")
    headers.append("Cumulative Processor Energy_0(mWh)")
    headers.append("IA Power_0(Watt)")
    headers.append("Cumulative IA Energy_0(Joules)")
    headers.append("Cumulative IA Energy_0(mWh)")
    headers.append("Package Temperature_0(C)")
    headers.append("Package Hot_0")
    headers.append("CPU Min Temperature_0(C)")
    headers.append("CPU Max Temperature_0(C)")
    headers.append("DRAM Power_0(Watt)")
    headers.append("Cumulative DRAM Energy_0(Joules)")
    headers.append("Cumulative DRAM Energy_0(mWh)")
    headers.append("Package Power Limit_0(Watt)")
    headers.append("GT Frequency(MHz)")
    headers.append("GT Requsted Frequency(MHz)")
    return ",".join(headers)


def merge_energy_result_for_all_run(testcase_path, num_of_run, energy_reports_path, save_path):
    testcases_names_loc = get_all_testcase_names_and_loc(testcase_path)
    all_merged = []
    all_merged.append(get_header())
    for tc in testcases_names_loc:
        aggregated = []
        for i in range(1, num_of_run + 1):
            file_path = energy_reports_path + "/" + tc + "-" + str(i) + ".csv"
            with open(file_path, "r") as file:
                lines = file.readlines()
                extracted_data = lines[1:-15]
                aggregated.extend(extracted_data)
        for i in range(len(aggregated)):
            aggregated[i] = tc + "," + aggregated[i]
        all_merged.extend(aggregated)
    write_aggregate_results(all_merged, save_path)


def write_aggregate_results(all_merged, path):
    content = ''.join(all_merged)
    with open(path, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    project_name = "jsoup"
    testcase_name_path = "/Users/mrhmisu/energy-test/dataset/testcase/with-loc/jsoup-testcases-loc.txt"
    result_base_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/" + project_name
    energy_reports_path = "/Users/mrhmisu/energy-test/dataset/energy-log/" + project_name
    number_of_run = 5
    average_save_path = result_base_path + "/" + project_name + "-" + "energy-median-average.json"
    # aggregate_save_path = energy_reports_path + "/res/" + project_name + "-" + "aggregate_result.csv"

    get_average_energy_result_json(testcase_name_path, number_of_run, energy_reports_path, average_save_path)
    # merge_energy_result_for_all_run(testcase_name_path, number_of_run, energy_reports_path,
    #                                 aggregate_save_path)

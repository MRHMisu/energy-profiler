import pandas


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
    average_energy_metrics = {'testcase': testcase_name, 'elapsed_time': 0, 'average_power': 0, 'energy_consumed': 0}
    for i in range(1, num_run + 1):
        file_path = base_path + "/" + testcase_name + "-" + str(i) + ".csv"
        energy_metrics = get_overall_result_for_a_single_run(file_path)
        average_energy_metrics['elapsed_time'] = average_energy_metrics['elapsed_time'] + energy_metrics['time']
        average_energy_metrics['average_power'] = average_energy_metrics['average_power'] + energy_metrics['power']
        average_energy_metrics['energy_consumed'] = average_energy_metrics['energy_consumed'] + energy_metrics['energy']

    average_energy_metrics['elapsed_time'] = average_energy_metrics['elapsed_time'] / num_run
    average_energy_metrics['average_power'] = average_energy_metrics['average_power'] / num_run
    average_energy_metrics['energy_consumed'] = average_energy_metrics['energy_consumed'] / num_run
    return average_energy_metrics


def get_all_testcase_names(path):
    with open(path, "r") as file:
        lines = file.readlines()
    return lines


def get_average_energy_result(testcase_path, num_of_run, energy_reports_path, save_path):
    testcase = []
    time = []
    power = []
    energy = []

    testcases_names = get_all_testcase_names(testcase_path)
    for tc in testcases_names:
        avg_result = get_overall_result_for_all_run(energy_reports_path, tc, num_of_run)
        testcase.append(avg_result['testcase'])
        time.append(avg_result['elapsed_time'])
        power.append(avg_result['average_power'])
        energy.append(avg_result['energy_consumed'])

    data = {
        'testcase': testcase,
        'elapsed_time': time,
        'average_power': power,
        'energy_consumed': energy
    }
    df = pandas.DataFrame(data)
    df.to_csv(save_path, index=False)


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
    testcases_names = get_all_testcase_names(testcase_path)
    all_merged = []
    all_merged.append(get_header())
    for tc in testcases_names:
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
    testcase_name_path = "/test-cases.txt"
    energy_reports_base_path = "/result"
    number_of_run = 5
    average_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/result/average_result.csv"
    aggregate_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/result/aggregate_result.csv"

    get_average_energy_result(testcase_name_path, number_of_run, energy_reports_base_path, average_save_path)
    merge_energy_result_for_all_run(testcase_name_path, number_of_run, energy_reports_base_path,
                                    aggregate_save_path)

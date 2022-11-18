import json


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = set(file.read().splitlines())
        return lines


def make_map(lines):
    items = {}
    for line in lines:
        items[line] = line
    return items


def write_to_csv(content, path):
    with open(path, 'w') as file:
        file.write(content)


def load_json(path):
    with open(path, 'r') as j:
        contents = json.loads(j.read())
    return contents


def add_default_count_foreach_smells(obj):
    smell_names = ['AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT', 'MNT', 'CTL', 'EmT', 'GF', 'IgT',
                   'SE', 'VT', 'DT', 'RO', 'DA', 'EH', 'CI', 'RP', 'LT']
    for sm in smell_names:
        obj[sm] = 0
    return obj


def get_smelly_and_non_smelly_testcases(energy_testcase_map, smelly_testcases_map):
    smelly_testcases = set(energy_testcase_map.keys()).intersection(smelly_testcases_map.keys())
    non_smelly_testcases = set(energy_testcase_map.keys()).difference(smelly_testcases_map.keys())
    return smelly_testcases, non_smelly_testcases


# "loc": "9",
#     "median_elapsed_time": 15.962748,
#     "median_power": 11.948479,
#     "median_energy_consumed": 189.492004,
#     "average_elapsed_time": 16.1229668,
#     "average_power": 11.9516156,
#     "average_energy_consumed": 192.7227628


# "test_class": "com.google.gson.JsonObjectTest",
#    "smell_count": 8,
#    "smells": {
#      "LT": 4,
#      "ET": 1,
#      "AR": 3
#    }

def prepare_energy_smell_pairs(eng_map, sm_map, save_path):
    smelly_testcases, non_smelly_testcases = get_smelly_and_non_smelly_testcases(eng_map, sm_map)
    headers = ['TC', 'LOC', 'SC', 'E', 'P', 'T', 'ESLoc', 'PSLoc', 'TSLoc', 'AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT',
               'MNT', 'CTL', 'EmT', 'GF', 'IgT',
               'SE', 'VT', 'DT', 'RO', 'DA', 'EH', 'CI', 'RP', 'LT']
    rows = []
    rows.append(str(",".join(headers)))
    for stc in smelly_testcases:
        energy_data = eng_map[stc]
        smell_data = sm_map[stc]
        row_obj = get_each_row_obj(stc, energy_data, smell_data)
        row = make_row_obj_to_csv_row(row_obj)
        rows.append(str(row))
    content = "\n".join(rows)
    write_to_csv(content, save_path)


def make_row_obj_to_csv_row(row_obj):
    values = []
    for v in row_obj:
        values.append(str(row_obj[v]))
    return ",".join(values)


def get_each_row_obj(smelly_testcase, energy_data, smell_data):
    obj = {}
    obj['TC'] = smelly_testcase
    obj['LOC'] = int(energy_data['loc'])
    obj['SC'] = int(smell_data['smell_count'])
    obj['E'] = float(energy_data['median_energy_consumed'])
    obj['P'] = float(energy_data['median_power'])
    obj['T'] = float(energy_data['median_elapsed_time'])
    obj['ESLoc'] = float(obj['E'] / (obj['SC'] / obj['LOC']))
    obj['PSLoc'] = float(obj['P'] / (obj['SC'] / obj['LOC']))
    obj['TSLoc'] = float(obj['T'] / (obj['SC'] / obj['LOC']))
    add_default_count_foreach_smells(obj)
    for smc in smell_data['smells']:
        if smc in obj:
            obj[smc] = smell_data['smells'][smc]

    return obj


if __name__ == '__main__':
    energy_map_file = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/jsoup/jsoup-energy-median-average.json"
    smell_map_file = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/jsoup/jsoup-testcase-smell-map.json"
    energy_smell_pairs_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/jsoup/jsoup-energy-smell-pair.csv"

    energy_map = load_json(energy_map_file)
    smell_map = load_json(smell_map_file)
    prepare_energy_smell_pairs(energy_map, smell_map, energy_smell_pairs_save_path)

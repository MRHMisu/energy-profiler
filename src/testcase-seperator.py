def read_file(file_path):
    with open(file_path, "r") as file:
        lines = set(file.read().splitlines())
        return lines


def make_map(lines):
    items = {}
    for line in lines:
        items[line] = line
    return items


def write_results(all_merged, path):
    content = ''.join(all_merged)
    with open(path, 'w') as file:
        file.write(content)


def find_non_smelly_testcase(all_test_case_path, smelly_test_case_path, non_smelly_test_case_save):
    all_testcase_map = make_map(read_file(all_test_case_path))
    smelly_testcase_map = make_map(read_file(smelly_test_case_path))
    non_smelly_testcases = set(all_testcase_map.keys()).difference(smelly_testcase_map.keys())
    print("Done")
    # write_results(non_smelly_testcases, non_smelly_test_case_save)


if __name__ == '__main__':
    all_test_case_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/smell-result/commons-lang/all_testcases.txt"
    smelly_test_case_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/smell-result/commons-lang/smelly_testcases_run.txt"
    non_smelly_test_case_save = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/smell-result/commons-lang/non_smelly_testcase.txt"
    find_non_smelly_testcase(all_test_case_path, smelly_test_case_path, non_smelly_test_case_save)

import csv
import json


def process_report(report_name, prefix):
    test_class_map = {}
    with open(report_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:  # skip columns
                print("Processing row: " + str(line_count))
                process_each_row(prefix, row, test_class_map)
            line_count += 1
    print(len(test_class_map))
    return test_class_map


# projectName row[0]
# name (test file) row[1]
# pathFile row[2]
# productionFile row[3] (ignore)
# junitVersion row[4] (ignore)
# loc row[5] (ignore)
# qtdMethods row[6] (ignore)
# testSmellName row[7]
# testSmellMethod row[8]
# testSmellLineBegin row[9]
# testSmellLineEnd row[10]

def process_each_row(path_prefix, row, test_class_map):
    test_file_name = row[1].strip()
    production_file_name = row[3].strip()
    test_class_name = test_file_name.strip().split(".java")[0]
    try:
        production_class_fqn = production_file_name.split(path_prefix)[1].replace("/", ".").split(".java")[0]
        package_name_fqn = ".".join(production_class_fqn.split(".")[0: len(production_class_fqn.split(".")) - 1])
        test_class_fqn = package_name_fqn + "." + test_file_name
        test_smell_name = row[7].strip()
        smelly_test_case_list = row[8].split(",")  # list of testcases seperated by comma

        smelly_test_cases_map = make_test_case_object(test_class_fqn, test_smell_name, smelly_test_case_list)
        populate_test_classes(test_class_map, test_class_fqn, smelly_test_cases_map)
    except:
        print("prefix errors")
        return


def populate_test_classes(testclass_to_testcase_map, test_class_name, testcases_list_containing_smells):
    # check if the testclass is already in the global map
    if test_class_name in testclass_to_testcase_map:
        # get the existing testcases from the <testclass, testcases> map
        testcases_map = testclass_to_testcase_map[test_class_name]
        # for each testcase in the new testcasemap
        for tc in testcases_list_containing_smells:  # <testcase->[smell]>
            # when testcase already in the testclass_to_testcase_map
            if tc in testcases_map:
                # (add the smell in the smell list)
                smells_needs_to_append = testcases_list_containing_smells[tc]['smells']  # get the new smells list
                already_contained_smells = testcases_map[tc]['smells']
                for sm in smells_needs_to_append:
                    # foreach new smell, first get its <smell-counter> map
                    if sm in already_contained_smells:
                        # if the smell is already in the  <smell-counter> map,
                        # increment the counter in global <testclass->testcase->smell> map
                        testclass_to_testcase_map[test_class_name][tc]['smells'][sm] = already_contained_smells[sm] + 1
                    else:
                        # if smell is not in the <smell-counter> map, it is a new smell for the testcase
                        # so just add it in the global <testclass->testcase->smell> map
                        testclass_to_testcase_map[test_class_name][tc]['smells'][sm] = smells_needs_to_append[sm]
            else:
                # if testcase already in the testclass_to_testcase_map
                # it is a new tescase for this testclass so add it to the global testclass_to_testcase_map
                testclass_to_testcase_map[test_class_name][tc] = testcases_list_containing_smells[tc]
    else:
        # if the testclass is not in the global map
        # just add it in the global list with the given smelly testcases
        # for a test class, this will execute once at first
        testclass_to_testcase_map[test_class_name] = testcases_list_containing_smells


def make_test_case_object(test_class_name, test_smell_name, smelly_test_cases):
    test_cases = {}
    for stc in smelly_test_cases:
        key = stc.strip()
        test_cases[key] = {
            "name": key,
            "mvn_run": test_class_name + "#" + key,
            "smells": {}
        }
        test_cases[key]['smells'][test_smell_name] = 1
    return test_cases


def make_smelly_test_list(testclasses):
    testcase_run = []
    for tcls in testclasses:
        testcases = testclasses[tcls]
        for tc in testcases:
            testcase_run.append(testcases[tc]['mvn_run'])
    print(len(testcase_run))
    return testcase_run


def save_to_json(map, path):
    json_string = json.dumps(map)
    with open(path, "w") as text_file:
        text_file.write(json_string)
    print("Saving Done")


def save_to_testcaes_in_csv(map, path):
    # Assertion Roulette
    # Eager Test
    # Mystery Guest
    # Sleepy Test
    # Unknown Test
    # Redundant Assertion
    # Dependent Test
    # Magic Number Test
    # Conditional Test Logic
    # EmptyTest
    # General Fixture
    # IgnoredTest
    # Sensitive Equality
    # Verbose Test
    # Default Test
    # Resource Optimism
    # Duplicate Assert
    # Exception Catching Throwing
    # Constructor Initialization
    # Print Statement
    # Lazy Test
    smell_names = ['AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT', 'MNT', 'CTL', 'EmT', 'GF', 'IgT',
                   'SE', 'VT', 'DT', 'RO', 'DA', 'EH', 'CI', 'RP', 'LT']
    test_cases = []
    for m in map:
        test_class = map[m]
        for tc in test_class:
            case = test_class[tc]['mvn_run']
            complete_line = case + ","


def write_smelly_test_results(path, test_list):
    content = '\n'.join(test_list)
    with open(path, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    project_prefix_path = "/Users/mrhmisu/.jnose_projects/gson/gson/src/main/java/"
    smell_by_testsmell = "/Users/mrhmisu/energy-test/dataset/smell/gson/gson-smell-by-testsmell.csv"

    output_smell_map_file = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/gson/gson-testcase-smell-map.json"
    smelly_test_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/gson/gson-smelly-testcase.txt"

    testclasss_map = process_report(smell_by_testsmell, project_prefix_path)
    test_list = make_smelly_test_list(testclasss_map)
    # save_to_json(testclasss_map, output_smell_map_file)
    # write_smelly_test_results(smelly_test_save_path, test_list)
    # save_to_testcaes_in_csv(testclasss_map, output_smell_map_file)
    print("done")

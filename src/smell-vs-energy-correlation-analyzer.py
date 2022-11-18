import numpy as np
from pandas import *
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
from scipy.stats import kendalltau


def compute_correlation_energy_vs_test_smell(file_name):
    """
       If the p-value is low (generally less than 0.05), then your correlation is statistically significant,
       and you can use the calculated Pearson coefficient. If the p-value is not low (generally higher than 0.05),
       then your correlation is not statistically significant (it might have happened just by chance) and
       you should not rely upon your Pearson coefficient.
    """
    data = read_csv(file_name)
    # header
    #  ['TC', 'LOC', 'SC', 'E', 'P', 'T', 'ESLoc', 'PSLoc', 'TSLoc', 'AR', 'ET', 'MG', 'ST', 'UT', 'RA', 'DepT',
    #            'MNT', 'CTL', 'EmT', 'GF', 'IgT',
    #            'SE', 'VT', 'DT', 'RO', 'DA', 'EH', 'CI', 'RP', 'LT']

    # E = np.array(data['tss_loc'].tolist())
    # tss_rev_loc_scores = np.array(data['tss_rev_loc'].tolist())
    # tss_nom_scores = np.array(data['tss_nom'].tolist())
    # tss_rev_nom_scores = np.array(data['tss_rev_nom'].tolist())
    # mut_scores = np.array(data['mut_score'].tolist())

    # calculate correlation coefficient and p-value between x and y
    r_E_vs_LOC, p_E_vs_LOC = kendalltau(data['ESLoc'].tolist(), data['ET'].tolist())
    print(r_E_vs_LOC, p_E_vs_LOC)
    r_P_vs_LOC, p_P_vs_LOC = kendalltau(data['PSLoc'].tolist(), data['ET'].tolist())
    print(r_P_vs_LOC, p_P_vs_LOC)


if __name__ == '__main__':
    energy_smell_pairs_save_path = "/Users/mrhmisu/Repositories/test-smells/energy-profiler/output/gson/gson-energy-smell-pair.csv"
    compute_correlation_energy_vs_test_smell(energy_smell_pairs_save_path)

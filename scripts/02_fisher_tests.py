import os
import pandas as pd
from scipy.stats import fisher_exact

root = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(root, "../data/processed/01_covid_hiv_data.csv"))

def fisher_test_wave(df, wave, col, cutoff):
    df = df[df["covid_wave"] != -1]
    df = df[df["covid_wave"] <= wave]
    if wave not in set(df["covid_wave"].tolist()):
        return
    df.loc[df["covid_wave"] > 0, "covid_wave"] = 1
    df = df[df[col] != -1]
    tl = df[df[col] <= cutoff]
    tg = df[df[col] >= cutoff]
    if (tl.shape[0] == 0) or (tg.shape[0] == 0):
        return
    if col == "viremic":
        alternative = "two-sided"
        x_data = []
        y_data = []
        for v in df[["covid_wave", col]].values:
            x_data += [v[0]]
            y_data += [v[1]]
        tab = pd.crosstab(x_data, y_data)
        if tab.shape != (2, 2):
            return
        odds_ratio, p_value = fisher_exact(tab, alternative=alternative)
        print("Wave {0} - {1} (cut = {2}) Fisher's exact (alternative = {3}): N = {4}, OR = {5:.2f}, P-value = {6:.2g}".format(wave, col.upper(), cutoff, alternative, len(df), odds_ratio, p_value))
        return len(df), odds_ratio, p_value, alternative
    if col == "rna":
        alternative = "two-sided"
        x_data = []
        y_data = []
        for v in df[["covid_wave", col]].values:
            x_data += [v[0]]
            if v[1] >= cutoff:
                y_data += [1]
            else:
                y_data += [0]
        tab = pd.crosstab(x_data, y_data)
        if tab.shape != (2, 2):
            return
        odds_ratio, p_value = fisher_exact(tab, alternative=alternative)
        print("Wave {0} - {1} (cut = {2}) Fisher's exact (alternative = {3}): N = {4}, OR = {5:.2f}, P-value = {6:.2g}".format(wave, col.upper(), cutoff, alternative, len(df), odds_ratio, p_value))
        return len(df), odds_ratio, p_value, alternative
    if col == "cd4":
        alternative = "two-sided"
        x_data = []
        y_data = []
        for v in df[["covid_wave", col]].values:
            x_data += [v[0]]
            if v[1] <= cutoff:
                y_data += [1]
            else:
                y_data += [0]
        tab = pd.crosstab(x_data, y_data)
        if tab.shape != (2, 2):
            return
        odds_ratio, p_value = fisher_exact(tab, alternative=alternative)
        print("Wave {0} - {1} (cut = {2}) Fisher's exact (alternative = {3}): N = {4}, OR = {5:.2f}, P-value = {6:.2g}".format(wave, col.upper(), cutoff, alternative, len(df), odds_ratio, p_value))
        return len(df), odds_ratio, p_value, alternative
    if col == "retention":
        alternative = "two-sided"
        x_data = []
        y_data = []
        for v in df[["covid_wave", col]].values:
            x_data += [v[0]]
            if v[1] >= cutoff:
                y_data += [1]
            else:
                y_data += [0]
        tab = pd.crosstab(x_data, y_data)
        if tab.shape != (2, 2):
            return
        odds_ratio, p_value = fisher_exact(tab, alternative=alternative)
        print("Wave {0} - {1} (cut = {2}) Fisher's exact (alternative = {3}): N = {4}, OR = {5:.2f}, P-value = {6:.2g}".format(wave, col.upper(), cutoff, alternative, len(df), odds_ratio, p_value))
        return len(df), odds_ratio, p_value, alternative
    if col == "died":
        alternative = "two-sided"
        x_data = []
        y_data = []
        for v in df[["covid_wave", col]].values:
            x_data += [v[0]]
            if v[1] >= cutoff:
                y_data += [1]
            else:
                y_data += [0]
        tab = pd.crosstab(x_data, y_data)
        if tab.shape != (2, 2):
            return
        odds_ratio, p_value = fisher_exact(tab, alternative=alternative)
        print("Wave {0} - {1} (cut = {2}) Fisher's exact (alternative = {3}): N = {4}, OR = {5:.2f}, P-value = {6:.2g}".format(wave, col.upper(), cutoff, alternative, len(df), odds_ratio, p_value))
        return len(df), odds_ratio, p_value, alternative

R = []
for wave in [1, 2, 3, 4]:
    for col in ["rna", "cd4", "viremic", "died", "retention"]:
        for cut in [1, 2, 3, 4, 5, 6]:
            results = fisher_test_wave(df, wave, col, cut)
            if results is None:
                continue
            r = [wave, col, cut, results[-1], results[0], results[1], results[2]]
            R += [r]

dr = pd.DataFrame(R, columns=["wave", "variable", "cutoff", "alternative", "num_samples", "odds_ratio", "p_value"])
dr.to_csv(os.path.join(root, "../data/processed/02_fisher_test_results.csv"), index=False)
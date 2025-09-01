import os
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(root, "../data/processed/01_covid_hiv_data.csv"))


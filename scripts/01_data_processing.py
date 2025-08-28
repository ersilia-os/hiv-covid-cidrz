import os
import csv
import pandas as pd
from datetime import datetime
from tqdm import tqdm

N_BLOCKS = 2

root = os.path.dirname(os.path.abspath(__file__))

raw_data_dir = os.path.join(root, '..', 'data', 'raw')
processed_data_dir = os.path.join(root, '..', 'data', 'processed')

base_file_name = "-28aug2025.csv"

STARTING_DATE = datetime.strptime("2017-01-01", "%Y-%m-%d")

AGE_CATS = {
    "15-19 years": 1,
    "20-29 years": 2,
    "30-39 years": 3,
    "40-49 years": 4,
    "50-59 years": 5,
    "60+ years": 6,
}

MARITAL_STATUS_CATS = {
    "Single": 1,
    "Married": 2,
    "Divorced/Seperated": 3,
    "Widowed": 4,
}

# id,visitdate,age,age_cat,sex,time_in_care,rna,cd4,retention,art_regimen,who_stage,facility,district,province,marital_status,died,official_transfer,covid_wave,vaccine

def process_data(df, art_regimen_cats, facility_cats, district_cats, province_cats):
    df = df[df["id"].notnull()]
    df = df[df["visitdate"].notnull()]
    
    # identifier column
    dp = pd.DataFrame({"id": df["id"]})
    # visit date
    visit_date = []
    day = []
    week = []
    month = []
    year = []
    for v in df["visitdate"].tolist():
        v = str(v)
        if v == "nan":
            visit_date += [None]
            continue
        v = datetime.strptime(v)
        day += [v.day]
        week += [v.isocalendar()[1]]
        month += [v.month]
        year += [v.year]
        delta_days = (v - STARTING_DATE).days
        visit_date += [delta_days]
    dp["visit_date"] = visit_date
    dp["day"] = day
    dp["week"] = week
    dp["month"] = month
    dp["year"] = year

    # age and age cat
    age = []
    age_cat = []
    for v in df["age"].tolist():
        if str(v) == "nan":
            age += [None]
            continue
        age += [int(v)]
    dp["age"] = age
    age_cat = []
    for v in df["age_cat"].tolist():
        v = str(v)
        if str(v) == "nan":
            age_cat += [None]
            continue
        if v not in AGE_CATS:
            raise ValueError(f"Unknown age category: {v}")
        age_cat += [AGE_CATS[v]]
    # sex column
    sex = []
    for v in df["sex"].tolist():
        v = str(v)
        if v == "nan":
            sex += [None]
            continue
        if v == "F":
            sex += [1]
            continue
        if v == "M":
            sex += [0]
            continue
        raise ValueError(f"Unknown sex category: {v}")
    dp["sex_female"] = sex
    # marital status
    marital_status = []
    for v in df["marital_status"].tolist():
        v = str(v)
        if v == "nan":
            marital_status += [None]
            continue
        if v not in MARITAL_STATUS_CATS:
            raise ValueError(f"Unknown marital status: {v}")
        marital_status += [MARITAL_STATUS_CATS[v]]
    dp["marital_status"] = marital_status
    
    # time in care column
    time_in_care = []
    for v in df["time_in_care"].tolist():
        if str(v) == "nan":
            time_in_care += [None]
            continue
        time_in_care += [int(v)]
    dp["time_in_care"] = time_in_care
    # official transfer
    official_transfer = []
    for v in df["official_transfer"].tolist():
        if str(v) == "nan":
            official_transfer += [None]
            continue
        official_transfer += [int(v)]
    dp["official_transfer"] = official_transfer
    
    # who stage
    who_stage = []
    for v in df["who_stage"].tolist():
        if str(v) == "nan":
            who_stage += [None]
            continue
        v = int(v.split("Stage ")[1])
        if v not in set([1,2,3,4]):
            raise ValueError(f"Unknown who stage: {v}")
        who_stage += [v]
    dp["who_stage"] = who_stage
    # art regimen
    art_regimen = []
    for v in df["art_regimen"].tolist():
        v = str(v).replace(" ", "")
        if v == "nan":
            art_regimen += [None]
            continue
        v = sorted(set(v.split("+")))
        k = "-".join(v)
        if k not in art_regimen_cats:
            art_regimen_cats[k] = len(art_regimen_cats) + 1
        art_regimen += [art_regimen_cats[k]]
    dp["art_regimen"] = art_regimen

    # facility
    facility = []
    for v in df["facility"].tolist():
        v = str(v).rstrip()
        if v == "nan":
            facility += [None]
            continue
        if v not in facility_cats:
            facility_cats[v] = len(facility_cats) + 1
        facility += [facility_cats[v]]
    dp["facility"] = facility
    # district
    district = []
    for v in df["district"].tolist():
        v = str(v).rstrip()
        if v == "nan":
            district += [None]
            continue
        if v not in district_cats:
            district_cats[v] = len(district_cats) + 1
        district += [district_cats[v]]
    dp["district"] = district
    # province
    province = []
    for v in df["province"].tolist():
        v = str(v).rstrip()
        if v == "nan":
            province += [None]
            continue
        if v not in province_cats:
            province_cats[v] = len(province_cats) + 1
        province += [province_cats[v]]
    dp["province"] = province

    # covid wave
    dp["covid_wave"] = df["covid_wave"]
    # vaccine
    vaccine = []
    for v in visit_date:
        if v == "nan":
            vaccine += [None]
            continue
        vaccine += [int(v)]
    dp["vaccine"] = vaccine

    # rna
    rna = []
    for v in df["rna"].tolist():
        v = str(v)
        if v == "nan":
            rna += [None]
            continue
        r = float(v)
        if r < 60:
            rna += [1]
            continue
        if r < 200:
            rna += [2]
            continue
        if r < 1000:
            rna += [3]
            continue
        if r >= 1000:
            rna += [4]
        raise Exception(f"Unknown rna value: {v}")
    dp["rna"] = rna
    # cd4
    cd4 = []
    for v in df["cd4"].tolist():
        v = str(v)
        if v == "nan":
            cd4 += [None]
            continue
        v = float(v)
        if v < 100:
            cd4 += [1]
            continue
        if v < 350:
            cd4 += [2]
            continue
        if v < 500:
            cd4 += [3]
            continue
        cd4 += [4]
    dp["cd4"] = cd4
    # suppressed
    viremic = []
    for v in df["rna"].tolist():
        v = str(v)
        if v == "nan":
            viremic += [None]
            continue
        v = float(v)
        if v < 1000:
            viremic += [0]
        else:
            viremic += [1]
    dp["viremic"] = viremic
    # death
    death = []
    for v in df["death"].tolist():
        v = str(v)
        if v == "nan":
            death += [None]
            continue
        death += [int(v)]
    dp["death"] = death
    # retention
    retention = []
    for v in df["retention"].tolist():
        v = str(v)
        if v == "nan":
            retention += [None]
            continue
        retention += [int(v)]
    dp["retention"] = retention

    return dp, art_regimen_cats, facility_cats, district_cats, province_cats

def assign_datatypes(df):
    df[df.isnull()] = -1
    
    df["id"] = df["id"].astype(int)
    df["visit_date"] = df["visit_date"].astype(int)
    df["day"] = df["day"].astype(int)
    df["week"] = df["week"].astype(int)
    df["month"] = df["month"].astype(int)
    df["year"] = df["year"].astype(int)

    df["age"] = df["age"].astype(int)
    df["age_cat"] = df["age_cat"].astype(int)
    df["sex_female"] = df["sex_female"].astype(int)

    df["time_in_care"] = df["time_in_care"].astype(int)
    df["official_transfer"] = df["official_transfer"].astype(int)

    df["who_stage"] = df["who_stage"].astype(int)
    df["art_regimen"] = df["art_regimen"].astype(int)

    df["facility"] = df["facility"].astype(int)
    df["district"] = df["district"].astype(int)
    df["province"] = df["province"].astype(int)

    df["covid_wave"] = df["covid_wave"].astype(int)
    df["vaccine"] = df["vaccine"].astype(int)

    df["rna"] = df["rna"].astype(int)
    df["cd4"] = df["cd4"].astype(int)
    df["viremic"] = df["viremic"].astype(int)
    df["death"] = df["death"].astype(int)
    df["retention"] = df["retention"].astype(int)

    return df

def save_codebook(data, name):
    data = dict((v,k) for k,v in data.items())
    keys = sorted(data.keys())
    R = []
    for k in keys:
        R.append((k, data[k]))
    file_name = os.path.join(root, "..", "data", "codebook", name+".csv")
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["value", "description"])
        for r in R:
            writer.writerow(r)

da = None
art_regimen_cats = {}
facility_cats = {}
district_cats = {}
province_cats = {}
for i in tqdm(range(N_BLOCKS)):
    block_n = i + 1
    file_name = os.path.join(raw_data_dir, f"block{block_n}{base_file_name}")
    df = pd.read_csv(file_name)
    dp, art_regimen_cats, facility_cats, district_cats, province_cats = process_data(df, art_regimen_cats=art_regimen_cats, facility_cats=facility_cats, district_cats=district_cats, province_cats=province_cats)
    dp = dp[dp["covid_wave"].notnull()]
    dp = assign_datatypes(dp)
    if da is None:
        da = dp
    else:
        da = pd.concat([da, dp], axis=0)

save_codebook(art_regimen_cats, "art_regimen")
save_codebook(facility_cats, "facility")
save_codebook(district_cats, "district")
save_codebook(province_cats, "province")

da.to_csv(os.path.join(processed_data_dir, f"01_covid_hiv_data.csv"), index=False)
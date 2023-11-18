
# ## Transformation Data


import numpy as np 
import pandas as pd 


# data = pd.read_csv("dataset_1st/training.csv")
def get_mcc_category(mcc_code):
        mcc_code = int(mcc_code)
        
        if 1 <= mcc_code <= 99:
            return "mcc1"
        elif 100 <= mcc_code <= 199:
            return "mcc2"
        elif 200 <= mcc_code <= 299:
            return "mcc3"  # You can continue this pattern for other ranges if needed
        elif 300 <= mcc_code <= 399:
            return "mcc4"
        elif 400 <= mcc_code <= 499:
            return "mcc5"
        else:
            return "unknown"


def trans_data(data):
    base_date = pd.to_datetime("2023-10-02")
    data["locdt"] = base_date + pd.to_timedelta(data["locdt"], unit = "D")


    data["loctm"] = data['loctm'].astype(str).str.zfill(6)
    data['loctm'] = data['loctm'].str[:2] + ":" + data['loctm'].str[2:4] + ":" + data['loctm'].str[4:]
    data["loctm"] = pd.to_datetime(data["loctm"], format = "%H:%M:%S")
    data["loctm"] = data["loctm"].dt.time


    data["lochr"] = data["loctm"].apply(lambda x: x.hour)


    data["combined_datetime"] = pd.to_datetime(data["locdt"].astype(str)+" "+data["loctm"].astype(str))


    contp_dum = pd.get_dummies(data["contp"], prefix = "contp", dtype = int)
    data = pd.concat([data, contp_dum], axis = 1)


    etymd_dum = pd.get_dummies(data["etymd"], prefix = "etymd", dtype = int)
    data = pd.concat([data, etymd_dum], axis = 1)

    data["mcc_cat"] = data["mcc"].fillna(0).apply(get_mcc_category)
    mcc_cat_dum = pd.get_dummies(data["mcc_cat"], prefix = "mcc_cat", dtype = int)
    data = pd.concat([data, mcc_cat_dum], axis = 1)

    data["conam_log"] = np.log(data["conam"] + 1)


    data["flam1_log"] = np.log(data["flam1"] + 1)

    stscd_dum = pd.get_dummies(data["stscd"], prefix = "stscd", dtype = int, dummy_na = True)
    data = pd.concat([data, stscd_dum], axis = 1)

    hcefg_dum = pd.get_dummies(data["hcefg"], prefix = "hcefg", dtype = int, dummy_na = True)
    data = pd.concat([data, hcefg_dum], axis = 1)

    data["csmam_log"] = np.log(data["csmam"] + 1)

    drop_col = ['txkey', 'locdt', 'loctm', 'chid', 'cano', 'contp', 'etymd', 'mchno',
       'acqic', 'mcc', 'conam','flam1', "mcc_cat", 'combined_datetime',
       'stocn', 'scity', 'stscd','csmcu', 'csmam']

    data = data.drop(drop_col, axis = 1).dropna()

    return data

def main():
     data = pd.read_csv("dataset_1st/training.csv")
     data = trans_data(data)

if __name__ == "__main__":
    main()
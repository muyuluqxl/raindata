import pandas as pd
mouth=['pre_06','pre_07','pre_08']
for mouth_idx in mouth:
    for year_idx in range(62):
        MaVread='./AnoCsv/anorain_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        MaVFile = pd.read_csv(MaVread,header=0)
        last_two_columns = MaVFile.iloc[:, -2:]
        
        Prb_rain_add='./PrbCsv/prbrain_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        Ano_stand_add='./standAnoCsv/Anostand_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        Prb_stand_add='./standPrbCsv/Prbstand_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        
        Prb_rain_new = pd.read_csv(Prb_rain_add)
        Prb_rain_new = pd.concat([Prb_rain_new, last_two_columns], axis=1)
        Prb_rain_new.to_csv(Prb_rain_add, index=False)
        
        Ano_stand_new = pd.read_csv(Ano_stand_add)
        Ano_stand_new = pd.concat([Ano_stand_new, last_two_columns], axis=1)
        Ano_stand_new.to_csv(Ano_stand_add, index=False)
        
        Prb_stand_new = pd.read_csv(Prb_stand_add)
        Prb_stand_new = pd.concat([Prb_stand_new, last_two_columns], axis=1)
        Prb_stand_new.to_csv(Prb_stand_add, index=False)
        
"""         last_two_rows.to_csv(Ano_stand_add, mode='a', header=False, index=False)
        last_two_rows.to_csv(Prb_stand_add, mode='a', header=False, index=False) """
    
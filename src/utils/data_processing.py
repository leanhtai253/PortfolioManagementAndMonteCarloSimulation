import pandas as pd
import numpy as np
from functools import reduce
import os

class dp:
    RAW_DATA_PATH = '.../data/raw'
    PROCESSED_DATA_PATH = '.../data/processed'
    FINAL_DATA_PATH = '.../data/final'

    START_DATE = '2020-10-14'
    END_DATE = '2022-10-16'

    @staticmethod
    def transform_data(DATA_PATH, SAVE_PATH, calculate_daily_log_return):
        ind = 0
        for file in os.listdir(DATA_PATH):
            df = dp.preprocessing(DATA_PATH,file, ind, calculate_daily_log_return)
            df.to_csv(os.path.join(SAVE_PATH, file), index=False)
            ind += 1
        print("Successfully save processed files at: ", SAVE_PATH)

    @staticmethod
    def final_data(DATA_PATH, SAVE_PATH, SAVE_NAME):
        companies = []

        date_df = pd.date_range(dp.START_DATE, dp.END_DATE).to_frame().reset_index(drop=True)
        date_df.columns = ['date']
        pd.to_datetime(date_df['date'])
        frames = [date_df]

        for file in os.listdir(DATA_PATH):
            company_name = file[:-4]
            companies.append(company_name)
            df = pd.read_csv(os.path.join(DATA_PATH, file))
            df['date'] = pd.to_datetime(df['date'])
            df = df[['date', 'log_return']]
            df.columns = ['date', company_name]
            frames.append(df)

        df_merged = reduce(lambda left,right: pd.merge(left,right,
                                on=['date'],how='inner'), frames)

        df_merged.to_csv(os.path.join(SAVE_PATH, SAVE_NAME), index=False)
        print(f'Final data is ready at {SAVE_PATH}')

    @staticmethod
    def preprocessing(DATA_PATH, FILENAME, STOCK_INDEX, calculate_daily_log_return):
        df = pd.read_csv(os.path.join(DATA_PATH, FILENAME))
        df = df[['Date', 'Price']]
        df.columns = ['date', 'price']
        df.insert(0, 'name', FILENAME[:-4].lower())
        df['date'] = pd.to_datetime(df['date'], dayfirst=False)
        df['price'] = pd.Series([val for val in df.price]).str.replace('.0','',regex=False).str.replace(',','').apply(pd.to_numeric)
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['stock_id'] = STOCK_INDEX
        df = df.sort_values(by='date').reset_index(drop=True)
        df['log_return'] = calculate_daily_log_return(df['price'])

        return df
    
    
    
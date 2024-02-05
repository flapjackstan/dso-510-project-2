import pandas as pd
import sqlite3 as sq

def csv_to_gzip(csv_path):
     df = pd.read_csv(csv_path)
     df.to_csv(f"{csv_path}.gz",compression='gzip')

def csv_to_sqlite(csv_path,filename):
     df = pd.read_csv(csv_path)
     df = df.drop(columns=["Unnamed: 0"])
     table_name = filename

     conn = sq.connect('{}.sqlite'.format(table_name))
     df.to_sql(table_name, conn, if_exists='replace', index=False)
     conn.close()

def main():
     # csv_to_gzip("./../data/parcel_data.csv")
     csv_to_sqlite("./../data/parcel_data.csv.gz","parcel_data")
     

if __name__ == "__main__":
     main()
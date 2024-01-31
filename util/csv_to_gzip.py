import pandas as pd

def csv_to_gzip(csv_path):
     df = pd.read_csv(csv_path)
     df.to_csv(f"{csv_path}.gz",compression='gzip')

def main():
     csv_to_gzip("./../data/parcel_data.csv")

if __name__ == "__main__":
     main()
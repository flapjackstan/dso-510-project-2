import geopandas as gpd
from census import Census
from us import states
import pandas as pd
import os 

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")
census = Census(CENSUS_API_KEY)

def get_census_data_from_zipcodes(zipcode, variables):
    """Grabs census data as df. look for variables here census.acs5.tables()"""
    zipcode_search = ",".join(zipcode)
    
    census_variables = variables['variables']
    census_rename = variables['rename_variables']
    
    rename = {i:j for i,j in zip(census_variables, census_rename)}
    
    data = census.acs5.state_zipcode(fields = census_variables,
                                          state_fips = states.CA.fips,
                                          zcta = f"{zipcode_search}",
                                          year = 2020)
        
    main_df = pd.DataFrame(data)
    main_df = main_df.rename(columns = rename)
    main_df = main_df.rename(columns = {"zip code tabulation area":"zipcode"})
    main_df["zipcode_str"] = main_df["zipcode"].astype(str)

    print(f"Downloaded data for {len(main_df)} out of {len(zipcode)} zipcodes")
    return main_df

def main():
    zipcodes = gpd.read_file("./../data/lac_zipcodes.geojson")
    zipcodes_list = zipcodes["ZIPCODE"].tolist()

    # stick to la county provided one
    # ca_zip_gdf = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2022/ZCTA520/tl_2022_us_zcta520.zip")
    # zip_gdf = ca_zip_gdf.query("GEOID20 == @zipcodes_list")
    # zip_gdf.to_file("./../data/tiger_lac_zipcodes.geojson", driver='GeoJSON')

    census_variables = {
    'variables': ['NAME', 'B01001_001E'], 
    'rename_variables': ['NAME', 'total_population'],
    'display': ['Tract Name', 'Total Population']}

    census_data = get_census_data_from_zipcodes(zipcodes_list,census_variables)
    census_data.to_csv("./../data/lac_zipcodes_census.csv",index=False)

if __name__ == "__main__":
     main()
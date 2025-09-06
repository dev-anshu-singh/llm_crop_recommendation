import pandas as pd
import config

irrigation_area_file_path = config.IRRIGATION_AREA_PATH
labour_cost_file_path = config.LABOUR_COST_PATH
normal_rainfall_file_path = config.NORMAL_RAINFALL_PATH
crop_production_file_path = config.CROP_PRODUCTION_PATH
ground_water_level_file_path = config.GROUND_WATER_LEVEL_PATH


def clean_groundwater_level_df(df):
    df_2 = df[df['Year'] == '2022-23'].copy()
    import pandas as pd

    df_2["Season"] = df_2["Water Level"].str.extract(r'(Pre Monsoon|Post Monsoon)')
    df_2["Water Level"] = df_2["Water Level"].str.replace(r'(Pre Monsoon|Post Monsoon).*', '', regex=True).str.strip()

    df_wide = df_2.pivot(index=["Year", "State", "District"],
                         columns="Season",
                         values="Water Level").reset_index()

    df_wide = df_wide.rename(columns={
        "Pre Monsoon": "Water Level Premonsoon",
        "Post Monsoon": "Water Level Postmonsoon"
    })

    return df_wide


def clean_rainfall_area_columns(df):
    new_columns = {}
    for col in df.columns:
        if "NORMAL RAINFALL" in col:
            # Extract the month part (first word)
            month = col.split()[0].capitalize()
            # Special case: ANNUAL
            if month == "Annual":
                new_columns[col] = "Annual (mm)"
            else:
                new_columns[col] = f"{month} (mm)"
        else:
            new_columns[col] = col  # keep other columns unchanged

    return df.rename(columns=new_columns)


def remove_last_second_word_column_name(df):
    new_columns = {}
    for col in df.columns:
        if len(col.split()) > 2:
            temp = col.split()
            if 'AREA' in temp:
                temp.remove('AREA')
            if 'PRODUCTION' in temp:
                temp.remove('PRODUCTION')
            new_columns[col] = " ".join(temp)
        else:
            new_columns[col] = col
    return df.rename(columns=new_columns)


def categorize_labour_cost(df):
    # Define bins based on quartiles
    bins = pd.qcut(
        df["DISTRICT MALE FIELD LABOUR (Rs per Day)"],
        q=4,
        labels=["Low", "Low-Medium", "High-Medium", "High"]
    )
    df["labour_cost_category"] = bins
    return df


irrigation_area_df = pd.read_csv(irrigation_area_file_path).drop(
    columns=['Dist Code', 'State Code', 'Year', 'State Name'], axis=1).pipe(remove_last_second_word_column_name)
labour_cost_df = pd.read_csv(labour_cost_file_path).pipe(categorize_labour_cost).drop(
    columns=['Dist Code', 'Year', 'State Code', 'DISTRICT MALE FIELD LABOUR (Rs per Day)', 'State Name'], axis=1)
normal_rainfall_df = pd.read_csv(normal_rainfall_file_path).drop(
    columns=['Dist Code', 'State Code', 'Year', 'State Name'], axis=1).pipe(clean_rainfall_area_columns)
crop_production_df = pd.read_csv(crop_production_file_path).drop(
    columns=['Dist Code', 'State Code', 'Year', 'State Name'], axis=1).pipe(remove_last_second_word_column_name)
ground_water_level_df = pd.read_excel(ground_water_level_file_path).pipe(clean_groundwater_level_df).drop(
    columns=['Year', 'State'], axis=1).rename(
    columns={'District': 'Dist Name', 'Water Level Postmonsoon': 'Water Level Postmonsoon (in mbgl)',
             'Water Level Premonsoon': 'Water Level Premonsoon (in mbgl)'})

datasets = {
    'normal_rainfall': normal_rainfall_df,
    'irrigation_area_from_different_sources': irrigation_area_df,
    'labour_cost': labour_cost_df,
    'production_of_crops': crop_production_df,
    'groundwater_level': ground_water_level_df
}


def get_district_info(district_name) -> dict:
    """
    Returns a dictionary of all information for a given district
    from multiple datasets.

    Parameters:
        district_name (str): Name of the district to search for
        datasets (dict): Dictionary of {dataset_name: dataframe}
                         Each dataframe must contain a 'Dist Name' column

    Returns:
        dict: Combined information for that district
    """

    district_info = {"Dist Name": district_name}

    for name, df in datasets.items():
        # Filter for the district (case-insensitive match)
        row = df[df["Dist Name"].str.lower() == district_name.lower()]

        if not row.empty:
            # Take the first match (if multiple rows exist)
            data = row.iloc[0].to_dict()
            # Remove duplicate 'Dist Name'
            data.pop("Dist Name", None)

            # Store in the result dict under dataset name
            district_info[name] = data
        else:
            district_info[name] = None  # No data found

    return district_info

# print(get_district_info('Khagaria'))


import pandas as pd
import re
from numpy import where 

from data_cleaning import format_dataframe
from sharks import shark_list

def injury_classification(df):
    """
    Clasifies injury data into fatal & non-fatal categories
    argument: df - the shark attack dataframe for injuries
    return : df with injury classification
    """
    # Detect strings that contain "fatal" (case insensitive) pattern
    detected_pattern = df['injury'].str.contains(r'(?<!non-)fatal', case=False, na=False)

    # Replace non-matching values with default value of non-fatal
    df['injury'] = where(detected_pattern, 'fatal', "non-fatal")

    # Format values to title case
    df['injury'] = df.loc[:, 'injury'].str.title()

    return df

def species_extract(df, pattern):
    """
    Helper function to extract sharks from formatted dataframe
    args: df - shark dataframe to extract species
               pattern - pattern with species to extract
    return: shark df with species name or null dataframe
    """

    filtered_df = df[df.loc[:, "species"].str.contains(pattern, case = False, regex = True)]

    # Resetting index for new df
    filtered_df.reset_index(drop=True, inplace=True)
    # Extracts the pattern in the column value and sets its as new value
    try:
        filtered_df["species"] = filtered_df.loc[:, "species"].str.extract(pattern, flags=re.IGNORECASE)
    except ValueError:
        print(f'No entries for {pattern}, skippped')
        return pd.DataFrame({"species" : []})

    # Formats column values to title format
    filtered_df["species"] = filtered_df.loc[:, "species"].str.title()

    return filtered_df

def visualize_data(shark_df):
    """ 
    Main function to get visualization ready data for notebook 
    args: shark_df - shark attack dataframe
    return: visualize ready dataframe in shark_data
    """
    shark_df = format_dataframe(shark_df)

    species_dfs = [species_extract(shark_df,shark) for shark in shark_list()]
    species_dfs = [species for species in species_dfs if not species.empty]
    
    shark_data = pd.concat(species_dfs, axis=0)

    shark_data = injury_classification(shark_data)

    shark_data.reset_index(drop=True, inplace=True)
    
    return shark_data
  
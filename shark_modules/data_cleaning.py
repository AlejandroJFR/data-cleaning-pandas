import pandas as pd
import re

def get_sharks(text):
    """Helper function for filter_species
        Uses regex to filter shark column data 

        Argument: text - str representing data in sharks column
        Returns: Filtered text with shark id or no id or 
                 no confirmation of shark attack
    """
    shark_pattern = r'(\b(?<![\d.m\'])'+ r'(?![\d.m\'])' + r'\w+(?:\s\w+){0,1}\b)\s+shark[s]*'
    no_confirm_pattern = r'(?:\b(?:no confirmation|not confirmed|unconfirmed|questionable|\?)\s*\b)'
    unidentified_pattern = r'([\d.m\']|to|\]|\[)+|[uU]nidentified|[qQ]uestionable'
    filter_pattern = r'[^a|or|to|for|but|the]\s+shark[s]*'

    output = text
    if re.search(no_confirm_pattern, text):
      return 'N/A'

    find = re.findall(shark_pattern,text)
    unidentified = re.findall(unidentified_pattern, text)
    for i,f in enumerate(find):
      find[i] = re.sub(filter_pattern,'', find[i])

    if unidentified: 
      return 'species unidentified'

    if find and find[0] and len(find) == 1:
      output = find[0] + ' shark'

    return output

def filter_species(shark_species):
    """
    Filters entries of species column of dataset using regex patterns:

    Argument : shark_species: pd.series - 
               the species column to filter entries
    Returns : shark_species: pd.series - 
              the filtered species column
    """
    shark_species.fillna('N/A', inplace=True) 
    shark_species = shark_species.apply(lambda x: re.sub(r'\s+', ' ', x)) 
    shark_species = shark_species.str.replace(r"\"", r"",regex=True) 
    shark_species = shark_species.apply(get_sharks)
    return shark_species

def format_dataframe(shark_df):
    """
    Formats/cleans the dataframe with steps :
       1. strip leading/trailing spaces and lowercase IN COLUMNS
       2. drop all columns except the neccesities: 'species', 'injury', 'activity','type' 
       3. filter trail/lead spaces + lowercase) string values in dataframe
       4. clean out type column with replacements for similar values
       5. clean and filter shark regex function
       6. return cleaned dataframe for use in extraction.py

    Argument : shark_df - the dataframe to clean/format for use in analysis/visulization
    Returns : the cleaned & formatted dataframe
    """

    # 1 
    clean_strings = lambda x: x.strip().lower() if isinstance(x,str) else x
    shark_df.columns = pd.Series(shark_df.columns).apply(lambda col: col.strip().lower())
    # 2
    keep = set(['species', 'injury', 'activity','type'])
    drop_cols = [col for col in shark_df.columns if col not in keep]
    shark_df.drop(columns=drop_cols, inplace = True)

    # 3
    shark_df = shark_df.applymap(clean_strings)

    #4 
    type_replace = {'Boat':'Watercraft', 'Under investigation':'Unverified', '?': 'Questionable'}
    shark_df['type'] = shark_df['type'].replace(type_replace)
    

    #5 
    shark_df.species = filter_species(shark_df['species'])

    # 6 
    return shark_df
import glob
import pandas as pd

# get a list of all csv files in the current directory
def combine_csv():
    csv_files = glob.glob('*.csv')


    # combine all csv files into a single dataframe
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files])

    # write the combined dataframe to a new csv file
    combined_df.to_csv('combined_851_new.csv', index=False)
    

def add_column():
    csv_files = glob.glob('*.csv')
    for csv in csv_files:
        print(csv)
        search_title = csv.replace('_', ' ').replace('.csv','')
        csv_input = pd.read_csv(csv)
        new_col = [search_title]*len(csv_input)
        try:
            csv_input.insert(0, 'Search_titles', new_col)
        except:
            print(f'{csv} Search_titles already exist')
        path = f'new\{csv}'
        csv_input.to_csv(path, index=False)
        print(f'{csv} is done')


combine_csv()
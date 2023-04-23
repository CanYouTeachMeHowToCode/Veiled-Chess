# NN-based content filtering recommendation model
import pandas as pd
import os 

# automatically remove all .DS_Store files
def removeTmpFiles(path):
    if path.split("/")[-1] == '.DS_Store': os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path): removeTmpFiles(path + "/" + filename)

# list all files within given folder
def listFile(path):
    if not os.path.isdir(path): return path
    else: return [listFile(path + "/" + filename) for filename in os.listdir(path)]

def loadAndProcessData(files):
    '''
    Load dataframes from all csv files in data folder, merge them together, and filter
    out all rows that has a zero scores (either indicates meaningless draw situations 
    or not applicable evaluation scores from stockfish due to time and depth limitations)

    Input:
        files (List[str]): file paths to csv files
    
    Output:
        df (pd.DataFrame): output merged dataframe that filtered out all zero score rows
    '''
    df = pd.DataFrame(columns=['board', 'player', 'gameInfo', 'score'])
    for file in files:
        curr_df = pd.read_csv(file)
        df = pd.concat([df, curr_df])
    df = df.loc[df['score'] != 0.0]
    df.reset_index(inplace=True)
    df.drop(['index', 'Unnamed: 0'], axis=1, inplace=True)
    return df

if __name__ == '__main__':
    files = listFile('data')
    df = loadAndProcessData(files)
    print(df)
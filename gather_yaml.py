#!/usr/bin/env python3

"""
Combine params.yaml from different model
"""

import pandas as pd
import yaml
from pathlib import Path


def concatenate_files(file_list):
    """
    concatenate all files from a list
    """
    appended_data = []
    for yf in file_list:
        with open(yf, 'r') as f:
    	    df = pd.json_normalize(yaml.load(f, Loader=yaml.FullLoader))

        df.rename(columns={'Unnamed: 0': 'title'}, inplace=True)
        df['model'] = Path(yf).parts[-2]
        appended_data.append(df)

    df_all = pd.concat(appended_data)
    return df_all


def main():

    top_dir = '../OUTPUT_20210617_22-57-30'
    top_model = ['BERT_base_uncased',  'multinomial_naive_bayes', 'simple_LSTM']

    classification_files = list(Path(top_dir).glob('**/params.yaml'))
    # remove refactor stuff
    classification_files_new = [str(f) for f in classification_files if 'refactor' not in str(f)]

    # gather data
    df_all = concatenate_files(classification_files_new)
    df_all.to_csv('params.csv', sep='\t', index=False)


if __name__ == '__main__':
    main()

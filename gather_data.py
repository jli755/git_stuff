#!/usr/bin/env python3

"""
Combine data from different model
"""

import pandas as pd
from pathlib import Path
from matplotlib import ticker 
import matplotlib.pyplot as plt

def concatenate_files(file_list):
    """
    concatenate all files from a list
    """
    appended_data = []
    for f in file_list:
        df = pd.read_csv(f, sep=',')
        df.rename(columns={'Unnamed: 0': 'title'}, inplace=True)
        df['model'] = Path(f).parts[-2]
        appended_data.append(df)

    df_all = pd.concat(appended_data)  
    return df_all


def simple_plot(df_wide, yl):
    """
    example plot
    """
    df_wide.plot(kind='bar')
    plt.ylabel(yl) 
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('$%.2f')) 
    plt.gca().xaxis.set_tick_params(rotation=0)
    plt.xticks(rotation=90)

    plt.show()


def main():

    top_dir = '../OUTPUT_20210603_08-38-24'
    top_model = ['BERT_base_uncased',  'multinomial_naive_bayes', 'simple_LSTM']

    classification_files = list(Path(top_dir).glob('**/classification_report.csv'))
    # remove refactor stuff
    classification_files_new = [str(f) for f in classification_files if 'refactor' not in str(f)]
    
    # gather data
    df_all = concatenate_files(classification_files_new)
    df_all.to_csv('classification_report.csv', sep='\t', index=False)

    # example plot for precision in BERT 
    df_precision = df_all.loc[(df_all.model.str.startswith('BERT')), ['title', 'precision', 'model']]
    print(df_precision['model'].unique())
    # reshape long to wide
    df_wide = df_precision.pivot_table(index=['title'],
                                 columns='model',  
                                 values='precision')
    
    simple_plot(df_wide, 'precision')


if __name__ == '__main__':
    main()

# Import packages
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref_indices')
    parser.add_argument('--test_indices')
    parser.add_argument('--results_csv')
    parser.add_argument('--comparison_pdf')
    args = parser.parse_args()

    # Input / Output file paths
    ## Input
    ref_indices = pd.read_csv(args.ref_indices,
                            sep=',')
    test_indices = pd.read_csv(args.test_indices,
                            sep=',')

    ## Output
    results_csv = args.results_csv
    comparison_pdf = args.comparison_pdf

    # -------------------------------- Script ------------------------------- #

    # Make sure the column names for the data set are fine ['name', 'i7', 'i5']
    if not ref_indices.columns.to_list().sort() == \
        test_indices.columns.to_list().sort():
        raise ValueError(
            """
            ref_indices or test_indices csv are not in the right format
            """)

    # Calculate the hamming distance, all in ref vs all in test
    def calculate_hamming_distance_index_sets(ref_set='',
                                            test_set=''):
        
        # Define small helper function
        def calc_hamming_dist(seq_1, seq_2):
            if len(seq_1) != len(seq_2):
                raise ValueError('Indices must have equal length')
            
            # Initiate the counting
            dist_counter = 0

            for ix in zip(seq_1, seq_2):
                if ix[0] != ix[1]:
                    dist_counter += 1
        
            return dist_counter

        # Prepare data
        ref_set = ref_set.copy()
        test_set = test_set.copy()

        ref_set = ref_set.set_index('name')
        test_set = test_set.set_index('name')

        # Do the calculations
        res_df = []

        for _index in ['i7', 'i5']:
            _df = []

            # Do the testing
            for ix, row in test_set.iterrows():
                ans = ref_set[_index].apply(
                    func=lambda w: calc_hamming_dist(seq_1=w,
                                                    seq_2=row[_index]))   
                ans.name = ix
                _df.append(ans)
            
            # Bring data into shape
            _df = pd.concat(_df, axis=1)
            _df.columns.name = 'test-index-name'
            _df.index.name = 'ref-index-name'

            _df = _df.stack()\
                    .rename(f'{_index}_hamming_distance')

            res_df.append(_df)

        res_df = pd.concat(res_df, axis=1)\
                .reset_index()

        return res_df


    # Save to file
    ref_df = calculate_hamming_distance_index_sets(ref_set=ref_indices,
                                                test_set=test_indices)
    ref_df.to_csv(results_csv, sep=',', index=False)

    # Plot results
    ## Bring data in right format
    ref_df = ref_df.set_index(['ref-index-name', 'test-index-name'])
    ref_df = ref_df.stack()\
                .reset_index()\
                .rename({'level_2':'index',
                            0:'hamming_distance'},
                        axis=1)

    fg1 = sns.displot(data=ref_df,
                    x='hamming_distance',
                    # col='ref-index-name',
                    col='test-index-name',
                    col_wrap=3,
                    hue='index',
                    multiple='dodge',
                    fill=True,
                    discrete=True,
                    shrink=0.8,
                    aspect=2.6,
                    height=1.8)

    # Fix figure aesthetics
    fg1.despine(right=False,
            top=False)
    fg1.refline(x=3.5, 
                color='red', 
                linestyle='-', 
                linewidth=3)

    # Save to file
    fg1.savefig(comparison_pdf, 
                dpi=300,
                bbox_inches='tight')
    

if __name__ == "__main__":
    main()
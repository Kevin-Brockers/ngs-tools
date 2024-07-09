# Calculate the index distance
- This small script will compute the distances between two sets of indices.

1. Install the `conda-env.yaml`
    - `conda env create -f conda-env.yaml`
    - `conda activate ngs-tools-python`

2. Parse the indice lists in csv format.
    - Both lists should have the following columns:
        1. name
        2. i7
        3. i5

3. Run the calculate distance script:
    - `python3.9 --test_set '' 
                 --reference_set ''
                 --comparison_csv ''
                 --comparison_pdf ''`
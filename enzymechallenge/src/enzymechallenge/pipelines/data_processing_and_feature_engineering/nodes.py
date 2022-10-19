"""
This is a boilerplate pipeline 'data_processing_and_feature_engineering'
generated using Kedro 0.18.3
"""

import pandas as pd

def CountFrequency(amino_list: list) -> list:
    """helper node for counting amino acid frequency.

    Args:
        amino_list: list.
    Returns:
        dictionary containing each amino acid as key and frequency as value
    """
    freq = {}
    for items in amino_list:
        freq[items] = amino_list.count(items)
    return freq


def preprocess_train(train: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the training data.

    Args:
        train: Raw data.
    Returns:
        Preprocessed train with protein length and percentage of each amino acid in the protein
    """
    train["prot_len"] = train.apply(lambda row: len(str(row["protein_sequence"])), axis=1)
    count_amino_df = pd.DataFrame.from_dict(list(train["protein_sequence"].apply(lambda x: CountFrequency(list(str(x))))))
    train = pd.concat([train,count_amino_df], join = 'outer', axis = 1)
    train.drop(columns = ['.','7','4','3'], inplace = True)
    train.iloc[:,6:] = train.iloc[:,6:].div(train.prot_len, axis=0)
    return train

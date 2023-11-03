import numpy as np
import tempfile
import pandas as pd

import pytest

import comsol_to_h5

@pytest.fixture
def one_d_df() -> pd.DataFrame:
    """fixture for generating 1d data frame 

    Returns:
        pd.DataFrame: data frame from 1D simulation
    """
    return comsol_to_h5.read_from_comsol_native_csv('test_files/decaying_sin.csv')


def test_correct_column_names_1d(one_d_df) -> None:
    correct_col_names = "X;u @ t=0, offset=0;u @ t=0.1, offset=0;u @ t=0.2, offset=0;u @ t=0.3, offset=0;u @ t=0.4, offset=0;u @ t=0.5, offset=0;u @ t=0.6, offset=0;u @ t=0.7, offset=0;u @ t=0.8, offset=0;u @ t=0.9, offset=0;u @ t=1, offset=0;u @ t=0, offset=1.5708;u @ t=0.1, offset=1.5708;u @ t=0.2, offset=1.5708;u @ t=0.3, offset=1.5708;u @ t=0.4, offset=1.5708;u @ t=0.5, offset=1.5708;u @ t=0.6, offset=1.5708;u @ t=0.7, offset=1.5708;u @ t=0.8, offset=1.5708;u @ t=0.9, offset=1.5708;u @ t=1, offset=1.5708".split(';')

    for col_name_test, col_name_df in zip(correct_col_names, one_d_df.columns):
        assert col_name_test == col_name_df


def test_correct_X_read_in_1d(one_d_df) -> None:
    # positions are 0 to 2*pi in file, should be same in df
    num_entries_X = len(one_d_df["X"])
    
    # set up test array. rounding of both test array and df values is necessary
    # as data set is not full precision.
    approximate_correct_positions = np.array([round(i/float(num_entries_X)*2.*np.pi +
                                                    np.pi/float(num_entries_X),4)
                                              for i in range(num_entries_X)])
    for x_test, x_df in zip(approximate_correct_positions, one_d_df["X"]):
        assert x_test == round(x_df,4)


def test_correct_val_read_in_1d(one_d_df) -> None:
    for state_name in one_d_df.columns:
        if state_name != "X":
            # initial is sin + 1, such that mean should always be 1.
            # applying rather liberal approximation due to disabled full precision 
            # in test data set.
            assert one_d_df[state_name].mean() == pytest.approx(1., rel=1e-5)

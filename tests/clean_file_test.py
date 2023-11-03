import numpy as np
import tempfile
import pandas as pd

import pytest

import comsol_to_h5


@pytest.fixture
def temporary_test_txt_file():
    """fixture for temporary text file

    Yields:
        str: path to temporary file
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # use clean_file() to write cleaned file which can be probed further by
        # tests
        temp_file = temp_dir + '/test_file_1.txt'
        # column description line of test_files/decaying_pi.txt is L 7
        comsol_to_h5.clean_file('test_files/decaying_pi.txt', temp_file, column_description_line=7)

        yield temp_file

@pytest.fixture
def test_df() -> pd.DataFrame:
    """fixture for probing proper format of read-in df after clean_file() is
    called

    Returns:
        pd.DataFrame: df from cleaned file
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # generate df from cleaned file from test_files/decaying_pi.txt to test
        # if it is read in properly into df
        temp_file = temp_dir + '/test_file_1.txt'
        comsol_to_h5.clean_file('test_files/decaying_pi.txt', temp_file)
        return comsol_to_h5.read_from_comsol_native_csv(temp_file)


def test_pandas_import(temporary_test_txt_file):
    """test whether pandas can read in data from cleaned text file

    Args:
        temporary_test_txt_file (_type_): cleaned temporary file fixture
    """
    try:
        df = pd.read_csv(temporary_test_txt_file, header = 7, delimiter = ';')
    except Exception as exc:
        assert False, f" raised exception {exc}"

def test_read_in_description_line(test_df):
    """test whether the right column descriptions are read out

    Args:
        test_df (_type_): test df fixture
    """
    columns = 'X;u @ t=0, offset=0;u @ t=0.1, offset=0;u @ t=0.2, offset=0;u @ t=0.3, offset=0;u @ t=0.4, offset=0;u @ t=0.5, offset=0;u @ t=0.6, offset=0;u @ t=0.7, offset=0;u @ t=0.8, offset=0;u @ t=0.9, offset=0;u @ t=1, offset=0;u @ t=0, offset=1.5708;u @ t=0.1, offset=1.5708;u @ t=0.2, offset=1.5708;u @ t=0.3, offset=1.5708;u @ t=0.4, offset=1.5708;u @ t=0.5, offset=1.5708;u @ t=0.6, offset=1.5708;u @ t=0.7, offset=1.5708;u @ t=0.8, offset=1.5708;u @ t=0.9, offset=1.5708;u @ t=1, offset=1.5708'.split(';')
    for col_test, col_df in zip(columns, test_df.columns):
        assert col_test == col_df

def test_row_number_df(test_df):
    """test whether pandas read out right number of rows

    Args:
        test_df (_type_): test df fixture
    """
    assert len(test_df) == 64

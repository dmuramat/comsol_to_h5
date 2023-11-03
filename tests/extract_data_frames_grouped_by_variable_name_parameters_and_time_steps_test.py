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

@pytest.fixture
def one_d_test_ordered_dict(one_d_df) -> dict:
    """fixture for providing the ordered dict returned by 
    extract_data_frames_grouped_by_variable_name_parameters_and_time_steps

    Args:
        one_d_df (pandas.DataFrame): data frame supplied by one_d_df fixture            

    Returns:
        dict: ordered dict with one-d test data
    """
    return comsol_to_h5.extract_data_frames_grouped_by_variable_name_parameters_and_time_steps(
        one_d_df
    )

def test_read_out_of_variables(one_d_test_ordered_dict):
    assert set(one_d_test_ordered_dict) == {'positions','u'}

def test_read_out_of_parameter_names(one_d_test_ordered_dict):
    # print(one_d_test_ordered_dict)
    for variable_name, content in one_d_test_ordered_dict.items():
        # at present, this is only 'u'
        if variable_name != 'positions':
            assert set(content) == {'offset=0', 'offset=1.5708'}

def test_read_out_of_time_step_names(one_d_test_ordered_dict):
    for variable_name, content in one_d_test_ordered_dict.items():
        # at present, this is only 'u'
        if variable_name != 'positions':
            for parameter_name, time_steps in content.items():
                test_set = {'t='+str(i/10.) for i in range(1,10)}
                test_set.add('t=0')
                test_set.add('t=1')
                assert set(time_steps) == test_set

def test_read_out_of_time_step_states(one_d_test_ordered_dict):
    for variable_name, content in one_d_test_ordered_dict.items():
        # at present, this is only 'u'
        if variable_name != 'positions':
            for parameter_name, time_steps in content.items():
                # time steps of this specific data set should all have mean 1.
                for _, time_step in time_steps.items():
                    assert np.mean(time_step) == pytest.approx(1., rel=1e-5)

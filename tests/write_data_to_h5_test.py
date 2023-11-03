import tempfile
import numpy as np
import pandas as pd
import h5py

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


@pytest.fixture
def parameters_1d_test_file() -> dict:
    """fixture for generating the parameter dict for 1d test file

    Returns:
        dict: parameter dict
    """
    return comsol_to_h5.extract_parameters_static('test_files/decaying_pi_ParametersStatic.txt')


@pytest.fixture
def h5_file_from_1d_test_data(one_d_df, parameters_1d_test_file):
    """fixture for generating a temporary hdf5 file from 1d test data set

    Args:
        one_d_test_ordered_dict (dict): dict from 1d test data set fixture
        parameters_1d_test_file (dict): dict with parameters from its fixture

    Yields:
        h5py.File: opened hdf5 file with data from 1d test data set written into it
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = temp_dir + '/test_file_1.h5'
        comsol_to_h5.write_data_to_h5(one_d_df, temp_file, 
                                         parameters_static=parameters_1d_test_file)

        yield h5py.File(temp_file, 'r')


def test_variable_naming_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    assert ({name for name in h5_file_from_1d_test_data} ==
            set(one_d_test_ordered_dict))


def test_parameter_naming_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    for name, content in one_d_test_ordered_dict.items():
        if name != 'positions':
            assert ( set(h5_file_from_1d_test_data[name]) ==
                    set(content))


def test_time_step_naming_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    for var_name, par_sets in one_d_test_ordered_dict.items():
        if var_name != 'positions':
            for par_name, time_steps in par_sets.items():
                assert( set(h5_file_from_1d_test_data[var_name + '/' + par_name]) ==
                       set(time_steps))


def test_dimension_naming_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    # one_d_test_ordered_dict['positions'] has the axes names, but also a tuple of all position
    # points ('X',) which is not written to the hdf5 file. At a later point, this may be useful
    # to write a non-cartesian grid to file (not implemented). This is excluded from the assert
    dimension_names = {dimension_name for  dimension_name in one_d_test_ordered_dict['positions'] if
                        not isinstance(dimension_name, tuple)}
    assert set(h5_file_from_1d_test_data['positions']) == dimension_names


def test_positions_values_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    # one_d_test_ordered_dict['positions'] has the axes names, but also a tuple of all position
    # points ('X',) which is not written to the hdf5 file. At a later point, this may be useful
    # to write a non-cartesian grid to file (not implemented). This is excluded from the assert
    dimension_names = {dimension_name for  dimension_name in one_d_test_ordered_dict['positions'] if
                        not isinstance(dimension_name, tuple)}
    for dim_name in dimension_names:
        assert (h5_file_from_1d_test_data['positions'][dim_name][:] ==
                one_d_test_ordered_dict['positions'][dim_name]).all()


def test_variable_values_1d(h5_file_from_1d_test_data, one_d_test_ordered_dict) -> None:
    # test whether time steps are written correctly
    for var_name, par_sets in one_d_test_ordered_dict.items():
        if var_name != 'positions':
            for par_name, time_steps in par_sets.items():
                for time_step_name, values in time_steps.items():
                    data_set_name = var_name + '/' + par_name + '/' + time_step_name
                    assert (h5_file_from_1d_test_data[data_set_name][:] == values).all()

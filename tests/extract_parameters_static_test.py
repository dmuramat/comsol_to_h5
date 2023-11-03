import tempfile

import pytest

import comsol_to_h5

@pytest.fixture
def parameter_test_dict() -> dict:
    """fixture for generating the parameter dict for 1d test file

    Returns:
        dict: parameter dict
    """
    return comsol_to_h5.extract_parameters_static('test_files/decaying_pi_ParametersStatic.txt')

def test_name_recognition(parameter_test_dict):
    for name in ['offset', 'L', 'dL']:
        assert name in parameter_test_dict

def test_value_read_in(parameter_test_dict):
    test_dict = {'offset': 1.57079, 'L': 6.283185, 'dL': 3.1415922e-2}

    for name, value in parameter_test_dict.items():
        assert test_dict[name] == pytest.approx(value)

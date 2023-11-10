import pytest
import comsol_to_h5

def test_integration_of_one_dict():
    dict_a = {"a": 1}
    target_dict = {}

    comsol_to_h5.group_dict_into_dict_tree(dict_a, target_dict)

    assert target_dict == dict_a


def test_first_layer_grouping():
    # test the first layer of dict grouping
    dict_list = [{"a": 1}, {"b": 2}, {"c": 3}]
    target_dict = {}

    for entry in dict_list:
        comsol_to_h5.group_dict_into_dict_tree(entry, target_dict)

    assert target_dict == {"a": 1, "b": 2, "c": 3}


def test_second_layer_grouping():
    dict_1 = {"a" : {"n": 1}}
    dict_2 = {"a" : {"m": 2}}
    target_dict = {}

    comsol_to_h5.group_dict_into_dict_tree(dict_1, target_dict)
    comsol_to_h5.group_dict_into_dict_tree(dict_2, target_dict)

    assert target_dict == {"a": {"n": 1, "m": 2}}


def test_multilevel_grouping():
    dict_1 = {"a" : {"n": 1}}
    dict_2 = {"a" : {"m": 2}}
    dict_3 = {"b" : {"i": 4}}
    dict_4 = {"b" : {"j": 5}}
    target_dict = {}

    comsol_to_h5.group_dict_into_dict_tree(dict_1, target_dict)
    comsol_to_h5.group_dict_into_dict_tree(dict_2, target_dict)
    comsol_to_h5.group_dict_into_dict_tree(dict_3, target_dict)
    comsol_to_h5.group_dict_into_dict_tree(dict_4, target_dict)

    assert target_dict == {"a": {"n": 1, "m": 2},
                           "b": {"i": 4, "j": 5}}


def test_exception_upon_duplicate_data_from_input():
    dict_1 = {"a" : {"n": 1}}
    dict_2 = {"a" : 2}
    target_dict = {}

    comsol_to_h5.group_dict_into_dict_tree(dict_1, target_dict)
    with pytest.raises(TypeError) as error:
        comsol_to_h5.group_dict_into_dict_tree(dict_2, target_dict)


def test_exception_upon_duplicate_data_from_target_dict():
    dict_1 = {"a" : 2}
    dict_2 = {"a" : {"n": 1}}
    target_dict = {}

    comsol_to_h5.group_dict_into_dict_tree(dict_1, target_dict)
    with pytest.raises(TypeError) as error:
        comsol_to_h5.group_dict_into_dict_tree(dict_2, target_dict)

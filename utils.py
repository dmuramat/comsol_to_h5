"""Utils for comsol_to_h5. Contains:
group_dict_into_dict_tree
"""

def group_dict_into_dict_tree(source_dict: dict, target_dict: dict, 
                              ignore_duplicate_names = False) -> None:
    """Groups source_dict which may be a hierarchy of dicts into the hierarchy
    of target_dict. Alters target_dict directly as pass by reference.

    Args:
        source_dict (dict): dict to be grouped into hierarchy of target_dict.
        target_dict (dict): Is altered, as passed by reference.
        ignore_duplicate_names (bool, optional): Source and target dict may contain duplicate
        values. If this is known, this variable can be set to True. Defaults to False.

    Raises:
        TypeError: If either the source_dict or the target_dict contain duplicate
        keys and ignore_duplicate_names = False, then these keys can only be merged when their
        corresponding values are also both dicts.
    """
    for name, contents in source_dict.items():

        if name in target_dict:
            # group dicts recursively
            if isinstance(contents, dict):
                if isinstance(target_dict[name], dict):
                    group_dict_into_dict_tree(contents, target_dict[name], ignore_duplicate_names)
                else:
                    # check if contents already exist. some data do not vary between
                    # different dicts, in which case one can safely ignore the duplicates.
                    if not ignore_duplicate_names:
                        raise TypeError("target_dict item \'" + name + "\'has duplicate value" +
                                        " and is not a dict")
            else:
                # check if contents already exist. some data do not vary between
                # different dicts, in which case one can safely ignore the duplicates.
                if not ignore_duplicate_names:
                    raise TypeError("source_dict item \'" + name + "\'has duplicate value" +
                                        " and is not a dict")

        # if the element does not exist yet, make new element
        else:
            target_dict[name] = contents
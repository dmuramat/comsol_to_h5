
def group_dict_into_dict_tree(source_dict: dict, target_dict: dict, 
                              ignore_duplicate_names = True) -> None:
    for name, contents in source_dict.items():
        
        # group dicts recursively
        if isinstance(contents, dict):
            if name in target_dict:
                if isinstance(target_dict[name], dict):
                    group_dict_into_dict_tree(contents, target_dict[name])
                    
                else:
                    raise TypeError
                
            else:
                target_dict[name] = contents
        
        else:
            # check if contents already exist. some data do not vary between 
            # different dicts, in which case one can safely ignore the duplicates.
            if name in target_dict:
                if not ignore_duplicate_names:
                    raise TypeError
                
            else:
                target_dict[name] = contents
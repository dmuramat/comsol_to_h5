import numpy as np
import pandas as pd
import h5py

def extract_parameters_static(parameter_file_name: str) -> dict:
    """extract parameters which are not sweeped over and output to dict

    Args:
        parameter_file_name (str): parameter file name, parameters may have integer or 
        decimal form, mathematical / natural constants are not recognized (at this point).

    Returns:
        dict: dict of the format {"<parameter_name>": <parameter value>}
    """
    parameters_static = {}

    with open(parameter_file_name, 'r') as handle:
        for line in handle.readlines():
            par_name = line.split(' ')[0]
            par_value = float(line.split(' ')[1])
            parameters_static[par_name] = par_value

    return parameters_static


def read_from_comsol_native_csv(file_name: str) -> pd.DataFrame:
    """detects start of header and reads file into pandas df with column naming

    Args:
        file_name (str): path to comsol-native csv file

    Returns:
        pd.DataFrame: df that can be processed by extract_data_frames_grouped_by_variable_name_parameters_and_time_steps
    """
    # detect start of header by looking for motif "% X" which demarcates begin of 
    # column description line in COMSOl spreadsheat format files
    column_description_line = 0
    with open(file_name, 'r') as handle:
        line = handle.readline()
        while line[:3] != "% X":
            column_description_line += 1 
            line = handle.readline()

    df = pd.read_csv(file_name, delimiter=';', header = column_description_line)

    # replace the "% X" column name with "X"
    df = df.rename(columns={"% X": "X"})

    return df


def extract_data_frames_grouped_by_variable_name_parameters_and_time_steps(source_df: pd.DataFrame) -> dict:
    """structures pandas data frame from comsol format into dict

    Args:
        source_df (pd.DataFrame): data frame read out form comsol output after cleaning file with 
        clean_file()

    Raises:
        KeyError: time step is recorded twice for same variable name and parameter
        KeyError: time step is missing

    Returns:
        dict: dictionary structured by 
        {"variable name": {"parameter_name": {"time_step_name": <time step:numpy array>}}}
    """
    column_names_df = source_df.columns
    variable_names = [name for name in list(set([name.split(' @ ')[0] for name in column_names_df])) 
                      if name not in ['X', 'Y', 'Z']]
    dimension_names = [name for name in column_names_df if name in ['X', 'Y', 'Z']]

    dimension_positions = {}
    for dimension_name in dimension_names:
        #np.unique already sorts
        dimension_positions[dimension_name] = np.unique(source_df[dimension_name].to_numpy())

    grouped_by_var_name = {}
    grouped_by_var_name["positions"] = dimension_positions
    grouped_by_var_name["positions"][tuple(dimension_names)] = source_df[dimension_names].to_numpy()

    for variable_name in variable_names:
        columns_with_variable = [name for name in column_names_df if variable_name + ' @ ' in name]
        grouped_by_param_set = {}
        # column name is '<var_name> @ <time>, par1, par2, ...'
        # split off anything before first variable information:
        parameter_values = list(set([name[len(name.split(', ')[0]) +2:]
                                     for name in columns_with_variable]))

        for par_val in parameter_values:
        # column name is '<var_name> @ <time>, par1, par2, ...'
        # split off time information:
            time_step_names = list(set([name.split(' @ ')[1].split(',')[0]
                                        for name in columns_with_variable if par_val in name]))
            time_step_dict = {}
            for t_step_name in time_step_names:
                #express column name as list
                column_name = [name for name in columns_with_variable if (par_val in name)
                               and (t_step_name == name.split(' @ ')[1].split(', ')[0])]
                #check whether there is only one entry
                if len(column_name) > 1:
                    print(column_name)
                    raise KeyError("time step" + t_step_name + "is represented with " +\
                                   "two entries for " + par_val)
                if len(column_name) == 0:
                    raise KeyError("no time step for " + par_val)

                column_name = column_name[0]
                time_step_dict[t_step_name] = source_df[column_name].to_numpy()

            grouped_by_param_set[par_val] = time_step_dict

        grouped_by_var_name[variable_name] = grouped_by_param_set

    return grouped_by_var_name


def write_data_to_h5(source_df: pd.DataFrame, destination_file_name: str, parameters_static = None) -> None:
    """writes extracted data form data frame to hdf5 file

    Args:
        source_df (pd.DataFrame): data frame extracted from cleaned .txt file
        destination_file_name (str): should end with "*.h5" to demarcate file format
        parameters_static (dict, optional): dict of the parameter values that are not 
        sweeped over. Defaults to None.
    """
    #can only write if file does not exist yet.
    file = h5py.File(destination_file_name, 'w-')
    sorted_data = extract_data_frames_grouped_by_variable_name_parameters_and_time_steps(source_df)

    # write static parameters to file
    if parameters_static is not None:
        for name in parameters_static:
            file.attrs[name] = parameters_static[name]

    for var_name, var_data in sorted_data.items():
        if var_name == "positions":
            positions_group = file.create_group(var_name)
            for dimension_name in var_data:
                #exclude other entries
                if dimension_name in ['X', 'Y', 'Z']:
                    positions_group.create_dataset(dimension_name, data=var_data[dimension_name])
        else:
            variable_group = file.create_group(var_name)
            for index, par_name in enumerate(var_data):
                # safeguard against empyt parameter names
                if par_name == "":
                    par_name_file = "parameter_set_" + str(index)
                else: 
                    par_name_file = par_name

                parameter_group = variable_group.create_group(par_name_file)

                if par_name != "":
                    parameter_names_list = [name.split("=")[0] for name in par_name.split(",")]
                    parameter_values_list = [name.split("=")[1] for name in par_name.split(",")]
                    #write parameters to attributes to make machine readable
                    for name, value in zip(parameter_names_list, parameter_values_list):
                        parameter_group.attrs[name] = value

                for t_step_name in var_data[par_name]:
                    time_step = float(t_step_name[2:])
                    time_step_data_set = parameter_group.create_dataset(t_step_name,
                                                    data=var_data[par_name][t_step_name])
                    #write time to attrs to make machine readable
                    time_step_data_set.attrs['time'] = time_step

    file.close()

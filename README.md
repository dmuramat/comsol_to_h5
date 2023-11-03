# comsol_to_h5

comsol_to_h5 is a package for converting COMSOL ';'-separated csv output and
columnar COMSOL output to hdf5 format. 

## Installation
Not shipping to PyPI yet.

## Usage
In command line:
```bash
# Takes input file in csv format, 
# reads in parameter file (only int and float values!),
# outputs to hdf5. 
# Can only output regular 1D grid data so far. Unstructured grids and higher dimensions
# may be supported in later versions.
convert_csv_to_h5 -i <input_file> -o <output file> -p <parameter file> 
```

In python:
```python
import comsol_to_h5

# get dict of parameters form parameter file
params = comsol_to_h5.extract_parameters_static("path/to/parameter/file.txt")

# get pandas df from ';'-separated csv file
data_df = comsol_to_h5.read_from_comsol_native_csv("path/to/csv/file.txt")

# convert csv file to dict that structures into ahierarchy of 
# {
#   "variable_name": {
#                      "parameter_name": {
#                                          "time_step_name": data_np_array
#                                          }
#                     }, 
#   "positions": {"X": x_positions, "Y": y_positions, ...}
# }
structured_data = comsol_to_h5.extract_data_frames_grouped_by_variable_name_parameters_and_time_steps(data_df)

# write the structured data to file
comsol_to_h5.write_data_to_h5(data_df, "path/to/write/file.h5", params)
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
import sys
import getopt
import tempfile
from write_time_steps import write_data_to_h5, read_from_comsol_native_csv,\
    extract_parameters_static
from clean_file import clean_file

if __name__ == "__main__":
    argv = sys.argv[1:]

    try:
         opts, args = getopt.getopt(argv,"hi:o:p:d:f:",["input-file=","output-file=",
                                                      "structured=", "parameter-file=", 
                                                      "description-line-number=",
                                                      "format="])
    except getopt.GetoptError:
        print('convert_txt_to_h5_script_options.py -i <inputfile> -o <outputfile>  ' +
              '-p <parameterfile> -d <line number of description line>' +
              '-f <file format (csv or columnar, defaults to csv)>')
        sys.exit(2)

    INPUT_FILE_NAME = None
    OUTPUT_FILE_NAME = None
    PARAMETER_FILE_NAME = None
    HEADER_LINE_NUMBER = -1
    FILE_FORMAT = 'csv'

    for opt, arg in opts:
        if opt == '-h':
            print('convert_txt_to_h5_script_options.py -i <inputfile> -o <outputfile>' +
                  ' -p <parameterfile> -d <line number of descritption line>' +
              '-f <file format (\'csv\' or \'columnar\', defaults to csv)>')
            sys.exit()
        elif opt in ("-i", "--input-file"):
            INPUT_FILE_NAME = arg
        elif opt in ("-o", "--output-file"):
            OUTPUT_FILE_NAME = arg
        elif opt in ("-p", "--parameter-file"):
            PARAMETER_FILE_NAME = arg
        elif opt in ("-d", "--description-line-number"):
            HEADER_LINE_NUMBER = int(arg)
        elif opt in ("-f", "--format"):
            FILE_FORMAT = arg

    # check right specification of file format
    if FILE_FORMAT not in ('csv', 'columnar'):
        raise ValueError('file format specified was \'' + FILE_FORMAT + '\', ' +
                           'valid formats are \';\'-separated csv (\'csv\') and \'columnar\'.')

    FILE_DF = None

    # read in file
    if FILE_FORMAT == 'csv':
        FILE_DF = read_from_comsol_native_csv(INPUT_FILE_NAME)
    elif FILE_FORMAT == 'columnar':
        with tempfile.TemporaryDirectory() as TEMP_DIR:
            TEMP_FILE_NAME = TEMP_DIR + "/cleaned.txt"
            clean_file(INPUT_FILE_NAME, TEMP_FILE_NAME, HEADER_LINE_NUMBER)
            FILE_DF = read_from_comsol_native_csv(TEMP_FILE_NAME)


    STATIC_PARAMETER_DICT = None
    if PARAMETER_FILE_NAME is not None:
        STATIC_PARAMETER_DICT = extract_parameters_static(PARAMETER_FILE_NAME)

    write_data_to_h5(FILE_DF, OUTPUT_FILE_NAME, 
                                      parameters_static=STATIC_PARAMETER_DICT)

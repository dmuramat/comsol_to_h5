#!/bin/python3
import sys
import getopt
import tempfile
import comsol_to_h5

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
    HEADER_LINE_NUMBER = 7
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
            
    if FILE_FORMAT not in ('csv', 'columnar'):
        raise RuntimeError('file format specified was \'' + FILE_FORMAT + '\', ' +
                           'valid formats are \';\'-separated csv and columnar.')

    FILE_DF = None

    # read in file
    if FILE_FORMAT == 'csv':
        FILE_DF = comsol_to_h5.read_from_comsol_native_csv(INPUT_FILE_NAME)
    elif FILE_FORMAT == 'columnar':
        with tempfile.TemporaryDirectory() as TEMP_DIR:
            
    #write a cleaned file, red in and rm cleaned file
    cleaned_file_name = OUTPUT_FILE_NAME + ".cleaned_file"
    clean_file(INPUT_FILE_NAME, cleaned_file_name, column_description_line= HEADER_LINE_NUMBER)
    source_df = pd.read_csv(cleaned_file_name, comment='%', delimiter=';')
    os.popen("rm " + cleaned_file_name)


    STATIC_PARAMETER_DICT = None
    if PARAMETER_FILE_NAME is not None:
        STATIC_PARAMETER_DICT = comsol_to_h5.extract_parameters_static(PARAMETER_FILE_NAME)
        comsol_to_h5.write_data_to_h5(source_df, OUTPUT_FILE_NAME, 
                                      parameters_static=STATIC_PARAMETER_DICT)

    else:
        comsol_to_h5.write_data_to_h5(source_df, OUTPUT_FILE_NAME)


def clean_file(filename_original: str, filename_clean: str) -> None:
    """cleans comsol txt file such that it can be read into pandas

    Args:
        filename_original (str): file name of the comsol output (imput file to )
        filename_clean (str): target file name under which cleaned file name is saved
        column_description_line (int, optional): line in which description of the csv table is located.
        The next line is the start of the tabulary data. Defaults to -1, then the column 
        desciption line is not modified for pandas readability.
    """
    cleaned_file = open(filename_clean, 'w')

    with open(filename_original, 'r') as handle:
        for line in handle:
            while '  ' in line:
                line = line.replace('  ', ' ')
            line = line.replace(' @ ', '@')
            line = line.replace(', ', ',')
            line = line.replace('% ', '%')
            #introduce separator
            line = line.replace(' ', ';')
            # comply with COMSOL ';'-separated csv format
            line = line.replace('@', ' @ ')
            line = line.replace(',', ', ')
            line = line.replace('%', '% ')
            # line = line[2:]
            cleaned_file.write(line)

    cleaned_file.close()

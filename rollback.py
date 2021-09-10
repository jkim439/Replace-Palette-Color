import os
import shutil


def main():

    # Set input path
    path = '/home/jkim/NAS/raw_dicom/brain/_3_infarction/FROM20181101_TO20181109/NCCT'

    # Output information
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nRollback Mode' \
          '\n----------------------------------------------------------------------------------------------------'

    # Set variables
    result = 0
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Recur load input directories
    for dir in sorted(dirs):

        # Check folder
        if not dir.isdigit():
            continue

        # Output loaded folder
        print '\n[LOAD]', path + '/' + dir

        # Set path
        path_original = path + '/' + dir + '/labels.ori'
        path_target = path + '/' + dir + '/labels'

        shutil.rmtree(path_target)
        os.rename(path_original, path_target)

        # Complete every process
        result += 1

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\n', result, 'Folders are processed successfully.'

    return None


if __name__ == '__main__':
    main()

# The following file contains helper functions shared across the project

def get_info(file_path):
    """ This method is used to get information for the database
    :param
        str obj : Takes the path to the file
    :return:
        dict obj : contains information of the file
    """
    file = open(file_path, mode='rt', encoding='utf-8')
    info = {}
    for line in file:
        key, value = line.split(":")
        info[key] = value[:-1]
    file.close()
    return info


def add_info(file_path, user_id, key, mode='wt'):
    """ Method to add information to the database
    :param
        file_path: str obj containing file location information
        user_id: str obj containing username/keyID
        key: int obj containing key information
        mode: str obj for writing or updating database
    """
    file = open(file_path, mode=mode, encoding='utf-8')
    if mode == 'wt':
        file.write("{}:{}".format(user_id, key))
    else:
        file.write("\n{}:{}".format(user_id,key))
    file.close()
    return

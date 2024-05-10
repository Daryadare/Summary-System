import os
from datetime import date


def create_file(exist_dir: str, outputs_to_write: list,
                in_process_state: int):

    new_dir_name = '/lecture_resumes'
    new_dir_path = exist_dir+new_dir_name
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    today = str(date.today())
    new_file_name = new_dir_path+'/lecture-'+today

    if in_process_state == 0:
        while os.path.exists(new_file_name):
            file_vers = 0
            new_file_name = new_dir_path+'/lecture-'+today+f'-v{file_vers}'
            file_vers += 1
        mode = 'w'
    elif os.path.exists(new_file_name) and in_process_state > 0:
        mode = 'a'
    else:
        mode = 'w'

    with open(new_file_name, mode) as file:
        for el in outputs_to_write:
            file.write(el + '\n\n')
    file.close()

    in_process_state += 1
    return new_file_name, in_process_state

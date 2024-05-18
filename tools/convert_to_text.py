import os
from datetime import date


def create_file(exist_dir: str, outputs_to_write: list,
                in_process_state: int, curr_file: str):

    new_dir_name = '/lecture_resumes'
    new_dir_path = exist_dir+new_dir_name
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    today = str(date.today())
    new_file_name = new_dir_path+'/lecture-'+today+'-v0'

    if in_process_state == 0:
        file_vers = 1
        while os.path.exists(new_file_name):
            part_name = new_file_name[:new_file_name.find('-v')]
            new_file_name = part_name+f'-v{file_vers}'
            file_vers += 1
        mode = 'w'
    elif os.path.exists(curr_file) and in_process_state > 0:
        mode = 'a'
        new_file_name = curr_file
        outputs_to_write.append('Ответы на ваши вопросы сгенерированы нейросетью. '
                                'Пожалуйста проверяйте важную информацию! \n')
    else:
        mode = 'w'

    new_file_name = new_file_name + '.txt'
    with open(new_file_name, mode, encoding='utf-8') as file:
        for el in outputs_to_write:
            file.write(el + '\n\n')
    file.close()

    in_process_state += 1
    return new_file_name, in_process_state

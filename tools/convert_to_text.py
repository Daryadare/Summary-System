import os
from datetime import date


def create_file(exist_dir: str, outputs_to_write: list,
                in_process_state: int, curr_file: str) -> tuple[str, int]:
    """
    Функция для записи данных в текстовый файл.
    :param exist_dir: путь к папке проекта
    :param outputs_to_write: данные для записи в текстовый файл
    :param in_process_state: статус, первой записи в файл или дополнения
    :param curr_file: имя
    :return: путь к результирующему текстову файлу;
             статус записи в файл
    """
    """ Создание папки для результирующих файлов """
    new_dir_name = '/lecture_resumes'
    new_dir_path = exist_dir+new_dir_name
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    """ Формирование названия файла """
    today = str(date.today())
    new_file_name = new_dir_path+'/lecture-'+today+'-v0'

    if in_process_state == 0:
        file_vers = 1
        """ Корректировка названия файла, если такое имя уже существует, и запись данных """
        while os.path.exists(new_file_name):
            part_name = new_file_name[:new_file_name.find('-v')]
            new_file_name = part_name+f'-v{file_vers}'
            file_vers += 1
        mode = 'w'
    elif os.path.exists(curr_file) and in_process_state > 0:
        """ Определение состояния дополнения файла """
        mode = 'a'
        new_file_name = curr_file
        outputs_to_write.append('Ответы на ваши вопросы сгенерированы нейросетью. '
                                'Пожалуйста проверяйте важную информацию! \n')
    else:
        mode = 'w'

    """ Запись текста в файл """
    new_file_name = new_file_name + '.txt'
    with open(new_file_name, mode, encoding='utf-8') as file:
        for el in outputs_to_write:
            file.write(el + '\n\n')
    file.close()

    in_process_state += 1
    return new_file_name, in_process_state

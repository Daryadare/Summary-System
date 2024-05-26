import re
import os
import shutil
import pypandoc


def get_text(filepath: str) -> str:
    """
    Функция для считывания текстового файла
    :param filepath: путь к текстовому файлу формата txt
    :return: данные, считанные из файла
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def convert_textfile(filepath: str) -> tuple[str, str, int, str]:
    """
    Функция для конвертации текстовых файлов.
    :param filepath: путь к текстовому файлу
    :return: путь к конвертированному файлу, путь к папке проекта,
             статус, был ли файл конвертирован или соответствовал формату txt изначально
    """
    path_status = 0
    """ Замена обратных слешей, если пользователь скопирует путь из папки """
    fp_slash = re.sub(r'\\', r'/', filepath)
    """ Получение имени папки, в которой находится файл """
    fdir = os.path.dirname(fp_slash)
    """ Получение имени файла с расширением"""
    fn_full = os.path.basename(fp_slash)
    """ Получение имени файла без расширения """
    fn = re.split(r"\.", fn_full)[0]
    """ Получение имени папки проекта """
    fdir_last = os.path.dirname(fdir)

    """ Если указанного файла с расширением txt не существует ни в папке с данными,
        ни в папке проекта, выполняется конвертация """
    if (not os.path.exists(fdir + f'/{fn}.txt')
            and not os.path.exists(fdir_last + f'/{fn}.txt')):
        output = pypandoc.convert_file(fp_slash,
                                       'plain',
                                       outputfile=f'{fn}.txt')
        assert output == ""
        """ path_status = 1 означает, что файл был конвертирован """
        path_status = 1

    """ Перемещение файла в папку с данными """
    if os.path.exists(fdir_last + f'/{fn}.txt'):
        fcopy = fdir_last + f'/{fn}.txt'
        shutil.copy2(fcopy, fdir)
        os.remove(fcopy)
    new_filepath = fdir + f'/{fn}.txt'

    text_for_sum = get_text(new_filepath)

    return new_filepath, fdir_last, path_status, text_for_sum

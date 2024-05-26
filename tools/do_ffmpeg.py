import re
import os
import ffmpeg
import shutil


def convert_file(filepath: str) -> tuple[str, str, int]:
    """
    Функция для конвертации аудио- или видеофайла в аудиофайл формата mp3.
    :param filepath: путь к аудио- или видеофайлу
    :return: путь к конвертированному файлу, путь к папке проекта,
             статус, был ли файл конвертирован или соответствовал формату mp3 изначально
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

    """ Если указанного файла с расширением mp3 не существует ни в папке с данными,
        ни в папке проекта, выполняется конвертация """
    if (not os.path.exists(fdir + f'/{fn}.mp3')
            and not os.path.exists(fdir_last + f'/{fn}.mp3')):
        (
            ffmpeg.input(fp_slash)
            .output(f'{fn}.mp3', loglevel='quiet')
            .run()
        )
        """ path_status = 1 означает, что файл был конвертирован """
        path_status = 1

    """ Перемещение файла в папку с данными """
    if os.path.exists(fdir_last + f'/{fn}.mp3'):
        fcopy = fdir_last + f'/{fn}.mp3'
        shutil.copy2(fcopy, fdir)
        os.remove(fcopy)
    new_filepath = fdir + f'/{fn}.mp3'

    return new_filepath, fdir_last, path_status

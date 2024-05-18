import re
import os
import shutil
import pypandoc


def get_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def convert_textfile(filepath):

    path_status = 0
    fp_slash = re.sub(r'\\', r'/', filepath)
    fdir = os.path.dirname(fp_slash)
    fn_full = os.path.basename(fp_slash)
    fn = re.split(r"\.", fn_full)[0]
    fdir_last = os.path.dirname(fdir)

    if (not os.path.exists(fdir + f'/{fn}.txt')
            and not os.path.exists(fdir_last + f'/{fn}.txt')):
        output = pypandoc.convert_file(fp_slash,
                                       'plain',
                                       outputfile=f'{fn}.txt')
        assert output == ""
        path_status = 1

    if os.path.exists(fdir_last + f'/{fn}.txt'):
        fcopy = fdir_last + f'/{fn}.txt'
        shutil.copy2(fcopy, fdir)
        os.remove(fcopy)
    new_filepath = fdir + f'/{fn}.txt'

    text_for_sum = get_text(new_filepath)

    return new_filepath, fdir_last, path_status, text_for_sum

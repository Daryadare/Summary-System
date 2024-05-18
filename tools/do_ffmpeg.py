import re
import os
import ffmpeg
import shutil


def convert_file(filepath: str):

    path_status = 0
    fp_slash = re.sub(r'\\', r'/', filepath)
    fdir = os.path.dirname(fp_slash)
    fn_full = os.path.basename(fp_slash)
    fn = re.split(r"\.", fn_full)[0]
    fdir_last = os.path.dirname(fdir)

    if (not os.path.exists(fdir + f'/{fn}.mp3')
            and not os.path.exists(fdir_last + f'/{fn}.mp3')):
        (
            ffmpeg.input(fp_slash)
            .output(f'{fn}.mp3', loglevel='quiet')
            .run()
        )
        path_status = 1

    if os.path.exists(fdir_last + f'/{fn}.mp3'):
        fcopy = fdir_last + f'/{fn}.mp3'
        shutil.copy2(fcopy, fdir)
        os.remove(fcopy)
    new_filepath = fdir + f'/{fn}.mp3'

    return new_filepath, fdir_last, path_status

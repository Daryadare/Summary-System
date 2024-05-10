import re
import os
import ffmpeg


def convert_file(filepath: str):

    path_status = 0
    fp_slash = re.sub(r'\\', r'/', filepath)
    fdir = os.path.dirname(fp_slash)
    fn_full = os.path.basename(fp_slash)
    fn = re.split(r"\.", fn_full)[0]

    if not os.path.exists(fdir + f'/{fn}.mp3'):
        (
            ffmpeg.input(fp_slash)
            .output(f'{fn}.mp3', loglevel='quiet')
            .run()
        )
        new_filepath = fdir + f'/{fn}.mp3'
        path_status = 1
    else:
        new_filepath = fp_slash

    return new_filepath, fdir, path_status

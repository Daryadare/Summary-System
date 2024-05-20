import sys
from models import whisper, fred_t5_sum, rugpt3_large
from tools import do_ffmpeg, do_pypandoc, convert_to_text


def sys_work():
    """ Функция для связи модулей и взаимодействия с пользователем """
    outputs_to_write = []
    sys_type = str(input('Введите цифру соответствующую, типу данных,'
                         'с которым вы хотите работать: \n 1. Аудио- или видеофайл \n '
                         '2. Текстовый файл \n'))

    if sys_type == '1':
        f_path = str(input('Введите путь к аудио- или видеофайлу, включая его название,'
                           'для которого вы хотите получить транскрипцию: \n'))
        new_filepath, fdir, path_status = do_ffmpeg.convert_file(f_path)
        if path_status == 1:
            print('Ваш файл был успешно преобразован к необходимому формату .mp3!')
        else:
            print('Ваш файл изначально соответствовал необходимому формату .mp3!')

        print('Идет процесс транскрибации данных...')
        res_w_text = str(whisper.transcribe(new_filepath))
        res_w_ts, cleaned_text_sum = whisper.clean_whisper_output(res_w_text)
        if res_w_ts and cleaned_text_sum:
            print('Транскрипция с Вашего файла была успешно получена!')

    else:
        f_path = str(input('Введите путь к текстовому файлу, включая его название,'
                           ' для которого вы хотите получить суммаризацию: \n'))

        new_filepath, fdir, path_status, text_for_sum = do_pypandoc.convert_textfile(f_path)
        if path_status == 1:
            print('Ваш файл был успешно преобразован к необходимому формату .txt!')
        else:
            print('Ваш файл изначально соответствовал необходимому формату .txt!')

    sum_size = str(input('Какого размера вы бы хотели получить краткое содержание? '
                         'Введите цифру:\n 1. Малый размер\n 2. Средний размер\n '
                         '3. Большой размер\n '))
    if sum_size == '1':
        tokens_size = 50
    elif sum_size == '2':
        tokens_size = 100
    elif sum_size == '3':
        tokens_size = 200
    else:
        tokens_size = 100

    print('Идет процесс резюмирования данных...')
    if sys_type == '1':
        res_t5 = fred_t5_sum.make_summ(cleaned_text_sum, tokens_size)
    else:
        res_t5 = fred_t5_sum.make_summ(text_for_sum, tokens_size)
    fin_res_t5 = res_t5[:res_t5.find('</s>')]
    print('Суммаризация успешно проведена!')

    print('Выполняется формирование текстового файла с результатом работы...')
    outputs_to_write.append(fin_res_t5)
    if sys_type == '1':
        outputs_to_write.append(res_w_ts)
    new_file_name, in_process_state = convert_to_text.create_file(fdir, outputs_to_write,
                                                                  in_process_state=0,
                                                                  curr_file='')
    print(f'Результирующий файл успешно сформирован и доступен по пути: {new_file_name}\n')

    q_a = []
    question = str(input('Если у Вас появился вопрос по лекции, '
                         f'напишите свой вопрос, предварительно закрыв файл. '
                         f'Если вопросов нет, введите Нет: \n'))
    while question.lower() != 'нет':
        dir_answer = rugpt3_large.answer(question)
        if dir_answer:
            fin_answer = dir_answer[:dir_answer.find('<s>')]
            q_a.append(fin_answer)
            print(fin_answer)
        else:
            print('Модель не смогла ответить на ваш вопрос, попробуйте переформулировать его \n')
        question = str(input('Если у Вас появился новый вопрос, задайте его.'
                             'Если вопросов больше нет, напишите Нет: \n'))

    if q_a:
        print('Выполняется обновление текстового файла с результатом работы...')
        convert_to_text.create_file(fdir, q_a, in_process_state, new_file_name)
        print(f'Результирующий файл успешно сформирован и доступен по пути: {new_file_name}\n')

    print('Спасибо за использование системы!')


if __name__ == "__main__":
    sys_work()
    sys.exit()

import os
import time
import keyboard
from tqdm import tqdm


def checkpath(path):
    paths = path.split('\\')
    while '' in paths:
        paths.remove('')
    for i in range(1, len(paths) + 1):
        p = '\\'.join(paths[:i])
        if not os.path.exists(p):
            os.mkdir(p)


def conv2text(src_dir, out_dir):
    checkpath(src_dir)
    checkpath(out_dir)

    for f in tqdm(os.listdir(src_dir)):
        if f[-4:] == '.pdf':
            readpath = src_dir + f
            writename = f.replace('.pdf', '.txt')
            writepath = out_dir + writename

            try:
                os.startfile(readpath)
            except():
                print('Error with opening file')
                continue

            time.sleep(3)

            keyboard.press_and_release('alt')
            time.sleep(0.1)
            keyboard.press_and_release('f')
            time.sleep(0.1)
            keyboard.press_and_release('t')
            time.sleep(0.1)
            for i in range(9):
                keyboard.press_and_release('down arrow')
                time.sleep(0.1)
            keyboard.press_and_release('enter')
            time.sleep(2)

            if os.path.exists(src_dir + writepath):
                os.remove(src_dir + writepath)

            keyboard.write(str(writepath))
            time.sleep(0.2)
            keyboard.press_and_release('enter')

            while not os.path.exists(src_dir + writepath):
                time.sleep(1)

            time.sleep(3)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)


def merge_texts(directory):
    txt = ''

    for f in os.listdir(directory):
        if f[-4:] == '.txt':
            txt += open(directory + f, 'rb').read().decode(encoding='windows-1252')

    open(directory + 'all.txt', 'w').write(txt)

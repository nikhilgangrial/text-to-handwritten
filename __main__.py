import numpy as np
import cv2 as cv
from cv2 import imread

page_ = cv.imread('page.png', -1)

# ----------------CAPITAL LETTERS----------- #
uppercase_letters_images = {i: imread(f'final\\upper\\{i}.png', -1) for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}


def correct_u(key):
    height, width = uppercase_letters_images[key].shape[:2]

    height_ = height
    if key == 'Y':
        height_ -= 50

    return height, width, 200 - height_


uppercase_letters_corrections = {i: correct_u(i) for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

# --------LOWER LETTERS---------- #
lowercase_letters_images = {i: imread(f'final\\lower\\{i}.png', -1) for i in "abcdefghijklmnopqrstuvwxyz"}


def correct_l(key):
    height, width = lowercase_letters_images[key].shape[:2]

    height_ = height
    if key in {'z', 'q', 'f'}:
        height_ -= 70
    elif key in {'y', 'p', 'j', 'g'}:
        height_ -= 90

    return height, width, 200 - height_


lowercase_letters_correction = {i: correct_l(i) for i in 'abcdefghijklmnopqrstuvwxyz'}


# ------------- other characters ---------- #
characters_images = {'.': imread("final\\chr\\'.'.png", -1)}

characters_correction = {'.': characters_images['.'].shape[:2] + (165,)}


# _______func for width of word____________ #
def width_word(word):
    width = 0
    for letter in word:
        if width > 0:
            width += 2
        # for uppercase letters
        if letter.isupper():
            width += uppercase_letters_corrections[letter][1]
        # for lowercase letters
        elif letter.islower():
            width += lowercase_letters_correction[letter][1]
        else:
            width += characters_correction[letter][1]

    return width


# TEXT TO BE CONVERTED
def main(text):

    lines = text.split('\n')

    page = np.zeros((10000, 5000, 4), np.uint8)  # 55, 75
    no = 0

    cordinate_y = 0
    for line in lines:
        
        words = line.split(' ')

        line_space = 5000
        cordinate_x = 0

        for word in words:
            width = width_word(word)

            # moves to next line if word cannot be fitted
            if width > line_space:
                cordinate_x = 0
                cordinate_y += 250
                line_space = 5000

            # creates new page while saviing the current if page is full
            if cordinate_y == 10000:
                cv.imwrite(f'outpage{no}.png', page)
                no += 1
                page = np.zeros((10000, 5000, 4), np.uint8)  # 55, 75
                cordinate_x = cordinate_y = 0
                line_space = 5000

            for letter in word:

                if letter.isupper():
                    height_letter, width_letter, correction = uppercase_letters_corrections[letter]

                    x_lower = cordinate_y + correction
                    x_upper = cordinate_y + height_letter + correction
                    y_lower = cordinate_x
                    y_upper = cordinate_x + width_letter

                    page[x_lower:x_upper, y_lower:y_upper] = uppercase_letters_images[letter]
                    cordinate_x += width_letter
                    line_space = 5000 - cordinate_x

                elif letter.islower():
                    height_letter, width_letter, correction = lowercase_letters_correction[letter]

                    x_lower = cordinate_y + correction
                    x_upper = cordinate_y + height_letter + correction
                    y_lower = cordinate_x
                    y_upper = cordinate_x + width_letter

                    page[x_lower:x_upper, y_lower:y_upper] = lowercase_letters_images[letter]
                    cordinate_x += width_letter
                    line_space = 5000 - cordinate_x

                elif letter == '\n':
                    cordinate_y += 250
                    cordinate_x = -68
                    line_space = 5000

                    if cordinate_y == 10000:
                        cv.imwrite(f'outpage{no}.png', page)
                        no += 1
                        page = np.zeros((10000, 5000, 4), np.uint8)  # 55, 75
                        cordinate_x = -68
                        cordinate_y = 0
                        line_space = 5000

                else:
                    height_letter, width_letter, correction = characters_correction[letter]

                    x_lower = cordinate_y + correction
                    x_upper = cordinate_y + height_letter + correction
                    y_lower = cordinate_x
                    y_upper = cordinate_x + width_letter

                    page[x_lower:x_upper, y_lower:y_upper] = characters_images[letter]
                    cordinate_x += width_letter
                    line_space = 5000 - cordinate_x

            else:
                cordinate_x += 68
                line_space -= 68
                if cordinate_x >= 5000:
                    cordinate_x = 0
                    cordinate_y += 250
                    line_space = 5000
                if cordinate_y >= 10000:
                    cv.imwrite(f'outpage{no}.png', page)
                    no += 1
                    page = np.zeros((10000, 5000, 4), np.uint8)  # 55, 75
                    cordinate_x = cordinate_y = 0
                    line_space = 5000
        else:
            cordinate_y += 250

    cv.imwrite(f'outpage{no}.png', page)


text = """
 Hello There.
"""
main(text)

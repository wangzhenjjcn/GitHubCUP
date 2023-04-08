import os
import sys
import datetime
from git import Repo

def read_banner_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def text_to_matrix(text):
    columns = 53
    rows = 7

    matrix = [[' ' for _ in range(columns)] for _ in range(rows)]

    for i, ch in enumerate(text[:13]):
        ch_matrix = character_to_matrix(ch)
        for row in range(7):
            for col in range(4):
                matrix[row][i * 4 + col] = ch_matrix[row][col]

    return matrix

def character_to_matrix(ch):
    char_map = {
        "A": ["  ##  ", " #  # ", "#    #", "######", "#    #", "#    #", "#    #"],
        "B": ["##### ", "#    #", "#    #", "##### ", "#    #", "#    #", "##### "],
        "C": [" #####", "#    #", "#     ", "#     ", "#     ", "#    #", " #####"],
        "D": ["##### ", "#    #", "#    #", "#    #", "#    #", "#    #", "##### "],
        "E": ["######", "#     ", "#     ", "##### ", "#     ", "#     ", "######"],
        "F": ["######", "#     ", "#     ", "##### ", "#     ", "#     ", "#     "],
        "G": [" #####", "#    #", "#     ", "#  ###", "#    #", "#    #", " #####"],
        "H": ["#    #", "#    #", "#    #", "######", "#    #", "#    #", "#    #"],
        "I": [" #####", "   #  ", "   #  ", "   #  ", "   #  ", "   #  ", " #####"],
        "J": ["######", "     #", "     #", "     #", "#    #", "#    #", " #### "],
        "K": ["#    #", "#   # ", "#  #  ", "###   ", "#  #  ", "#   # ", "#    #"],
        "L": ["#     ", "#     ", "#     ", "#     ", "#     ", "#     ", "######"],
        "M": ["#    #", "##  ##", "# ## #", "#    #", "#    #", "#    #", "#    #"],
        "N": ["#    #", "##   #", "# #  #", "#  # #", "#   ##", "#    #", "#    #"],
        "O": [" #####", "#    #", "#    #", "#    #", "#    #", "#    #", " #####"],
        "P": ["##### ", "#    #", "#    #", "##### ", "#     ", "#     ", "#     "],
        "Q": [" #####", "#    #", "#    #", "#    #", "#  # #", "#   # ", " ### #"],
        "R": ["##### ", "#    #", "#    #", "##### ", "#  #  ", "#   # ", "#    #"],
        "S": [" #####", "#    #", "#     ", " #####", "     #", "#    #", " #####"],
        "T": ["######", "   #  ", "   #  ", "   #  ", "   #  ", "   #  ", "   #  "],
        "U": ["#    #", "#    #", "#    #", "#    #", "#    #", "#    #", " #####"],
        "V": ["#    #", "#    #", "#    #", "#    #", " #  # ", "  ##  ", "   #  "],
        "W": ["#    #", "#    #", "#    #", "#    #", "# ## #", "#  # #", "#    #"],
        "X": ["#    #", " #  # ", "  ##  ", "  ##  ", " #  # ", "#    #", "#    #"],
        "Y": ["#    #", " #  # ", "  ##  ", "   #  ", "   #  ", "   #  ", "   #  "],
        "Z": ["######", "    # ", "   #  ", "  #   ", " #    ", "#     ", "######"],
        " ": ["      ", "      ", "      ", "      ", "      ", "      ", "      "],
        ",": ["      ", "      ", "      ", "  ### ", "  ### ", "   #  ", "  #   "],
        ".": ["      ", "      ", "      ", "      ", "      ", "  ##  ", "  ##  "],
        "!": ["  ##  ", "  ##  ", "  ##  ", "  ##  ", "  ##  ", "      ", "  ##  "],
        "?": [" #####", "#    #", "     #", "   ## ", "   #  ", "      ", "   #  "],
        "'": ["  ##  ", "  ##  ", "   #  ", "      ", "      ", "      ", "      "],
        ":": ["      ", "  ##  ", "  ##  ", "      ", "      ", "  ##  ", "  ##  "],
        ";": ["      ", "  ##  ", "  ##  ", "      ", "  ##  ", "  ##  ", "   #  "],
        "-": ["      ", "      ", "      ", "##### ", "      ", "      ", "      "],
        "_": ["      ", "      ", "      ", "      ", "      ", "      ", "######"],
        "/": ["    # ", "   #  ", "  #   ", " #    ", "#     ", "      ", "      "],
        "+": ["      ", "  ##  ", "  ##  ", "######", "  ##  ", "  ##  ", "      "],
        "=": ["      ", "      ", "######", "      ", "######", "      ", "      "],
        "*": ["  #   ", " ###  ", "# # # ", "  #   ", "      ", "      ", "      "],
        "(": ["    # ", "   #  ", "  #   ", "  #   ", "  #   ", "   #  ", "    # "],
        ")": ["  #   ", "   #  ", "    # ", "    # ", "    # ", "   #  ", "  #   "],
        "[": ["  ### ", "  #   ", "  #   ", "  #   ", "  #   ", "  #   ", "  ### "],
        "]": [" ###  ", "   #  ", "   #  ", "   #  ", "   #  ", "   #  ", " ###  "],
        "{": ["   ## ", "  #   ", "  #   ", " #    ", "  #   ", "  #   ", "   ## "],
        "}": [" ##   ", "   #  ", "   #  ", "    # ", "   #  ", "   #  ", " ##   "],

    }

    if ch in char_map:
        return char_map[ch]
    else:
        return [
            '    ',
            '    ',
            '    ',
            '    ',
            '    '
        ]


def matrix_to_dates(matrix):
    today = datetime.date.today()
    first_day_of_year = today.replace(month=1, day=1)
    first_sunday = first_day_of_year + datetime.timedelta(days=(6 - first_day_of_year.weekday()))

    active_dates = []

    for row in range(7):
        for col in range(53):
            if matrix[row][col] == '#':
                active_date = first_sunday + datetime.timedelta(weeks=col, days=row)
                if active_date <= today:
                    active_dates.append(active_date)

    return active_dates

def commit_and_push_dates(dates, repo_dir, commit_message):
    repo = Repo(repo_dir)
    index = repo.index

    for date in dates:
        for hour in range(1, 7):
            index.commit(commit_message, author_date=f"{date} {hour}:00:00", commit_date=f"{date} {hour}:00:00")
    
    repo.git.push()

def main():
    banner_text = read_banner_file('banner.txt')
    matrix = text_to_matrix(banner_text)
    active_dates = matrix_to_dates(matrix)
    commit_and_push_dates(active_dates, '.', banner_text)

if __name__ == '__main__':
    main()

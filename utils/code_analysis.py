"""
Модуль для сохранения содержимого файлов с определенными расширениями в текстовый файл.

Этот модуль предоставляет функцию, которая обходит все файлы в указанной корневой директории,
выбирает файлы с нужными расширениями и сохраняет их содержимое в один текстовый файл.
"""

import os


def save_scripts_to_file(root_directory, output_file, extensions_to_include):
    """
    Проходит по всем файлам в указанной директории и сохраняет содержимое файлов с заданными расширениями в один текстовый файл.

    :param root_directory: Путь к корневой директории, в которой нужно искать файлы.
    :type root_directory: str
    :param output_file: Путь к выходному текстовому файлу, в который будет сохранено содержимое файлов.
    :type output_file: str
    :param extensions_to_include: Список расширений файлов, содержимое которых необходимо сохранить.
                                  Например, ['.py', '.js', '.html', '.css'].
    :type extensions_to_include: list
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for foldername, subfolders, filenames in os.walk(root_directory):
            # Пропускаем папки 'static' и 'templates'
            if 'static' in foldername:
                continue

            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                file_extension = os.path.splitext(filename)[1]

                # Если расширение файла совпадает с нужными, добавляем его содержимое
                if file_extension in extensions_to_include:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"\n--- {file_path} ---\n")
                            outfile.write(infile.read())
                            outfile.write("\n")
                    except Exception as e:
                        print(f"Ошибка при чтении файла {file_path}: {e}")


# Пример использования
root_directory = '/Users/ivan/Desktop/PyFlask/fad/app'  # Путь к папке 'app'
output_text_file = 'all_scripts_content.txt'
extensions_to_include = ['.py', '.html']  # Можно указать расширения файлов

save_scripts_to_file(root_directory, output_text_file, extensions_to_include)

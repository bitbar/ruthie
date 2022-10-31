import os
import re


def get_file_path(unittests_path):
    for unittests_root, unittests_dirs, unittests_files in os.walk(unittests_path):
        module_root = unittests_root.replace(os.path.sep, '.')

        for file_name in unittests_files:
            if file_name[0] in ['.', '_']:
                continue

            module_name, file_ext = os.path.splitext(file_name)
            if file_ext != '.py':
                continue

            yield f'{module_root}.{module_name}'

        for dir_name in unittests_dirs:
            yield from get_file_path(f'{module_root}.{dir_name}')


def get_file_line(unittests_path):
    gen_get_file_path = get_file_path(unittests_path)
    for module_path in gen_get_file_path:
        module_file_path = module_path.replace('.', os.path.sep) + '.py'
        with(open(module_file_path, 'r')) as file:
            while True:
                line = file.readline()
                if not line:
                    break

                yield module_path, line


def classes_in(unittests_path):
    classes = []
    current_class = None
    test_found = False
    tests_number = 0

    gen_get_file_line = get_file_line(unittests_path)
    for module_path, line in gen_get_file_line:
        class_name = re.match(r"class ([^(]+)", line)
        if class_name:
            if test_found:
                classes.append((module_path, current_class, tests_number))
            current_class = class_name.group(1)
            test_found = False
            tests_number = 0
            continue

        if re.match(r" +def test_", line):
            test_found = True
            tests_number += 1

    classes.sort(key=lambda x: x[2])
    return classes

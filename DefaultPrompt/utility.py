def simplify_path(dir):
    if dir[0] == '!':
        dir = dir[1:]
    else:
        return None

    if dir[-1] == '/':
        dir = dir[:-1]

    folders = dir.split('/')
    enddir = []

    for folder in folders:
        if folder == '..':
            enddir.pop()
        elif folder == '.':
            pass
        else:
            enddir.append(folder)

    return '!'+'/'.join(enddir)+'/'


def get_file_path(cwd, filepath):
    if filepath[0] == '!':
        return simplify_path(filepath)
    else:
        return simplify_path(cwd+filepath)

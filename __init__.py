# vim: set fileencoding=utf-8

import fnmatch
import os
import stat
import re
import subprocess

from ranger.api import register_linemode
from ranger.core.linemode import LinemodeBase

from .icons import file_node_extensions, file_node_exact_matches, file_node_pattern_matches

def get_file_type(filename):
    # Run the 'file' command and capture its output
    result = subprocess.run(['file', filename], capture_output=True, text=True)

    # Return the output of the 'file' command
    return result.stdout.strip()

def get_icon(file):

    if file.is_link:
        if not file.exists:
            return '⚠️'
        if file.stat and stat.S_ISDIR(file.stat.st_mode):
            return '🔖'
        return '🎯'

    if file.is_socket:
        return '💡'

    if file.is_fifo:
        return '🅿️'

    if not file.is_directory and file.stat:
        mode = file.stat.st_mode
        if mode & stat.S_IXUSR:
            return '🚀'
        if stat.S_ISCHR(mode):
            return '🖨️'
        if stat.S_ISBLK(mode):
            return '💾'

    if file.is_directory:
        return '📂'

    filepath:str = file.relative_path
    filename:str = os.path.basename(filepath)


    source_file = ['.c', '.cpp', '.h', '.hpp', '.proto', 'makefile', 'Makefile', '.mk']

    if re.search(r'[Dd]ocker', filename):
        return '🐋'
    if filename.endswith('.py'):
        return '🐍'
    if filename.endswith('.json') or filename.endswith('.yaml') or filename.endswith('.xml') or filename.endswith('.html'):
        return '🪪'
    if any(filename.endswith(ext) for ext in source_file):
        return '✏️'

    file_type:str = get_file_type(filepath).lower()
    if filename.endswith('.sh') or filename.endswith('.bash') or re.search(r'shell', file_type):
        return '🥷'
    if re.search(r'elf', file_type):
        return '👻'

    if re.search(r'text', file_type):
        return '📄'


    return ' '


def get_symbol(file):
    if file.is_link:
        if not file.exists:
            return '!'
        if file.stat and stat.S_ISDIR(file.stat.st_mode):
            return '~'
        return '@'

    if file.is_socket:
        return '='

    if file.is_fifo:
        return '|'

    if not file.is_directory and file.stat:
        mode = file.stat.st_mode
        if mode & stat.S_IXUSR:
            return '*'
        if stat.S_ISCHR(mode):
            return '-'
        if stat.S_ISBLK(mode):
            return '+'

    if file.is_directory:
        return '/'

    return ''


@register_linemode
class DevIcons2Linemode(LinemodeBase):
    name = 'devicons2'
    uses_metadata = False

    def filetitle(self, file, metadata):
        return '{0} {1}{2}'.format(
            get_icon(file),
            file.relative_path,
            get_symbol(file),
        )

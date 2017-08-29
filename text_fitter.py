'''
A simple tool that fits text to fixed width.

You can choose a wrapper - single or double quote - and
a number of characters per line.
'''

import argparse

try:
    import pyperclip
except ImportError:
    PYPERCLIP_AVAILABLE = False
else:
    PYPERCLIP_AVAILABLE = True


class TextFitter(object):

    escaped_chars = []

    def __init__(self, file_path, wrapper, char_limit):
        with file_path as opened_file:
            joined_lines = ''.join(opened_file)
        if wrapper == 'single':
            self._wrapper = "'"
        else:
            self._wrapper = '"'
        # 3 characters are reserved for quotation marks and a newline
        self._real_limit = char_limit - 3
        if joined_lines[-1] == '\n':
            joined_lines = joined_lines[:-1]
        self._cleared_lines = joined_lines.replace(
            wrapper, '\{}'.format(wrapper)).replace('\t', r'\t').replace('\n', r'\n')

    def get_complete_text(self):
        head_index = 0
        tail_index = self._real_limit
        parsed_lines = []
        while head_index < len(self._cleared_lines):
            parsed_lines.append('{wrapper}{text}{wrapper}'.format(
                text=self._cleared_lines[head_index:tail_index], wrapper=self._wrapper))
            head_index += self._real_limit
            tail_index += self._real_limit
        return '\n'.join(parsed_lines)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description="Text Fitter v. 0.02. Fit text to a fixed-sized column.",
        epilog="If pyperclip module is available, you can copy the result text to clipboard.")
    parser.add_argument('file_path', type=file, help="Path to the file containing a text to fit.")
    if PYPERCLIP_AVAILABLE:
        parser.add_argument('-c', '--clip', action='store_true',
                            help="Copy the fitted text to clipboard.")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        help="A file to save the fitted text.")
    parser.add_argument('-m', '--max_chars', default=72, type=int,
                        help="Maximum number of characters per line (72 if not specified).")
    parser.add_argument('-w', '--wrapper', default="single", choices=["single", 'double'],
                        help="Choose a quotation mark, which will wrap lines of the text.")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parsed_args()
    fitter = TextFitter(args.file_path, args.wrapper, args.max_chars)
    fitted_text = fitter.get_complete_text()
    print "Fitted text:\n\n"
    print fitted_text
    if args.output:
        with args.output as output_file:
            output_file.write(fitted_text)
    if getattr(args, 'clip', None):
        pyperclip.copy(fitted_text)

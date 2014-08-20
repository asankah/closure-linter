import vim
import sys
import os

from inspect import getsourcefile

closure_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(getsourcefile(lambda _:None))), '..'))
gflags_path = os.path.abspath(os.path.join(closure_path, 'gflags'))
if closure_path not in sys.path:
  sys.path += [closure_path]
if gflags_path not in sys.path:
  sys.path += [gflags_path]

from closure_linter import error_fixer
from closure_linter import runner
from closure_linter.common import simplefileflags as fileflags
import gflags as flags

class VimErrorFixer(error_fixer.ErrorFixer):
  def FinishFile(self):
    if self._file_fix_count:
      token = self._file_token
      while token.is_deleted:
        token = token.next

      while token.previous:
        token = token.previous

      lines = []
      line = ''
      char_count = 0
      while token:
        line += token.string
        char_count += len(token.string)

        if token.IsLastInLine():
          if (line or not self._file_is_html or
              token.orig_line_number is None):
            lines += [line]
          else:
            # TODO: get original line corresponding to token.orig_line_number -
            # 1 and append it to lines here.
            pass
          line = ''
          # TODO: deal with lines that are longer than 80 characters here.
          char_count = 0

        token = token.next

      vim.current.range[:] = lines


flags.FLAGS([os.path.abspath(getsourcefile(lambda _:None)), '--jslint_error=all'])

runner.Run(vim.current.buffer.name, VimErrorFixer(), vim.current.range)

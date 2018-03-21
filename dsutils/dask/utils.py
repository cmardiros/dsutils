import sys
import dask
from dask import diagnostics


class ProgressBar(diagnostics.ProgressBar):

    """
    Add ability to label progress bar
    """

    def __init__(self, identifier=None):
        self.identifier = identifier

        super(ProgressBar, self).__init__()

    def _draw_bar(self, frac, elapsed):
        bar = '#' * int(self._width * frac)
        percent = int(100 * frac)
        elapsed = diagnostics.progress.format_time(elapsed)
        msg = '\r[{0:<{1}}] | {2}% Completed | {3} ({4})'
        msg = msg.format(bar, self._width, percent, elapsed,
                         self.identifier)
        with dask.utils.ignoring(ValueError):
            sys.stdout.write(msg)
            sys.stdout.flush()

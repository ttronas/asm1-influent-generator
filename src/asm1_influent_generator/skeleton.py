"""
This is a skeleton file that can serve as a starting point for a Python
console script. This is accomplished via the following lines in `pyproject.toml`:

```toml
[project.scripts]
asm1_influent_generator = "asm1_influent_generator.skeleton:app"
```

Then run `hatch run asm1_influent_generator 10` to execute this in your default environment or
`hatch shell` to enter the default environment, followed by `asm1_influent_generator 10`.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import enum
import logging
import sys
from typing import Annotated

import numpy as np
import typer

from asm1_influent_generator import __version__
from asm1_influent_generator.asm1_generator import ASM1Generator

_logger = logging.getLogger(__name__)


class LogLevel(str, enum.Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'


def setup_logging(log_level: LogLevel):
    """Setup basic logging"""
    log_format = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
    numeric_level = getattr(logging, log_level.upper(), None)
    logging.basicConfig(level=numeric_level, stream=sys.stdout, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')


app = typer.Typer(
    name=f'ASM1 Influent Generator {__version__}',
    help='A Python Module to generate Arrays in the Activated Sludge Model 1 (ASM1) format.',
)


@app.command()
def main(
    n: Annotated[int, typer.Argument(..., min=1, help='Positive integer')],
    log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.WARNING,
):
    """Wrapper allowing `ASM1Generator` to be called with an argument in a CLI fashion

    Instead of returning the value from `ASM1Generator.generate`, it directly saves the generated arrays to .csv files.
    Each array has the shape (n_timesteps, n_components + 1), where:
    n_timesteps: Number of timesteps in each sample
    n_components: Number of components in each sample. The first column is time in days
    """
    setup_logging(log_level)
    _logger.debug('Initialising ASM1Generator')
    asm1_gen = ASM1Generator()
    _logger.debug('Generating %d samples', n)
    out = asm1_gen.generate(n)
    print('I created %d samples for you! I saved them into your working directory.' % n)  # noqa: T201
    _logger.info('Saving generated samples to generated_samples[i].csv')
    for i in range(n):
        np.savetxt(
            f'generated_samples{i + 1}.csv',
            out[i],
            delimiter=',',
            header='time,SI,SS,XI,XS,XBH,XBA,XP,SO,SNO,SNH,SND,XND,SALK,TSS,Q,TEMP,SD1,SD2,SD3,XD4,XD5',
        )
    _logger.info('Script ends here')


if __name__ == '__main__':
    app()

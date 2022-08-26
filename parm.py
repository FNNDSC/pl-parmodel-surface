#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _                                             _      _                        __               
      | |                                           | |    | |                      / _|              
 _ __ | |______ _ __   __ _ _ __ _ __ ___   ___   __| | ___| |______ ___ _   _ _ __| |_ __ _  ___ ___ 
| '_ \| |______| '_ \ / _` | '__| '_ ` _ \ / _ \ / _` |/ _ \ |______/ __| | | | '__|  _/ _` |/ __/ _ \
| |_) | |      | |_) | (_| | |  | | | | | | (_) | (_| |  __/ |      \__ \ |_| | |  | || (_| | (_|  __/
| .__/|_|      | .__/ \__,_|_|  |_| |_| |_|\___/ \__,_|\___|_|      |___/\__,_|_|  |_| \__,_|\___\___|
| |            | |                                                                                    
|_|            |_|                                                                                    
"""


parser = ArgumentParser(description='Create surfaces from spherical functions',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--name', default='foo',
                    help='argument which sets example output file name')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='Parametric Surface Functions',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)

    output_file = outputdir / f'{options.name}.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Uses physics (ISO) convention for spherical coordinates
https://en.wikipedia.org/wiki/Spherical_coordinate_system#/media/File:3D_Spherical_2.svg
"""


from math import sin, cos, acos, atan2
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
from typing import Callable

import numpy as np
import numpy.typing as npt
from chris_plugin import chris_plugin, PathMapper
from bicpl import PolygonObj

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version

DISPLAY_TITLE = r"""
 _ __   __ _ _ __ _ __ ___    _ __  _   _ 
| '_ \ / _` | '__| '_ ` _ \  | '_ \| | | |
| |_) | (_| | |  | | | | | |_| |_) | |_| |
| .__/ \__,_|_|  |_| |_| |_(_) .__/ \__, |
| |                          | |     __/ |
|_|                          |_|    |___/
"""

parser = ArgumentParser(description='Create surfaces from spherical functions',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-e', '--equation', required=True, type=str,
                    help='3D function in the form r(polar, azimuth)=?')
parser.add_argument('-i', '--input', default='**/*.obj',
                    help='input files glob')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


@chris_plugin(
    parser=parser,
    title='Parametric Surface Functions',
    category='Modeling',
    min_memory_limit='500Mi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr)
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.input)
    for input_file, output_file in mapper:
        parm(options.equation, input_file, output_file)


def parm(equation: str, input_file: Path, output_file: Path):
    sphere = PolygonObj.from_file(input_file)
    vertices = project_mesh(equation, sphere.point_array)
    surf = sphere.reset_points(vertices)
    surf.save(output_file)


def project_mesh(equation: str, sampling_tensor: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    function = func(equation)

    def proj(point):
        r, theta, phi = cart2sphere(*point)
        r = function(theta, phi)
        return sphere2cart(r, theta, phi)

    return np.array([proj(p) for p in sampling_tensor], dtype=np.float32)


def func(equation: str) -> Callable[[float, float], float]:
    return eval('lambda theta, phi: ' + equation)


def cart2sphere(x: float, y: float, z: float) -> tuple[float, float, float]:
    """
    Adapted from ``dipy.core.geometry.cart2sphere``
    """
    # doesn't matter for sinusoidal functions, but it would be nice to
    # change these angles to be in the range of
    # 0 <= theta < pi
    # 0 <= phi < 2*pi
    r = euclidean_distance(x, y, z)
    # center will be missing if it exists at whole numbers
    theta = acos(z / r)
    phi = atan2(y, x)
    return r, theta, phi


def sphere2cart(r: float, polar: float, azimuth: float) -> tuple[float, float, float]:
    x = r * sin(polar) * cos(azimuth)
    y = r * sin(polar) * sin(azimuth)
    z = r * cos(polar)
    return x, y, z


def euclidean_distance(*args):
    """
    Wrapper for ``numpy.linalg.norm``
    """
    return np.linalg.norm(args)


if __name__ == '__main__':
    main()

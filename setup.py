from setuptools import setup

setup(
    name='parmodel-surface',
    version='1.0.0',
    description='Create surfaces from spherical functions',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-parmodel-surface',
    py_modules=['parm'],
    install_requires=['chris_plugin', 'pybicpl'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'parm = parm:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1',
            'pytest-mock~=3.8'
        ]
    }
)

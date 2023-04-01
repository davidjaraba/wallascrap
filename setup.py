from setuptools import setup

setup_args = dict(
    name='cars-scrapping',
    version='0.1',
    description='Descripción del proyecto',
    author='velcas',
    py_modules=['main'],
    install_requires=[
        'telegram',
        'selenium'
    ]
)

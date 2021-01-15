from setuptools import setup


setup(
    name="flick",
    version='0.1',
    py_modules=['images'],
    install_requires=[
        'Click',
        'texttable',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        flick=images:cli
    ''',
)


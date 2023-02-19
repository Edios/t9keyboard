from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='t9keyboard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.1',
    description='T9 Keyboard controlled by Numpad keyboard buttons.',
    url='https://github.com/Edios/t9keyboard',
    author='Miroslaw Lazarewicz',
    author_email='miroslaw.lazarewicz@gmail.com',
    license='MIT',
    packages=['t9keyboard'],
    install_requires=['pynput'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
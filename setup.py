import setuptools

setuptools.setup(
    name='gemdqm',
    version="0.0.3",
    description="Utilities for GEM DQM",
    author="Seungjin Yang",
    author_email="seungjin.yang@cern.ch",
    url="https://github.com/slowmoyang/GEMDQMUtils",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.9',
    license='BSD-3',
    packages=setuptools.find_packages(),
)

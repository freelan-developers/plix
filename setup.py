from setuptools import (
    setup,
    find_packages,
)

setup(
    name='plix',
    url='http://plix.readthedocs.org/en/latest/index.html',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    license='MIT',
    version=open('VERSION').read().strip(),
    description=(
        "A tool to create build matrices and run them in parallel."
    ),
    long_description="""\
A command-line tool to create build matrices and run them, possibly in
parallel, on different platforms.
""",
    packages=find_packages(exclude=[
        'tests',
    ]),
    install_requires=[
    ],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
    ],
)

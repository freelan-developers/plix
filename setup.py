from setuptools import (
    setup,
    find_packages,
)

setup(
    name='plix',
    url='http://plix.readthedocs.org/en/latest/index.html',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    maintainer='Julien Kauffmann',
    maintainer_email='julien.kauffmann@freelan.org',
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
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
    ],
)

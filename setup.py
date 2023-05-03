import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='senscritique',
    version='0.5.4',
    author='Wok',
    author_email='wok@tuta.io',
    description='SensCritique Takeout on PyPI',
    keywords=['senscritique', 'takeout', 'takeaway'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/woctezuma/SensCritique-Takeout',
    download_url='https://github.com/woctezuma/SensCritique-Takeout/archive/0.5.4.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'lxml',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Games/Entertainment',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: French',
    ],
    python_requires='>=3',
)

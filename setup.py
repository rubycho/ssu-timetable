import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssu-timetable",
    version="0.0.1",
    author="rubycho",
    author_email="rubycho@outlook.kr",
    description="SSU subject parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rubycho/ssu-timetable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'lxml',
        'bs4',
        'requests',
    ]
)

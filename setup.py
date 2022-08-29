from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A wrapper for nlpcloud free-tier services with no requests per minute limits.'
LONG_DESCRIPTION = 'A wrapper for nlpcloud free-tier services with no requests per minute limits.'
# Setting up
setup(
    name="freenlpc",
    version=VERSION,
    author="Abdelrhman Nile",
    author_email="<abdelrhmannile@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['nlpcloud'],
    keywords=['python', 'natural languge processing', 'nlp', 'deep learning', 'AI', 'GPT', 'LLMS', 'nlpcloud'],
    classifiers=[
        "Development Status :: Deploying",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Gitools",
    version="1.2.2",
    license="MIT",
    author="AliReza Beigy",
    author_email="AliRezaBeigyKhu@gmail.com",
    entry_points="""
        [console_scripts]
        gitools=gitools.__main__:main
    """,
    python_requires=">=3.6",
    platforms=["nt", "posix"],
    long_description=long_description,
    packages=setuptools.find_packages(),
    url="https://github.com/AliRezaBeigy/Gitools",
    long_description_content_type="text/markdown",
    description="A handy tool to modify git history",
    keywords="git history filter-branch change-date git-history",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
    ],
)

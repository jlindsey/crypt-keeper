from setuptools import setup, find_packages

setup(
    name="crypt-keeper",
    version="1.1.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "crypt-keeper = crypt_keeper.cli:main",
        ]
    },
    install_requires=[
        "redis ==2.10.3",
        "python-keyczar ==0.715"
    ]
)

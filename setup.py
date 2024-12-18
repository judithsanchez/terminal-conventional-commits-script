from setuptools import setup, find_packages

setup(
    name="conventional-commits",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "prompt_toolkit>=3.0.0",
    ],
    scripts=[
        'scripts/install.sh',
        'scripts/install.bat',
        'scripts/install.py'
    ],
    entry_points={
        "console_scripts": [
            "gcommit=conventional_commits.app:main",
        ],
    },
    author="judithsanchez",
    description="Interactive conventional commits CLI tool with emojis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/conventional-commits",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ],
    },
)
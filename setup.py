from setuptools import setup, find_packages

setup(
    name="ashiart",
    # Version is the single source in ashiart/__init__.py via
    # setup.cfg (attr: ashiart.__version__); do not duplicate it here.
    packages=find_packages(),
    install_requires=[
        "pillow>=10.0.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "video": ["opencv-python>=4.8.0"],
    },
    entry_points={
        'console_scripts': [
            'ashiart=ashiart.cli:main',
        ],
    },
    author="Faycal Amrouche",
    author_email="fayam69420@gmail.com",
    description="A package for generating ASCII art from images",
    url="https://github.com/Faycall1l/Ashiart",
    keywords="ascii, art, image, converter",
    python_requires=">=3.8",
) 
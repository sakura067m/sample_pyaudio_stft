from setuptools import setup

requirements = [
    "numpy",
    "matplotlib",
    "PyQt5",
    "pyaudio",
]

setup(
    name="spectre",
    version="1.0.0",
    description="show the spectre with your mic",
    url="https://github.com/sakura067m/sample_pyaudio_stft",
    author="sakura067m",
    author_email="3IE19001M@s.kyushu-u.ac.jp",
##    license='',  # TBD
    packages=["spectre"],
    package_dir={"spectre": "spectre"},
    package_data={
        "spectre":[]
    },
    entry_points={
        "gui_scripts": ["spectre = spectre.__main__:main"]
    },
    install_requires=requirements,
    python_requires='>=3.4',
    keywords="STFT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],

)

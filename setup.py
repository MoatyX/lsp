import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    pass

setuptools.setup(
    name="lsp-moaty",
    version="0.9",
    author="Moaty",
    author_email="moaty.hassan@navimatix.de",
    description="A tool that generates high level C++ representation of LwM2M Objects and C source that defines "
                "these LwM2M objects in the Zephyr-RTOS environment, from OMA's XML Object Definitions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MoatyX/lsp.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "jinja2",
        "Click"
    ],
    entry_points='''
    [console_scripts]
    lsp=lsp.main:generate_cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)

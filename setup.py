import setuptools

setuptools.setup(
    name='statsmaker',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=[
        "pyro-ppl",
        "torch",
    ],
    url='https://github.com/jialuechen/statsmaker',
    license='Apache-2.0',
    author='Jialue Chen',
    author_email='jialuechen@outlook.com',
    description='Probabilistic Progamming Language (PPL) for Market Microstructure Modeling',
    python_requires=">=3.6"
)

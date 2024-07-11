import setuptools

setuptools.setup(
    name='statsmaker',
    version='0.1.0',
    packages=setuptools.find_packages(),
    install_requires=[
        "pytorch==2.2",
        "pandas==2.2.1",
        "networkx==3.2.1"
    ],
    url='https://github.com/jialuechen/statsmaker',
    license='Apache-2.0',
    author='Jialue Chen',
    author_email='jialuechen@outlook.com',
    description='Probabilistic Progamming Language (PPL) for Market Microstructure Modeling'
)

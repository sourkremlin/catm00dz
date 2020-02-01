import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='catm00dz',
    version='100.0.0',
    author='Kyle',
    author_email='pls dont email me',
    description='For the self-aware cat person',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sourkremlin/catm00dz',
    packages=setuptools.find_packages(),
    install_requires=['pillow'],
    test_requires=['pytest'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: The Unlicense',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'catm00dz=catm00dz.main:main'
        ]        
    },
    python_requires='>=3.6',
)
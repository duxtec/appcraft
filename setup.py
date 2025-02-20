from setuptools import setup, find_packages

setup(
    name='appcraft',
    version='0.2.0',
    description='Um framework que cria estruturas de projeto personalizadas.',
    author='Dux Tecnologia',
    author_email='contato@tpereira.com.br',
    url='https://github.com/duxtec/appcraft',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'appcraft': [
            'templates/**/*',
            'scripts/**/*',
            'utils/**/*',
        ],
    },
    entry_points={
        'console_scripts': [
            'appcraft=appcraft.scripts.cli:main',
        ],
    },
    install_requires=[
        'prompt_toolkit',
        'toml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

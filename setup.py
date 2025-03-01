from setuptools import setup, find_packages

setup(
    name='farm-manager',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer==0.9.0',
        'rich==10.16.2',
        'pydantic==1.10.13',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'numpy==1.26.4',
        'scikit-learn==1.4.0'
    ],
    entry_points={
        'console_scripts': [
            'farm-manager=farm_manager.cli:main',
        ],
    },
    author='Agricultural Management Team',
    description='Herramienta integral de gestión agrícola',
    long_description=open('README.md').read() if open('README.md').read() else 'CLI para gestión agrícola',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

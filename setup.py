from setuptools import setup
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')
REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')

setup(
    name='soap-as-rest-server',
    version='0.0.2',
    description='Soap Proxy Module to get data from SOAP Services',
    long_description=open(README).read(),
    long_description_content_type='text/markdown',
    author='Frank Mendonca', author_email='frankmed57@gmail.com',
    license='MIT',
    keywords=['soap', 'xml', 'json', 'rest'],
    install_requires=open(REQUIREMENTS).readlines(),
    packages=['soap_as_rest_server'],
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    url='https://github.com/frankmendonca/soap-as-rest-server',
    python_requires='>=3.6',
)

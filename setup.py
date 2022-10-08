from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='outscraper',
    version='1.8.0',
    description='Python bindings for the Outscraper API',
    long_description=readme(),
    classifiers = ['Programming Language :: Python',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Topic :: Utilities',
    ],
    keywords='outscraper webscraper extractor google api maps search json scrape parser reviews google play amazon',
    url='https://github.com/outscraper/outscraper-python',
    author='Outscraper',
    author_email='support@outscraper.com',
    license='MIT',
    packages=['outscraper'],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type='text/x-rst',
)

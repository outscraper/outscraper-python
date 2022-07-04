from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='google-services-api',
    version='1.5.1',
    description='Google Maps and Google Maps reviews scraper by Outscraper API',
    long_description=readme(),
    classifiers = ['Programming Language :: Python',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Topic :: Utilities',
    ],
    keywords='extractor google api maps search json scrape parser reviews google play',
    url='https://github.com/outscraper/google-scraper-pyhton',
    author='Outscraper',
    author_email='team@outscraper.com',
    license='MIT',
    packages=['outscraper'],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type='text/x-rst',
)

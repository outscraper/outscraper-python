from setuptools import setup


from outscraper import VERSION


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='google-services-api',
    version=VERSION,
    description='Google services extractor by OutScraper API',
    long_description=readme(),
    classifiers = ['Programming Language :: Python',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Topic :: Utilities',
    ],
    keywords='extractor google api maps search json scrape parser',
    url='http://github.com/outscraper/google-services-api-pyhton',
    author='OutScraper',
    author_email='team@outscraper.com',
    license='MIT',
    packages=['outscraper'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type='text/x-rst',
)

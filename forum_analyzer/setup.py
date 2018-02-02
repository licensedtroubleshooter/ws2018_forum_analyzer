from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='forum_analyzer',
    version='0.01',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Text Processing :: Linguistic', ],
    url='https://www.ya.ru/',
    license='MIT',
    install_requires=['scipy',
                      'numpy',
                      'pandas',
                      'vk',
                      'catboost',
                      'psycopg2',
                      'scikit-learn',
                      'gensim'],
    # dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
    include_package_data=True,
)
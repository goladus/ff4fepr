from setuptools import setup

setup(name='ff4fepr',
      version='0.0.1',
      description="",
      url='http://github.com/goladus/ff4fepr',
      author='Goladus',
      author_email='goladus@goladus.com',
      license='MIT',
      packages=['ff4fepr'],
      scripts=['bin/ff4fe-post-randomizer'],
      install_requires=['pyyaml'],
      package_data={'ff4fepr': ['resources/*.yml',
                                'resources/*.yaml',
                                'resources/*.j2',
                                'resources/*.csv']},
      zip_safe=False)

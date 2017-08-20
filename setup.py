try:
	from setuptools import setup
except ImportError:
	from disutils.core import setup
package = 'pysurvey_analysis'
version = '1.0'

setup(version=version,
	name=package,
	description='Survey Statistics',
	url='http://github.com/anGie44/survey_analysis',
	author='anGie44',
	author_email='angelinepinilla@gmail.com',
	license='',
	packages=['pysurvey_analysis'],
	scripts=['pysurvey_analysis/surveyAnalysis.py'])

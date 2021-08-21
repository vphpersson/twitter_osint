from setuptools import setup, find_packages

setup(
    name='twitter_osint',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'httpx_oauth @ git+ssh://git@github.com/vphpersson/httpx_oauth.git#egg=httpx_oauth',
        'pyutils @ git+ssh://git@github.com/vphpersson/pyutils.git#egg=pyutils'
        'twitter_api @ git+ssh://git@github.com/vphpersson/twitter_api.git#egg=twitter_api'
    ]
)

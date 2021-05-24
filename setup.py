from setuptools import setup, find_packages

setup(
    name='telegramBot',
    packages=find_packages(['telegramBot']),
    version='0.1.0',
    desctiption='telegram bot',
    auth='playmixer',
    license='MIT',
    install_requires=[''],
    setup_requires=['pydantic', 'requests']
)

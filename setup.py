import setuptools

setuptools.setup(
    name='telegramBot',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version='0.1.1',
    desctiption='telegram bot',
    auth='playmixer',
    license='MIT',
    install_requires=['requests'],
    setup_requires=['']
)

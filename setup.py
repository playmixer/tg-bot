import setuptools

setuptools.setup(
    name='telegramBot',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version='0.1.0',
    desctiption='telegram bot',
    auth='playmixer',
    license='MIT',
    install_requires=['pydantic', 'requests'],
    setup_requires=['']
)

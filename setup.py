from setuptools import setup

setup(
    name="portfolio",
    version="1.0",
    packages=['portfolio'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Jinja',
        'Werkzeug',
    ]
)

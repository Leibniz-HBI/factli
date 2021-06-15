from setuptools import setup

setup(
    name='get_posts',
    version='0.1.0',
    py_modules=['get_posts'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'get_posts = get_posts:cli',
        ],
    },
)

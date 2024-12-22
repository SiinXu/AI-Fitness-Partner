from setuptools import setup, find_packages

setup(
    name="ai-fitness-partner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'pandas',
        'numpy',
        'openai',
        'python-dotenv',
        'pyjwt'
    ]
)

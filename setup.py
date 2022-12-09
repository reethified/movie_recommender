from setuptools import setup,find_packages

requirements = [
    'click<=6.0',
    'flask',
    'flask-admin',
    'flask-wtf',
    'flask-restful',
    'flask-bootstrap',
    'implicit',
    'notebook',
    'notebook_shim',
    'numpy',
    'pandas',
    'scikit-learn',
    'scipy',
    'seaborn',

]

setup(
    name = "recommender_app",
    version = "1.0.0",
    author = "Rahul Sharma",
    author_email = "reethified@gmail.com",
    description ="A Recommender app for multiple collaborative filtering implementations-"
                 " User Based collaborative filtering and Item Based Collaborative Filtering",
    license = "BSD",
    keywords = "A Recommender app for multiple collaborative filtering implementations",
    url = "TBD",
    packages=find_packages(include=['recommender_app', 'recommender_app.*']),
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: collaborative filtering"
    ],
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "dataset": ["*.dat"]
    }
)
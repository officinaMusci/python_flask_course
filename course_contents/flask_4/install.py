
# ./setup.py



from setuptools import find_packages, setup


setup(
    name='project',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'python-dotenv',
        'flask-jwt-extended'
    ],
)



# ./MANIFEST.in
# Ici on déclare les fichiers
# statiques à importer
include services/database/schema.sql
graft static
graft templates
global-exclude *.pyc



# On installe, global ou env
# $ pip install -e .

# Maintenant, flask run fonctionne
# partout dans la machine
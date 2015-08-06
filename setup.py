from setuptools import setup

setup(
    name="linnaeus",
    version="v0.0.17",
    author="Mali Akmanalp <Harvard CID>",
    description=("Harvard CID's classification tools."),
    url="http://github.com/cid-harvard/classifications/",
    packages=["linnaeus"],
    package_dir={
        "linnaeus": "."
    },
    install_requires=[
        'unidecode',
    ],
    package_data={
        '': [
            'industry/ISIC/Colombia/out/isic_ac_3.0.csv',
            'industry/ISIC/Colombia/out/isic_ac_4.0.csv',
            'industry/NAICS/Mexico/out/industries_mexico_scian_2007.csv',
            'product/HS/Atlas/out/hs92_atlas.csv',
            'product/HS/Mexico_Prospedia/out/products_mexico_prospedia.csv',
            'product/HS/Colombia_Prospedia/out/products_colombia_prospedia.csv',
            'occupation/SINCO/Mexico/out/occupations_sinco_2011.csv',
            'location/Colombia/DANE/out/locations_colombia_dane.csv',
            'location/Colombia/Prospedia/out/locations_colombia_prosperia.csv',
            'location/Mexico/INEGI/out/locations_mexico_inegi.csv',
            'location/International/DANE/out/locations_international_dane.csv',
        ]
    }
)

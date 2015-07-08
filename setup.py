from setuptools import setup

setup(
    name="linnaeus",
    version="v0.0.8",
    author="Mali Akmanalp <Harvard CID>",
    description=("Harvard CID's classification tools."),
    url="http://github.com/cid-harvard/classifications/",
    packages=["linnaeus"],
    package_dir={
        "linnaeus": "."
    },
    package_data={
        '': [
            'industry/ISIC/Colombia/out/isic_ac_3.0.csv',
            'industry/ISIC/Colombia/out/isic_ac_4.0.csv',
            'product/HS/Atlas/out/hs92_atlas.csv',
            'location/Colombia/DANE/out/locations_colombia_dane.csv',
            'location/Mexico/INEGI/out/locations_mexico_inegi.csv',
        ]
    }
)

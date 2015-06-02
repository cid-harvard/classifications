from setuptools import setup, find_packages

setup(
    name="linnaeus",
    version="v0.0.1",
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
        ]
    }
)

from setuptools import setup

setup(
    name="linnaeus",
    version="v0.0.92",
    author="Mali Akmanalp <Harvard CID>",
    description=("Harvard CID's classification tools."),
    url="http://github.com/cid-harvard/classifications/",
    packages=["linnaeus"],
    package_dir={
        "linnaeus": "."
    },
    install_requires=[
        'unidecode',
        'six'
    ],
    package_data={
        '': [
            'industry/ISIC/Colombia/out/isic_ac_3.0.csv',
            'industry/ISIC/Colombia/out/isic_ac_4.0.csv',
            'industry/ISIC/Colombia_Prosperia/out/industries_colombia_isic_prosperia.csv',
            'industry/NAICS/Mexico/out/industries_mexico_scian_2007.csv',
            'industry/NAICS/Mexico_datlas/out/industries_mexico_scian_2007_datlas.csv',
            'product/Datlas/Rural/out/livestock.csv',
            'product/Datlas/Rural/out/land_use.csv',
            'product/Datlas/Rural/out/agricultural_products.csv',
            'product/Datlas/Rural/out/agricultural_products_expanded.csv',
            'product/Datlas/Rural/out/agricultural_products_census.csv',
            'product/Datlas/Rural/out/nonagricultural_activities.csv',
            'product/Datlas/Rural/out/farm_type.csv',
            'product/Datlas/Rural/out/farm_size.csv',
            'product/HS/Atlas/out/hs92_atlas.csv',
            'product/HS/Mexico_Prospedia/out/products_mexico_prospedia.csv',
            'product/HS/Colombia_Prospedia/out/products_colombia_prospedia.csv',
            'product/HS/Peru_Datlas/out/products_peru_datlas.csv',
            'product/HS/IntlAtlas/out/hs92_atlas.csv',
            'product/SITC/IntlAtlas/out/sitc_rev2.csv',
            'occupation/SINCO/Mexico/out/occupations_sinco_2011.csv',
            'occupation/SINCO/Mexico_datlas/out/occupations_sinco_datlas_2011.csv',
            'occupation/SOC/Colombia/out/occupations_soc_2010.csv',
            'location/Colombia/DANE/out/locations_colombia_dane.csv',
            'location/Colombia/Prospedia/out/locations_colombia_prosperia.csv',
            'location/Mexico/INEGI/out/locations_mexico_inegi.csv',
            'location/Peru/INEI/out/locations_peru_inei.csv',
            'location/Peru/datlas/out/locations_peru_datlas.csv',
            'location/International/DANE/out/locations_international_dane.csv',
            'location/International/Mexico/out/locations_international_mexico.csv',
            'location/International/ISO-CID/out/locations_international_iso_cid.csv',
            'location/International/Atlas/out/locations_international_atlas.csv',
        ]
    }
)

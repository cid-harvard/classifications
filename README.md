# Harvard CID Repository of Classification Systems

Classification systems that Harvard CID has cleaned, available for you as CSVs, sometimes along with how we generated them.

## Background

Over time at CID, we've come to know and work with a number of product, industry, occupation and location classification systems. While these are often international standards, there usually are regional variations, historical version differences and other factors that that complicate the life of a researcher. Oftentimes, the format these classification systems are delivered in are unsuitable for computer processing - often just dumped into a table in a website or in a PDF file or word document. We would like to provide to researchers and the general public the results of our efforts to clean this data.

## Available data

type|name|adaptation|localized name|version|description|link
----|----|----------|--------------|-------|-----------|----
industry|ISIC|Colombia|CIIU 4 A.C.|4.0|ISIC 4.0, colombian version.|[here](industry/ISIC/Colombia)
industry|ISIC|Colombia|CIIU 3 A.C.|3.0|ISIC 3.0, colombian version.|[here](industry/ISIC/Colombia)
product|HS|International|Harmonized System|1992|Harmonized system, as used by the Atlas of Economic Complexity.|[here](product/HS/Atlas)
location|DANE Divipola |||2015-03-31|Colombian administrative regions, from DANE.|[here](location/Colombia/DANE)

## Guidelines

1. Data must be easily accessible and usable. There is no point to data that isn't. We're trying to help with this.
2. Provenance must be clear whenever possible. The original source must be cited and linked. Data without a source cannot be considered reliable and might as well not exist. Data that has a clear source that is difficult to access is still bad. 
3. Cleaning methodology (and wherever possible, code) must be provided. The best is to have code that processes the raw inputs directly and produces the cleaned data, in a manner that others can reproduce, or in a manner that, when there is a change or update to the original source, you can repeat.
4. We're using CSV files because it's the most common and interchangeable format, and does not require proprietary software (MS Access, STATA). We're using quoted string fields whenever necessary.
5. We're trying to stick to UTF-8 encoding for the files to accommodate different languages, but will provide tools to get rid of non-ascii characters in csv files to support a wider variety of software.

## Directory Structure

Files are split into:
- type of classification (e.g. product, industry, occupation)
- name of classification (e.g. ISIC, SITC, HS, ONET)
- adaptation (a specific country or international)

Then the resulting directory contains
- out/: the cleaned data
- in/: if the data was hand-processed in any way before automatic processing, that should be in here.
- raw/: a folder with a copy of the raw data
- Whatever code is necessary to generate the out/ data, if available.

## Contributions

Contributions are welcome! If you're familiar with git and github, please do a pull request. Otherwise, get in touch with me.

### Examples of bad contributions:

Data that is super useful, yet:
- you found on a USB drive somewhere and don't know where it came from
- can't explain, step by step, how you created it or what you changed
- people changed it over the years and you're not sure how it relates to the original
- is still messy

If you get in touch with me, I will do my personal best to get your prospective contribution into good shape, including helping you with code and automation and converting formats.

## Contact

Please get in touch with mali underscore akmanalp at hks dot harvard dot edu.

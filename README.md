# Harvard CID Repository of Classification Systems

Summary: Classification systems that Harvard CID has cleaned, available for you as CSVs, sometimes along with how we generated them.

## Background

Over time at CID, we've come to know and work with a number of product, industry, occupation classification systems. While these are often international standards, there usually are regional variations, historical version differences and other factors that that complicate the life of a researcher. Oftentimes, the format these classification systems are delivered in are unsuitable for computer processing - often just dumped into a table in a website or in a PDF file or word document. We would like to provide to researchers and the general public the results of our efforts to clean this data.

## Manifesto

1. Provenance must be clear whenever possible. The original source must be cited and linked. Data without a source cannot be considered reliable and might as well not exist. Data that has a clear source that is difficult to access is only slightly better. 
2. Cleaning methodology (and wherever possible, code) must be provided.
3. We're using CSV files because it's the most common and interchangeable format. We're using quoted string fields whenever necessary.
4. We're trying to stick to UTF-8 encoding for the files to accomodate , but will provide tools to get rid of non-ascii characters in csv files to support legacy tools such as STATA.

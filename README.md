# OMIM-Spider
A spider for OMIM(Online Mendelian Inheritance in Man) using Python 3.6 .
## Project Introduction
OMIM is a comprehensive, authoritative compendium of human genes and genetic phenotypes that is freely available and updated daily.
In order to analyze the relation between different diseases or genes, we implement a spider to crawl the data which diseases molecular
basis was known.
- omim.py is main program. it mainly uses API key(need to apply: https://omim.org/api) to accquire the data.
- inheritance_modifiy.py: mainly to standardize the data of inheritance. Format: {inheritance; identifiers in different medical 
ontology}
- molecularBasis_modify.py: mainly to standardize the data of molecularBasis. {gene, gene number}
- phenotype_modify.py: mainly to standardize the data of phenotype. {phenotype description; SNOMEDCT ID; UMLS ID; ICD10CM ID; 
ICD9CM ID; HPO ID} 
## Supplement materials
- SNOMEDCT: https://uts.nlm.nih.gov//snomedctBrowser.html#722431007;0;0;CONCEPT_ID;null;SNOMEDCT_US;null;true;
- UMLS: https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?query=C0266619&v%3Aproject=nlm-main-website&utm_expid=.mlzP9bTAQJ-7kAp-iWFk_A.0&utm_referrer=
- HPO: http://compbio.charite.de/hpoweb/showterm?id=HP:0000118
- ICD9CM: https://www.cdc.gov/nchs/icd/icd9cm.htm
- ICD10CM: https://www.cdc.gov/nchs/icd/icd10cm.htm

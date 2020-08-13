# name-classifier
This project builds a name-classifier to parse name for people, household and corporation.
Input File: 2020-07-30 12-49-08.786143-assessor.xlsx
Output File: output.json
Package Installation: pip install probablepeople 

There are 3 possible name types: 'Person', 'Household', 'Corporation'

There can be one or multiple owner names/ last buyer names correspoding to one address (one record/ one row). 

The name (names) is saved in a list for each address (record) in the output file.
All addresses' owners names are saved in a list as the value to the key 'Owners Names' in the output.json file.
All addresses' buyers names are saved in a list as the value to the key 'Buyers Names' in the output.json file.
Therefore, the value to the key 'Owners Names' is a list of owners names list in the output.json file and the number of sublists is the number of records (rows) in the input file.
So is the case for the value to the key 'Buyers Names' in the output.json file.

For name parsed as type 'Person', formated output name is saved as:
	{'LastName': '', 'MiddleName': '', 'FirstName': ''} 
where 'LastName' can be parsed 'LastName' or 'Surname' or 'LastInitial', and '' is given if none of above is available.

For name parsed as type 'Household' or 'Corporation', original parsed result is given for user's choice later.

If there is an error of parsing, when the error information is given as 'Unable to tag this string because more than one area of the string has the same label', the original name and the parsed name are given for user's correction in the future.
NOTE: When this error is raised, it's likely that either (1) the string is not a valid person/corporation name or (2) some tokens were labeled incorrectly.

For example, the result of running the command probablepeople.tag('O KINSELLA SHAUN M O KINSELLA KEVEN') is an error with the following information.

ORIGINAL STRING:  O KINSELLA SHAUN M O KINSELLA KEVEN
PARSED TOKENS:    [('O', 'Surname'), ('KINSELLA', 'Surname'), ('SHAUN', 'GivenName'), ('M', 'MiddleInitial'), ('O', 'Surname'), ('KINSELLA', 'Surname'), ('KEVEN', 'GivenName')]
UNCERTAIN LABEL:  Surname


The strategy for this version is as follows.
(1) If the name has any of the following string part
corporate_list = ["CO", "LLC", "TRUST", "LL", "LP", "DEPARTMENT", "PLAN", "OF", "INC", "FAMILY", "PROPERTIES",
                  "REVOCABLE", "ESTATES", "&", "INVESTMENTS"]
it is categorized as a "Corporation" by our definition.
(2) Otherwise, the first part of the name is regarded as the Last Name of a person by our definition.
(3) If there is a conflict between our categorization and the package's categorization of the name, i.e. a name with the first part as the Last Name is regarded as a person's name by us while a corporation's name by the package, the name can not be parsed into "First Name", "Middle Name", and "Last Name". Therefore, the result for this kind of name is set as "TBD: name" and needs manual parse.

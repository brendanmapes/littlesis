# littlesis
[![MIT License](https://img.shields.io/npm/l/starwars-names.svg?style=flat-square)](http://test.pypi.org/project/littlesis/)

Python wrapper for the LittleSisAPI. Makes using the LittleSis API more efficient for the Python user, and allows for simpler data exploration on API calls, specifically get requests. View the docs for the LittleSis API [here](https://littlesis.org/api) to better understand exactly the types of get requests this package performs.

## Installation
#### pip
```bash
$ pip install littlesis
```
#### github
[Download latest version here](https://github.com/brendanmapes/littlesis)

## Usage
### import littlesis module
```python
import littlesis
from littlesis import littlesis
```
#### id_to_name()
```python
id_to_name(96583)
'Ted Cruz'
```
Converts any ID number in the LittleSis database to the name of the individual or entity which it represents. 

#### name_to_id()
```python
name_to_id('Ted Cruz')
96583
```
Converts any name within the LittleSis database to the corresponding ID number. If shortened versions of the name are used, the function will return the ID number of the entity with the highest number of relationships documented on the site.
```python
name_to_id('Cruz')
96583
```

#### entity()
```python
entity('Barack Obama')
```
This returns a JSON of an entity get request to the LittleSis API, which includes basic information on who/what the entity is. Originally, get requests to this API require knowledge of the ID for each entity, but this function allows for entry of entities by name instead.

#### relationship()
```python
relationship('Barack Obama')
```
This returns a JSON of a relationship get request to the LittleSis API, which includes a list of related entities to the individual entered in the function, and information on the nature of each of those relationships. Again, this function avoids the necessity of knowledge for the ID for a given entity in the original API requests, and allows for entry of entities by name. As with all functions in this package, shortened versions of the names used in the function (last names) will call for information on the entity that has the highest number of relationships documented in the database. 

#### list_entities()
```python
list_entities('Trump', 'Obama', 'Bill Clinton')
```
This returns a pandas dataframe from entity get requests to the LittleSis API for all entities listed in the function call. This allows for basic exploration of the information within these get requests, without manual individual calls to the API, which only allows for one entity to be entered at a time. Due to rate limiting restrictions on the LittleSis API, this function has been throttled down to work at a rate that avoids rate limit related failure (1 request per second). 

#### relationships_df()
```python
relationsihps_df('Lebron James')
```
This returns a dataframe of information for all related entities for the entity entered into the function. This function performs a relationship get request to the LittleSis API, and parses it into a dataframe, converting all ID numbers for each related entity to the names of the entity, which isn't included in the standard API get request. Again, to avoid rate limit related failure, this function works at a rate of one call per second, which results in a total run time of about 1 second per related entity listed. 

#### timelines()
```python
timelines('Lebron James')
```
This returns a dataframe of information on the time period of relationships for the entity entered into the function by name. ID numbers in the original relationship get request are converted to the name of the entity, again, requiring throttling to avoid rate limit related failure. 

#### bio()
```python
bio('Obama')
'The 44th President of the United States, he was sworn into office on January 20,
    2009; born in Honolulu, Hawaii, August 4, 1961; obtained early education in Jakarta,
    Indonesia, and Hawaii; continued education at Occidental College, Los Angeles, Calif.;
    received a B.A. in 1983 from Columbia University, New York City; worked as a community 
    organizer in Chicago, Ill.; studied law at Harvard University, where he became the 
    first African American president of the Harvard Law Review, and received J.D. in 1991;
    lecturer on constitutional law, University of Chicago; member, Illinois State senate
    1997-2004; elected as a Democrat to the U.S. Senate in 2004 for term beginning January
    3, 2005.'
```
This returns a string of biographical/background information on the entity entered to the function by name. 

#### lists()
```python
lists('Lebron James')
Bloomberg Business Week Most Powerful Athletes (2011)
The World's Highest Paid Celebrities (2017)
```
This returns a list of the lists to which the entity belongs within the LittleSis database.

#### lists_w_descriptions()
```python
lists('Lebron James')
Bloomberg Business Week Most Powerful Athletes (2011) (description: The 100 most
    powerful athletes on and off the field. No coaches, owners, managers, executives or
    retired athletes were considered. Off-field metrics included the results of polls on
    individual athletes by E-Poll Market Research and estimated endorsement dollars. On
    field metrics were tallied on those who outscored, out-tackled, or outskated the
    competition during 2009 and 2010. Sports were weighted according to their popularity
    in the U.S. )
    The World's Highest Paid Celebrities (2017) (description: FORBES' annual ranking of
    the highest-earning entertainers in the world, published June 12 2017. The list
    evaluates front of camera talent; fees for agents, managers and lawyers are not
    deducted. )
```
This returns a similar list to that produced by the lists() function, but includes expanded descriptions for the lists to which the entity belongs. 

#### relationship_blurbs()
```python
relationship_blurbs('Lebron James')
    LeBron James  gave money to  Children’s Aid Society 
    LeBron James  and  Savannah Brinson James  are/were in a family
    LeBron James  and  Rich Paul  are/were business partners
    Randy Mims  and  LeBron James  have/had a professional relationship
    LeBron James  has a position (Founder  ) at  James Family Foundation 
    Maverick Carter  and  LeBron James  are/were business partners
    LeBron James  is an owner of  Blaze Pizza LLC 
    LeBron James  has a position (Co founder  ) at  Klutch Sports 
    LeBron James  gave money to  Democratic National Committee 
    LeBron James  gave money to  Democratic White House Victory Fund 
    Aaron Goodwin  and  LeBron James  have/had a professional relationship
```
This returns a list of all relationships documented for the given entity within the LittleSis database. This function is performing a relationship get request for the given entity, and filtering that information to select simply the relationship descriptors, for quick read and analysis. 

#### relationship_blurbs_w_amounts()
```python
relationship_blurbs_w_amounts('Lebron James')
    LeBron James  gave money to  Children’s Aid Society  None
    LeBron James  and  Savannah Brinson James  are/were in a family None
    LeBron James  and  Rich Paul  are/were business partners None
    Randy Mims  and  LeBron James  have/had a professional relationship None
    LeBron James  has a position (Founder  ) at  James Family Foundation  None
    Maverick Carter  and  LeBron James  are/were business partners None
    LeBron James  is an owner of  Blaze Pizza LLC  None
    LeBron James  has a position (Co founder  ) at  Klutch Sports  None
    LeBron James  gave money to  Democratic National Committee  20000
    LeBron James  gave money to  Democratic White House Victory Fund  20000
    Aaron Goodwin  and  LeBron James  have/had a professional relationship None
```
Similarly to relationship_blurbs(), this function returns a list of all relationships for the given entity, but includes dollar amounts that relationship involved, which is often a primary piece of information being searched for when using the LittleSis API to understand things like political campaign contributions.


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`littlesis` was created by Brendan Mapes. It is licensed under the terms of the MIT license. See below.

Copyright (c) 2021 Brendan Mapes

MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits

`littlesis` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Further Guidance
View more in depth usage guide [here](https://littlesis.readthedocs.io/en/latest/autoapi/littlesis/littlesis/index.html).

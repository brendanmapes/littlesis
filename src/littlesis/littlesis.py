import pandas as pd
import requests
import ratelimit
from ratelimit import limits
from ratelimit import sleep_and_retry

def id_to_name(x):
    """
    Converts from LittleSis ID number to name. 
    
    Parameters
    ----------
    x  LittleSis ID number
    
    Example
    -------
    >>> id_to_name(96583)
    'Ted Cruz'
    """
    
    path = 'https://littlesis.org/api/entities/{}'.format(x)
    response = requests.get(path)
    response = response.json()
    name = response['data']['attributes']['name']
    return name

def name_to_id(name):
    """
    Converts from name to LittleSis ID number. Resorts to entity with the highest number of relationships listed for entries that
    point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name : Name to be converted
    
    Example
    -------
    >>> name_to_id('Ted Cruz')
    96583
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    return ID

def entity(name): 
    """
    Provides info from entity get request to LittleSis API, by name input rather than id 
    input as is required in original get request format, in JSON format. Resorts to entity with the highest number of relationships listed
    for entries that point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name: Name of 1 individual or organization for which information is desired.
    
    Example
    -------
    >>> entity('Barack Obama'
    {'meta': {'copyright': 'LittleSis CC BY-SA 4.0',
      'license': 'https://creativecommons.org/licenses/by-sa/4.0/',
      'apiVersion': '2.0'},
     'data': {'type': 'entities',
      'id': 13503,
      'attributes': {'id': 13503,
       'name': 'Barack Obama',
       'blurb': '44th President of the United States',
       'summary': 'The 44th President of the United States, he was sworn into office on January 20, 2009; born in Honolulu, Hawaii, August
       4, 1961; obtained early education in Jakarta, Indonesia, and Hawaii; continued education at Occidental College, Los Angeles,
       Calif.; received a B.A. in 1983 from Columbia University, New York City; worked as a community organizer in Chicago, Ill.; studied
       law at Harvard University, where he became the first African American president of the Harvard Law Review, and received J.D. in
       1991; lecturer on constitutional law, University of Chicago; member, Illinois State senate 1997-2004; elected as a Democrat to the
       U.S. Senate in 2004 for term beginning January 3, 2005.',
      'website': 'http://obama.senate.gov/',
       'parent_id': None,
       'primary_ext': 'Person',
       'updated_at': '2021-12-15T21:28:15Z',
       'start_date': '1961-08-04',
       'end_date': None,
       'aliases': ['Barack Obama'],
       'types': ['Person', 'Political Candidate', 'Elected Representative']},
      'links': {'self': 'https://littlesis.org/entities/13503-Barack_Obama'}}}
      """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path2 = 'https://littlesis.org/api/entities/{}'.format(ID)
    response2 = requests.get(path2)
    response2 = response2.json()
    return response2

def relationships(name): 
    """
    Provides info from relationships get request to LittleSis API, by name input rather
    than id input as is required in original get request format, in JSON format. Resorts to entity with the highest number of
    relationships listed for entries that point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name: name: Name of 1 individual or organization for which information is desired.
    
    Example
    -------
    >>>relationships('Steve Jobs')
    {'meta': {'currentPage': 1,
      'pageCount': 1,
      'copyright': 'LittleSis CC BY-SA 4.0',
      'license': 'https://creativecommons.org/licenses/by-sa/4.0/',
      'apiVersion': '2.0'},
     'data': [{'type': 'relationships',
       'id': 1643319,
       'attributes': {'id': 1643319,...
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path2 = 'https://littlesis.org/api/entities/{}/relationships'.format(ID)
    response2 = requests.get(path2)
    response2 = response2.json()
    return response2

@sleep_and_retry
@limits(calls=1, period=1)
def basic_entity(name): 
    """
    Creates pandas dataframe for one individual or entity with basic information from
    entity get request to LittleSis API. Resorts to entity with the highest number of relationships listed for entries that
    point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name: Name of 1 information or entity for which information is desired.
    
    Example
    -------
    >>> basic_table('Steve Jobs')
    info        name                                            aliases  \
    0     Steve Jobs  [Steven P Jobs, Steve Jobs, Mr Steven "Steve P...   

    info                         blurb date_of_birth    end_date  \
    0     Apple co-founder, former CEO    1955-02-24  2011-10-05   

    info                      types  website  
    0     [Person, Business Person]      NaN  
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path2 = 'https://littlesis.org/api/entities/{}'.format(ID)
    response2 = requests.get(path2)
    response2 = response2.json()
    data2 = response2['data']['attributes']
    df = pd.DataFrame(list(data2.items()))
    df.columns = ['info', 'value']
    df = pd.pivot(df, columns = 'info', values = 'value')
    df = df.fillna(method='bfill', axis=0)
    df = df.iloc[:1, :]
    df = df[['name', 'aliases', 'blurb', 'start_date', 'end_date', 'types', 'website']]
    df.rename(columns = {'start_date': 'date_of_birth'}, inplace = True)
    return df

@sleep_and_retry
@limits(calls=1, period=1)
def list_entities(*args):
    """
    Concatenates dataframes created by basic_table() for entity get requests to LittleSis
    API, resulting in pandas dataframe of multiple rows. Resorts to entity with the highest number of relationships listed for entries
    that point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    *args: List of names of individuals or entities for which to include information in
    the resluting dataframe. 
    
    Example
    -------
    >>> list_table('Steve Jobs', 'Lebron James')
    info          name                                            aliases  \
    0       Steve Jobs  [Steven P Jobs, Steve Jobs, Mr Steven "Steve P...   
    1     LeBron James                                     [LeBron James]   

    info                         blurb date_of_birth    end_date  \
    0     Apple co-founder, former CEO    1955-02-24  2011-10-05   
    1         NBA/Los Angeles Lakers—F    1984-12-30         NaN   

    info                                         types  website  
    0                        [Person, Business Person]      NaN  
    1     [Person, Business Person, Media Personality]      NaN  
    """
    
    list_of_dfs = []
    for name in args:
        df = basic_entity(name)
        list_of_dfs.append(df)
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    return combined_df
   
@sleep_and_retry
@limits(calls=1, period=1)
def id_to_name(x):
    path = 'https://littlesis.org/api/entities/{}'.format(x)
    response = requests.get(path)
    if response.status_code != 200:    
        raise Exception('API response: {}'.format(response.status_code))
    else:
        response = response.json()
        name = response['data']['attributes']['name']
        return name
def relationships_df(name): 
    """
    Creates pandas dataframe with information from relationships get request to LittleSis
    API.
    
    Parameters
    ----------
    name: Name of one individual or organization for which relationship information is
    desired and included in the dataframe. 
    
    Example
    -------
    >>> relationships_df('Lebron James')
                             primary_entity   related_entity amount currency  \
    0                Children’s Aid Society     LeBron James   None     None   
    1                Savannah Brinson James     LeBron James   None     None 
    ...
                      category goods filings  \
    0                      None  None    None 
    ...
    """
    
    path_for_ID_search = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path_for_ID_search)
    response = response.json()
    ID = response['data'][0]['id']
    path_for_relationships = 'https://littlesis.org/api/entities/{}/relationships'.format(ID)
    response2 = requests.get(path_for_relationships)
    response2 = response2.json()
    relationships = pd.DataFrame(response2['data'])
    relationships = pd.DataFrame.to_dict(relationships)
    blurbs = pd.DataFrame(relationships['attributes'])
    blurbs = blurbs.T
    blurbs = blurbs[['entity2_id', 'entity1_id', 'amount', 'currency', 'description1', 'goods', 'filings', 'description', 'start_date',
    'end_date', 'is_current']]
    blurbs['entity1_id'] = blurbs['entity1_id'].apply(id_to_name)
    blurbs['entity2_id'] = blurbs['entity2_id'].apply(id_to_name)
    blurbs.rename(columns = {'entity2_id': 'primary_entity','entity1_id': 'related_entity', 'description1':'category'}, inplace = True)
    return blurbs


def timelines(name): 
    """
    Creates dataframe specifically from timeline information of relationships from
    relationships get request on LittleSis API. Resorts to entity with the highest number of relationships listed for entries that
    point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name: Name of one individual or organization for which relationship information is
    desired and included in the dataframe. 
    
    Example
    -------
    >>> timelines('LeBron James')
    earched_entity   related_entity  start_date  \
    0                Children’s Aid Society     LeBron James        None   
    1                Savannah Brinson James     LeBron James        None   
    ...
      end_date is_current  
    0         None       None  
    1         None       None  
    ...
    """
    
    path_for_ID_search = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path_for_ID_search)
    response = response.json()
    ID = response['data'][0]['id']
    path_for_relationships = 'https://littlesis.org/api/entities/{}/relationships'.format(ID)
    response2 = requests.get(path_for_relationships)
    response2 = response2.json()
    relationships = pd.DataFrame(response2['data'])
    relationships = pd.DataFrame.to_dict(relationships)
    blurbs = pd.DataFrame(relationships['attributes'])
    blurbs = blurbs.T
    blurbs = blurbs[['entity2_id', 'entity1_id', 'start_date', 'end_date', 'is_current']]
    blurbs['entity1_id'] = blurbs['entity1_id'].apply(id_to_name)
    blurbs['entity2_id'] = blurbs['entity2_id'].apply(id_to_name)
    blurbs.rename(columns = {'entity2_id': 'searched_entity','entity1_id': 'related_entity'}, inplace = True)
    return blurbs

def bio(name): 
    """
    Provides paragraph biography/background description of 1 individual or entity from an entity get request on LittleSis API. Resorts to
    entity with the highest number of relationships listed for entries that point to multiple entites (like last name only entries). 
    
    Parameters
    ----------
    name: Name of one individual or organization for which biographical information is desired. 
    
    Example
    -------
    >>> bio('Barack Obama')
    'The 44th President of the United States, he was sworn into office on January 20,
    2009; born in Honolulu, Hawaii, August 4, 1961; obtained early education in Jakarta,
    Indonesia, and Hawaii; continued education at Occidental College, Los Angeles, Calif.;
    received a B.A. in 1983 from Columbia University, New York City; worked as a community 
    organizer in Chicago, Ill.; studied law at Harvard University, where he became the 
    first African American president of the Harvard Law Review, and received J.D. in 1991;
    lecturer on constitutional law, University of Chicago; member, Illinois State senate
    1997-2004; elected as a Democrat to the U.S. Senate in 2004 for term beginning January
    3, 2005.'
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path2 = 'https://littlesis.org/api/entities/{}'.format(ID)
    response2 = requests.get(path2)
    response2 = response2.json()
    response2 = response2['data']['attributes']['summary']
    return response2

def lists(name): 
    """
    Provides list of all lists that the entity belongs to on the LittleSis website, from a
    LittleSis lists get request. Resorts to entity with the highest number of relationships listed for entries that
    point to multiple entites (like last name only entries). 
    
    Parameters
    ---------
    name: Name of one individual or organization for which relationship information is
    desired and included in the list of list memberships is desired. 
    
    Example
    -------
    >>> lists('Lebron James')
    Bloomberg Business Week Most Powerful Athletes (2011)
    The World's Highest Paid Celebrities (2017)
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path = 'https://littlesis.org/api/entities/{}/lists'.format(ID)
    response = requests.get(path)
    response = response.json()
    data = pd.DataFrame(response['data'])
    data = pd.DataFrame.to_dict(data)
    names = pd.DataFrame(data['attributes'])
    names = pd.DataFrame.to_dict(names)
    for key, value in names.items():
        print(value['name'])

        
def lists_w_descriptions(name): 
    """
    Provides list of lists to which the entity belongs on the LittleSis website, from a
    lists get request to the API, with added descriptions for the lists included if they
    exist on the site. Resorts to entity with the highest number of relationships listed for entries that
    point to multiple entites (like last name only entries). 
    
    Parameters
    ---------
    name: Name of one individual or organization for which list of list membership is
    desired. 
    
    Example
    -------
    >>> lists_w_descriptions('Lebron James')
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
    """
    
    path = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path)
    response = response.json()
    ID = response['data'][0]['id']
    path = 'https://littlesis.org/api/entities/{}/lists'.format(ID)
    response = requests.get(path)
    response = response.json()
    data = pd.DataFrame(response['data'])
    data = pd.DataFrame.to_dict(data)
    names = pd.DataFrame(data['attributes'])
    names = pd.DataFrame.to_dict(names)
    for key, value in names.items():
        print(value['name'], '(description:', value['description'],')')
        
def relationship_blurbs(name): 
    """
    Provides a list of blurbs from the relationship get request to the LittleSis API,
    allowing for inspection of all relationships for the requested entity. Resorts to entity with the highest number of relationships
    listed for entries that point to multiple entites (like last name only entries). 
    
    Parameters
    ---------
    name: Name of one individual or organization for which relationship information is
    desired and included in the list. 
    
    Example
    -------
    >>> relationship_blurbs('Lebron James')
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
    """
    
    path_for_ID_search = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path_for_ID_search)
    response = response.json()
    ID = response['data'][0]['id']
    path_for_relationships = 'https://littlesis.org/api/entities/{}/relationships'.format(ID)
    response2 = requests.get(path_for_relationships)
    response2 = response2.json()
    relationships = pd.DataFrame(response2['data'])
    relationships = pd.DataFrame.to_dict(relationships)
    blurbs = pd.DataFrame(relationships['attributes'])
    blurbs = pd.DataFrame.to_dict(blurbs)
    for key, value in blurbs.items():
        print(value['description'])
        
def relationship_blurbs_w_amounts(name): 
    """
    Provides a list of blurbs from the relationship get request to the LittleSis API,
    allowing for inspection of all relationships for the requested entity, and includes number amounts of donation size alongside each
    blurb. Resorts to entity with the highest number of relationships listed for entries that point to multiple entites (like last name
    only entries). 
    
    Parameters
    ---------
    name: Name of one individual or organization for which relationship information is
    desired and included in the list. 
    
    Example
    -------
    >>> relationship_blurbs_w_amounts('Lebron James')
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
    """
    
    path_for_ID_search = 'https://littlesis.org/api/entities/search?q={}'.format(name)
    response = requests.get(path_for_ID_search)
    response = response.json()
    ID = response['data'][0]['id']
    path_for_relationships = 'https://littlesis.org/api/entities/{}/relationships'.format(ID)
    response2 = requests.get(path_for_relationships)
    response2 = response2.json()
    relationships = pd.DataFrame(response2['data'])
    relationships = pd.DataFrame.to_dict(relationships)
    blurbs = pd.DataFrame(relationships['attributes'])
    blurbs = pd.DataFrame.to_dict(blurbs)
    for key, value in blurbs.items():
        print(value['description'], (value['amount']))        

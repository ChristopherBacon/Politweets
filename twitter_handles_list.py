"""
Politweets Python Project
Using Twitter API to scrape tweets then sentiment analysis with Textblob, finally present using Streamlit
This is the cleaning twitter handles and creating party column section
"""

import pandas as pd

# The handles are all from the excellent website https://www.politics-social.com stumbled on this midway through my project
more_handles = pd.read_csv(r'MPs_twitter.csv')
politweets = pd.read_csv(r'politweets.csv')
extra_mps = ['@AdamHollowayMP', '@NadineDorries', '@PBottomleyMP', '@davidmorrisml', '@nigelmp', '@JamieHWStone']
additional_mps = {'AdamHollowayMP': 'Conservative',
                  'NadineDorries': 'Conservative',
                  'PBottomleyMP': 'Conservative',
                  'davidmorrisml': 'Conservative',
                  'nigelmp': 'Conservative',
                  'JamieHWStone': 'Liberal Democrat'}


def mps_list_additional(more_handles, extra_mps):
    """ take list of handles and add in extras"""
    # mps to list
    new_handles_list = more_handles['Screen name'].to_list()
    # add extra mps to original list
    for mp in extra_mps:
        new_handles_list.append(mp)
    return new_handles_list


def clean_handles(new_handles_list):
    """ strip @ from mps so can be compared against twitter data scrape"""
    # some quick cleaning of the handles
    cleaned_handles = []
    for mp in new_handles_list:
        mp = mp.strip(' ').replace('@', '')
        cleaned_handles.append(mp)
    return cleaned_handles


def mp_handles_dict(cleaned_handles):
    """create mp handles dict from"""
    party_dict = dict(zip(cleaned_handles, more_handles.Party))
    return party_dict


def additional_mps_to_dict(additional_mps, party_dict):
    """ add any additional mps to the mp dicitonary to map to scraped data"""
    # add a few extra mps that were missing
    party_dict.update(additional_mps)
    return party_dict


def drop_wrong_handles(politweets):
    """drops list of handles from dataframe"""
    politweets = politweets[(politweets.screen_name != 'Davidmpmorris') |
                            (politweets.screen_name != 'DrDanPoulter') |
                            (politweets.screen_name != 'ElectNigel') |
                            (politweets.screen_name != 'transportgovuk')
                            ]

    return politweets


def create_party_column(politweets, new_dict):
    """update politweets with political party column"""
    # chose 1 to fill the empty party entries
    politweets['party'] = politweets['screen_name'].map(new_dict)
    return politweets


def check_if_parties_missing_after_dic_map():
    """check if any party is missing"""
    # have chosen 1 to act as filter number for empty party
    missing_party = len(politweets[politweets['party'] == 1])
    return missing_party


# these variables will help create party column, remove & update mps
new_handles_list = mps_list_additional(more_handles, extra_mps)
cleaned_handles = clean_handles(new_handles_list)
party_dict = mp_handles_dict(cleaned_handles)
plus_extras_dict = additional_mps_to_dict(additional_mps, party_dict)

#additional column creation and cleaning
politweets = pd.read_csv(r'politweets.csv')
politweets['party'] = politweets['screen_name'].map(plus_extras_dict)
politweets['party'].fillna(1)
politweets = drop_wrong_handles(politweets)
politweets.to_csv(r'politweets.csv', index=False)



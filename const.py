# Copyright (c) 2018 LAC Co.,Ltd.
# All rights reserved.
#
# This software is released under the BSD License.
# https://opensource.org/licenses/BSD-2-Clause

# define constants

# MISP URL
MISP_URL = 'https://example.misp'

# import configuration dictionary.
#
# key: user account(mail address)
# value: dictionary containing the following keys.
#
# 	authkey: valid authkey for user account.
#
# 	distribution: One of the following constants.
DISTRIBUTION_YOUR_ORGANIZATION = '0'
DISTRIBUTION_THIS_COMMUNITY = '1'
DISTRIBUTION_CONNECTED_COMMUNITIES = '2'
DISTRIBUTION_ALL_COMMUNITIES = '3'
DISTRIBUTION_SHARING_GROUP = '4'

# 	threat_level: One of the following constants
THREAT_LEVEL_HIGH = '1'
THREAT_LEVEL_MIDIUM = '2'
THREAT_LEVEL_LOW = '3'
THREAT_LEVEL_UNDEFINED = '4'

# 	analysis_level:  One of the following constants
ANALYSIS_LEVEL_INITIAL = '0'
ANALYSIS_LEVEL_ONGOING = '1'
ANALYSIS_LEVEL_COMPLETED = '2'

IMPORT_CONFIG = {
    'sample1@user.email': {
        'authkey': 'sample1 user authkey', 'distribution': DISTRIBUTION_YOUR_ORGANIZATION, 'threat_level': THREAT_LEVEL_MIDIUM, 'analysis_level': ANALYSIS_LEVEL_COMPLETED
    }, 'sample2@user.email': {
        'authkey': 'sample2 user authkey', 'distribution': DISTRIBUTION_THIS_COMMUNITY, 'threat_level': THREAT_LEVEL_MIDIUM, 'analysis_level': ANALYSIS_LEVEL_COMPLETED
    }
}

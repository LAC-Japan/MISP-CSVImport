# define constants

# API key dictionary.
# key: user account(mail address)
# value: apikey
MISP_APIKEYS = {
	'sample@user.email': 'authkey'
}

# MISP URL
MISP_URL = 'https://example.misp'

# distribution
# your_organization = 0
# this_community = 1
# connected_communities = 2
# all_communities = 3
# sharing_group = 4
DISTRIBUTION = '0'

# threat level
# high = 1
# medium = 2
# low = 3
# undefined = 4
THREAT_LEVEL = '2'

# analysis level
# initial = 0 
# ongoing = 1
# completed = 2
ANALYSIS_LEVEL = '0'

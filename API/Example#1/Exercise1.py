#Exercise #1 : Collecting IOCs

#client.search.submission --> /api/v4/search/index/
SID = 'XXXXXXX'

# Store IOCs in variables that can be used to dump to disk to sent to another process
SUB_COLLECTED_IOCS, ONT_COLLECTED_IOCS = dict(), dict()

# Pull IOCs from submission (without Ontology API)
#client.submission.summary --> /api/v4/submission/summary/sid/ 

# Pull IOCs from submission (with Ontology API) 
#client.ontology.submission --> /api/v4/ontology/submission/sid/ 
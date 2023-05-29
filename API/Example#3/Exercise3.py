#Exercise #3: Ingest files through Ingest API

# Files within this directory will be ingested to Assemblyline
INGEST_DIR = '/tmp/'
QUEUED_IDS = []
NOTIF_QUEUED_IDS = [] 
NOTIFICATION_QUEUE_NAME = "testing_queue"
# Submission parameters (Only submit to Extract & Safelist service)
submission_params = { 
    'classification' : 'TLP:W',     # classification
    'description' : 'Hello world',  # file description
    'deep_scan' : False,            # activate deep scan mode
    'priority' : 1000,              # queue priority (the higher the number, the higher the priority)
    'ignore_cache' : False,         # ignore system cache
    'services' : {
        'selected' : [ # selected service list (override user profile)
            'Extract',
            'Safelist'
        ],
        'resubmit' : [],            # resubmit to these services if file initially scores > 500
        'excluded': [],             # exclude these services
    },
    'service_spec': {               # provide a service parameter
        'Extract': {
            'password': 'password'
        }
    }
}

# Ingest files through Ingest API with(/out) notification queues
#client.ingest --> /api/v4/ingest/
#client.ingest.get_message_list --> /api/v4/ingest/get_message_list/nq_name/
#client.search.submission --> /api/v4/search/index/
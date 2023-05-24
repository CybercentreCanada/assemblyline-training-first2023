# `GET /api/v4/file/download/<sha256>/`
Python:

`Client.file.download(sha256, encoding=None, sid=None, output=None, password=None)`

Response: \<binary-data>

# `POST /api/v4/ingest/`
Python:

`Client.ingest(fh=None, path=None, content=None, url=None, sha256=None, fname=None, params=None, metadata=None, alert=False, nq=None, nt=None, ingest_type='AL_CLIENT')`

Response:
```
{ "ingest_id": <ID OF THE INGESTED FILE> }
```
# `GET /api/v4/ingest/get_message/<notification_queue>/`
Python:

`Client.ingest.get_message(nq)`

Example Response:
```
{'extended_scan': 'skipped',
 'failure': '',
 'ingest_id': '3SKGKc1NVO8HBkqMT4TpWV',
 'ingest_time': '2023-05-24T16:07:41.884092Z',
 'retries': 0,
 'score': 0,
 'submission': {'files': [{
    'name': 'www.google.ca',
    'sha256': '2f13d3007853599ac19e808c7a9453703184152da746ba8b0e3933a563fa93dc',
    'size': 145819}],
  'metadata': {'ingest_id': '3SKGKc1NVO8HBkqMT4TpWV',
   'submitted_url': 'https://www.google.ca',
   'ts': '2023-05-24T16:07:41.877723Z',
   'type': 'INGEST'},
  'notification': {'queue': 'test', 'threshold': None},
  'params': {'auto_archive': False,
   'classification': 'TLP:CLEAR',
   'deep_scan': False,
   'delete_after_archive': False,
   'description': '[INGEST] Inspection of URL: https://www.google.ca',
   'generate_alert': False,
   'groups': ['USERS'],
   'ignore_cache': True,
   'ignore_dynamic_recursion_prevention': False,
   'ignore_filtering': False,
   'ignore_size': False,
   'initial_data': None,
   'malicious': False,
   'max_extracted': 100,
   'max_supplementary': 100,
   'never_drop': False,
   'priority': 150,
   'profile': False,
   'psid': None,
   'quota_item': False,
   'service_spec': {'URLDownloader': {'include_submitted_url': True}},
   'services': {'excluded': [],
    'rescan': [],
    'resubmit': [],
    'runtime_excluded': [],
    'selected': ['Ancestry', 'URLDownloader']},
   'submitter': 'user',
   'ttl': 30,
   'type': 'INGEST'},
  'scan_key': '3354668ac080fec81c23f241ee2b5dd8v0',
  'sid': '2gfYPTznkoWWmYTZHxuljl',
  'time': '2023-05-24T16:07:41.877807Z'}}
```
# `GET /api/v4/ingest/get_message_list/<notification_queue>/`
Python:

`Client.ingest.get_message_list(nq)`

Response: <List of messages>
# `GET /api/v4/ontology/<sid>/`
Python:

`Client.ontology.submission(sid, sha256s=[], services=[], output=None)`

Response: List of [ontologies](https://cybercentrecanada.github.io/assemblyline4_docs/odm/models/ontology/ontology/)
# `GET /api/v4/search/<index>/`
Python:

`Client.search.<index>(query, filters=None, fl=None, offset=0, rows=25, sort=None, timeout=None, use_archive=False, track_total_hits=None)`

Response:
```
{
    "total": 201,                          # Total results found
    "offset": 0,                           # Offset in the result list
    "rows": 100,                           # Number of results returned
    "next_deep_paging_id": "asX3f...342",  # ID to pass back for the next page during deep paging
    "items": []                            # List of results
}
```
# `GET /api/v4/submission/full/<sid>/​`
Python:

`Client.submission.full(sid)`

Response:
```
{"classification": "UNRESTRICTED"  # Access control for the submission
    "error_count": 0,                  # Number of errors in this submission
    "errors": [],                      # List of error blocks (see Get Service Error)
    "file_count": 4,                   # Number of files in this submission
    "files": [                         # List of submitted files
    ["FNAME", "sha256"], ...],              # Each file = List of name/sha256
    "file_infos": {                    # Dictionary of fil info blocks
    "234...235": <<FILE_INFO>>,          # File in block
    ...},                                # Keyed by file's sha256
    "file_tree": {                     # File tree of the submission
    "333...7a3": {                       # File tree item
    "children": {},                         # Recursive children of file tree item
    "name": ["file.exe",...]                # List of possible names for the file
    "score": 0                              # Score of the file
    },, ...},                            # Keyed by file's sha256
    "missing_error_keys": [],          # Errors that could not be fetched from the datastore
    "missing_result_keys": [],         # Results that could not be fetched from the datastore
    "results": [],                     # List of Results Blocks (see Get Service Result)
    "services": {                      # Service Block
    "selected": ["mcafee"],              # List of selected services
    "params": {},                        # Service specific parameters
    "excluded": []                       # List of excluded services
    },
    "state": "completed",              # State of the submission
    "submission": {                    # Submission Block
    "profile": true,                     # Should keep stats about execution?
    "description": "",                   # Submission description
    "ttl": 30,                           # Submission days to live
    "ignore_filtering": false,           # Ignore filtering services?
    "priority": 1000,                    # Submission priority, higher = faster
    "ignore_cache": true,                # Force reprocess even is result exist?
    "groups": ["group", ...],            # List of groups with access
    "sid": "ab9...956",                  # Submission ID
    "submitter": "user",                 # Uname of the submitter
    "max_score": 1422, },                # Score of highest scoring file
    "times": {                         # Timing block
    "completed": "2014-...",             # Completed time
    "submitted": "2014-..."              # Submitted time
    }
}
```
# `GET /api/v4/submission/summary/<sid>/`
Python:

`Client.submission.summary(sid)`

Response:
```
{"map": {                # Map of TAGS to sha256
    "TYPE__VAL": [          # Type and value of the tags
        "sha256"                   # List of related sha256s
        ...],
    "sha256": [                # sha256
        "TYPE__VAL"             # List of related type/value
        ...], ... }
    "tags": {               # Dictionary of tags
    "attribution": {        # attribution tags
        "TYPE": [               # Type of tag
        "VALUE",                # Value of the tag
        ...
        ],...
        }, ...
    ),
    "behavior": {},         # behavior tags
    "ioc"" {}               # IOC tags
    },
    "attack_matrix": {      # Attack matrix dictionary
    "CATEGORY": [           # List of Attack pattern for a given category
        ("ATTACK_ID",          # Attack ID
        "PATTERN_NAME")       # Name of the Attack Pattern
    ... ],
    ...
    },
    "heuristics": {         # Heuristics dictionary
    "info": [               # Heuritics maliciousness level
        ("HEUR_ID",            # Heuristic ID
        "Heuristic name")     # Name of the heuristic
    ... ],
    ...
    }
}
```
# `GET /api/v4/submission/<sid>/file/<sha256>/​`
Python:

`Client.submission.get_file_submission_results(sid, sha256)`

Response:
```
{
    "errors": [],    # List of error blocks
    "file_info": {}, # File information block (md5, ...)
    "results": [],   # List of result blocks
    "tags": []       # List of generated tags
}
```

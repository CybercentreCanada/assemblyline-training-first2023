# Exercise #2: Performing Filtered File Collection

# Download file(s) with a certain score

# Filter for submissions that exceed a certain score
SUBMISSION_MAX_SCORE_MINIMUM = 1000
# Filter for files within a submission that exceed a certain score
FILE_SCORE_THRESHOLD = 500
# Download files that meet the FILE_SCORE_THRESHOLD into this directory
OUTPUT_DIRECTORY = '/tmp/'

# Grab a submission with certain overall max score
# client.search.submission --> /api/v4/search/index/

# Get the SHA256 of every file associated to the submission
# client.submission.full --> /api/v4/submission/full/sid/
# client.submission.file --> /api/v4/submission/sid/file/sha256/

# If file score is greater than threshold, download in cARTed format
# client.file.download --> /api/v4/file/download/sha256?encoding=cart/

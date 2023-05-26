$DOMAIN_STG = "malware-stg.cyber.gc.ca"
$USERNAME = "moguilb-cyber"
$KEY_STG = 'Automation:q^jz2cmiuQg3sL^He3B$K35S0iUmyN!Lmu2o5m0dUOoqgt58'
$submit_path = "https://" + $DOMAIN_STG + "/api/v4/submit"
$ingest_path = "https://" + $DOMAIN_STG + "/api/v4/ingest"

$header = @{
    'x-user' = $USERNAME
    'x-apikey' = $KEY_STG
    'accept' ='application/json'
}
$File = 'myfile.txt'
$body = @{
    "json"="{'params': {'description': 'My CURL test'}, 'metadata': {'any_key': 'any_value'}}"
    f = Get-Item -Path $File
   } | ConvertTo-Json

$result_submit = Invoke-WebRequest -Uri $submit_path -Method POST -Body $body -Headers $header


#$result_ingest = Invoke-WebRequest -Uri $ingest_path -Method POST -Body $body -Headers $header
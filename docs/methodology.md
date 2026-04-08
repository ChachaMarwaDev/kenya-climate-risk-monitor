How to calculate the standard precipitation index (SPI) for a given station and time period?

    SPI = (P-P*) /  σp
    where P = precipitation
    p* = mean precipitation
    σp = standard deviation of precipitation
    
    | SPI Values | Category |
    |------------|----------|
    | ≥ 2.00 | Extremely Wet |
    | 1.50 to 1.99 | Severely Wet |
    | 1.00 to 1.49 | Moderately Wet |
    | -0.99 to 0.99 | Near Normal |
    | -1.00 to -1.49 | Moderately Dry |
    | -1.50 to -1.99 | Severely Dry |
    | ≤ -2.00 | Extremely Dry |


Verifying google cloud with dlt
0. run `gcloud auth application-default login`
1. pip install "dlt[gs]" - install dlt with GCS support
2. set our environment variables since I was on windows
    ```powershell
    $env:GCS_BUCKET_NAME = "your-actual-bucket-name"
    $env:GCS_PROJECT_ID  = "your-actual-project-id"```
3. Verify the ADC is visible to python
    `python -c "import google.auth; creds, project = google.auth.default(); print('Project:', project)"`
4. If it prints the project Id, ADC is working. If errors run `gcloud auth application-default login`

Kestra admin user
1. Email - admin@kestra.io
2. Paswword - TopSecret42

Always before building the image
`gcloud auth application-default login`
Since I used ADC use this to get OAuth fields
```powershell
Get-Content "$env:APPDATA\gcloud\application_default_credentials.json" | ConvertFrom-Json | Select-Object client_id, client_secret, refresh_token | Out-File -FilePath "$env:TEMP\gcloud_output.txt"; Notepad "$env:TEMP\gcloud_output.txt"```
Get the client_id, client_secret, new refresh token
Update the extraction/.dlt/secrets.toml with the above details
Then can you build the docker File
`docker build -t kenya-pipeline:latest .`
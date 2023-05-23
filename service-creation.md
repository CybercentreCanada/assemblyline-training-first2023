# Goal
The goal is to make a module querying MalwareBazaar (https://bazaar.abuse.ch/browse/) for information, specifically the MalwareBazaar signature and comments. This will showcase the various available tools for module writers in Assemblyline, for example:
* ResultSections
* Tags
* Heuristics
* Service configuration
* File management
* Debugging
* Productionalization

An instance of the dev Assemblyline is going to be required and can be started with the following, after installing the development-setup.
```bash
cd ~/git/alv4/assemblyline-base/dev/depends
docker-compose -f docker-compose-minimal.yml up -d --wait
cd ../core
docker-compose up -d --wait
```

# Starting files
You will find four files in a folder named `mbinfo`.
- mbinfo.py: Class implementing ServiceBase
- service_manifest.yml: Service definition and metadata
- Dockerfile: Container creation for productionalization
- requirements.txt: Optional file for productionalization

# Execution and debugging
The easiest way and fastest way to execute your module on a file is to use run_service_once:
```bash
cd ~/git/alv4
source venv/bin/activate
cd assemblyline-training-first2023/mbinfo
python -m assemblyline_v4_service.dev.run_service_once mbinfo.MBInfo ../samples/d3d3facae5e604eded7bf28b146dff57334aa0d9691f1f32eb6f0a30f819bcb8.cart
```

A more complete way is to run it in debug mode in Visual Studio Code, but it needs the dev instance running.

# Improving the module
Change the python script to query MalwareBazaar
```python
import requests
# [...]
        data = {'query': 'get_info', 'hash': request.sha256}
        response = requests.post(
            "https://mb-api.abuse.ch/api/v1/",
            data=data,
            timeout=15,
            allow_redirects=True,
        ).json()
        self.log.info(response)
```

The signature under the data key and the data key contains the list of files asked for. The get_info query will always return a single file in the list.

Create a KeyValue ResultSection for the ["data"][0]["signature"]
```python
from assemblyline_v4_service.common.result import Result, ResultKeyValueSection
# [...]
        kv_res = ResultKeyValueSection("Family", parent=request.result)
        kv_res.set_item("Family", response["data"][0]["signature"])
```
We can run_service_once again, and see the new section in the result.json.

Create a Text ResultSection for the ["data"][0]["comment"]
```python
from assemblyline_v4_service.common.result import (
    Result,
    ResultKeyValueSection,
    ResultTextSection,
)
# [...]
        text_res = ResultTextSection("Comment")
        text_res.add_line(response["data"][0]["comment"])
        request.result.add_section(text_res)  # Instead of parent=request.result
```

Add the family as a tag on the ResultSection
```python
        kv_res.add_tag("attribution.family", response["data"][0]["signature"])
        kv_res.add_tag("network.signature.message", "ThisIsAMessage")
```

Add the full json response as a supplementary file
```python
import json
import os
# [...]
        with open(
            os.path.join(self.working_directory, "malware-bazaar.json"), "w"
        ) as f:
            f.write(json.dumps(response))

        request.add_supplementary(
            os.path.join(self.working_directory, "malware-bazaar.json"),
            "malware-bazaar.json",
            "Full content of the malware bazaar response",
        )
```

Add scoring heuristic if signature is in ["Smoke Loader", "AgentTesla", "RedLineStealer"]
```yaml
# Service heuristic blocks: List of heuristic objects that define the different heuristics used in the service
heuristics:
  - description: Known malicious signature found
    filetype: "*"
    heur_id: 1
    name: Known malicious signature found
    score: 1000
```
```python
        if response["data"][0]["signature"] in [
            "Smoke Loader",
            "AgentTesla",
            "RedLineStealer",
        ]:
            kv_res.set_heuristic(1)
```

Add service configuration to add more signatures
```yaml
config:
  bad_signatures: ["Smoke Loader", "AgentTesla", "RedLineStealer"]
```
```python
DEFAULT_BAD_SIGNATURES = ["Smoke Loader", "AgentTesla", "RedLineStealer"]
# [...]
        self.bad_signatures = self.config.get("bad_signatures", DEFAULT_BAD_SIGNATURES)
        self.log.info(f"Using bad signatures: {self.bad_signatures}")
# [...]
        if response["data"][0]["signature"] in self.bad_signatures:
            kv_res.set_heuristic(1)
```

Add service submission configuration to flag any signature as malicious
```yaml
submission_params:
  - name: flag_all_signatures
    type: bool
    default: false
    value: false
```
```python
        if (
            request.get_param("flag_all_signatures")
            or response["data"][0]["signature"] in self.bad_signatures
        ):
            kv_res.set_heuristic(1)
```

Add extracted file instead of supplementary file
```python
        request.add_extracted(
```

Now it crashes, but not on the original file. It needs a check for a successful answer from MalwareBazaar.
```python
        if response["query_status"] != "ok":
            # File wasn't found, therefore, nothing to do
            return
```

More robustness could be added to the service, like making sure there is a comment or a signature before creating the sections, but that's more on the python side than the Assemblyline side.

# Productionalization
This is where the Dockerfile and requirements.txt are needed. The requirements.txt is not mandatory, but could be useful if you third-party libraries are needed.

Assuming the use of a pipeline (github actions, azure devops, jenkins, ...), and creation of different versions of the module over time, the service manifest has to be changed to use the service tag.
```yaml
# Version of the service
version: $SERVICE_TAG
# [...]
docker_config:
  image: ${PRIVATE_REGISTRY}first/assemblyline-service-mbinfo:$SERVICE_TAG
```

The basic Dockerfile can be modified to receive both the build type and the service tag from the pipeline
```Dockerfile
# Use argument from pipeline to determine the type of build
ARG branch=stable
FROM cccs/assemblyline-v4-service-base:$branch
# [...]
# Patch version in manifest
USER root
# Use argument from pipeline to determine the tag
ARG version=4.4.0.dev1
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

# Switch to assemblyline user
USER assemblyline
```

Start scaler and updater in the assemblyline instance
```bash
cd ~/git/alv4/assemblyline-base/dev/core
docker-compose -f docker-compose-sca-upd.yml up -d --wait
```

Build a docker container and push it to the local dev registry
```bash
cd ~/git/alv4/assemblyline-training-first2023/mbinfo
docker build --build-arg branch=stable --build-arg version=4.4.0.dev0 -t 127.0.0.1:32000/first/assemblyline-service-mbinfo:4.4.0.dev0 .
docker push 127.0.0.1:32000/first/assemblyline-service-mbinfo:4.4.0.dev0
```
In a real production pipeline, the `latest` or `stable` tag, with the associated `4.4.latest` and `4.4.stable` tag should be created to help new deployements.

The service can now be added by copying the manifest into the service management of the running instance.

Sending new files is going to scale up and down the service, while pushing a new docker container is going to show up as an update in the service management page.

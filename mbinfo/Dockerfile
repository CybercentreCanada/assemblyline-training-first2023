FROM cccs/assemblyline-v4-service-base:stable

# Python path to the service class from your service directory
ENV SERVICE_PATH mbinfo.MBInfo

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --user --requirement requirements.txt && rm -rf ~/.cache/pip

# Copy Sample service code
WORKDIR /opt/al_service
COPY . .

# Switch to assemblyline user
USER assemblyline

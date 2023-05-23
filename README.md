# Pre-requisites
The setup script assumes the following:
- You are running this on a Ubuntu 20.04+ machine or VM with at least 4 cores and 8 GB of Ram.
- You are confortable with running the setup_vscode.sh script, this script will install and configure packages for ease of use.
  - **If you are uncomfortable which some of the changes that it makes, you should comment them before running the script.**

# Installation instruction
```bash
# Create your git directory
mkdir -p ~/git
# Clone repo
cd ~/git
git clone https://github.com/CybercentreCanada/assemblyline-development-setup alv4
# Run setup script
cd ~/git/alv4
./setup_vscode.sh -c
```
Once the script is done and you accepted to reboot, clone this repository in your workspace.
```bash
cd ~/git/alv4
git clone https://github.com/CybercentreCanada/assemblyline-training-first2023.git assemblyline-training-first2023
# Overwrite the default launch configuration with one specific for First 2023
cp ~/git/alv4/assemblyline-training-first2023/.vscode/launch.json ~/git/alv4/.vscode/
```
Launch VSCode, install the recommended extensions when prompted or by typing '@recommended' in the Extensions tab.
```bash
code ~/git/alv4
```

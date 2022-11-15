# Actualizar OS
sudo apt-get update
# Herramientas de monitoreo y logging
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install -Y
curl -sSO https://dl.google.com/cloudagents/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh --also-install
#Docker
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release -Y
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -Y
#Crear archivo credenciales:
mkdir service-account
gcloud storage cp gs://credencials-app-music/path_to_your_.json_credential_file service-account
#Env file:
gcloud storage cp gs://credencials-app-music/.env.cloud .

# Para script de arranque:
# run docker image:
sudo docker run --env-file .env.cloud -d --name api-rest -v $(pwd)/service-account:/credential/service-account -p 80:5000 davidzub/api-rest-music-converter:latest

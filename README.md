# Data Collection Pipeline

## CI/CD pipeline
* Set up the relevant GitHub secrets that contain the credentials required to push to the Dockerhub:
    * First secret: create a `DOCKER_HUB_USERNAME` and your Docker ID as value
    * Create a new Personal Access Token for Docker Hub.
    * Second secret: add the PAT as a second secret with the name `DOCKER_HUB_ACCESS_TOKEN`
* The workflow and its steps are defined in the `.github/workflows/main.yml`
    * The workflow runs on every push event for the main branch
    * The job is to sign in to Docker Hub, build and push a Docker image.

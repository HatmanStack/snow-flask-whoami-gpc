# Snowflake Flask App - Google Cloud Platform Deployment

This repository contains a Flask application that displays database information from a Snowflake database, deployed on Google Cloud Run.

## Enhanced Visualizations

### Homepage (/)
The homepage features a dual-layer visualization:
1. **Vega-Lite Chart**: A bar chart showing name counts from the Snowflake database
2. **Three.js Background Animation**: A dynamic background with falling data sprites representing database entries. The animation creates a sense of data flow and adds visual interest to the page.

### HardData Page (/HardData)
The HardData page has been completely overhauled with an interactive 3D visualization:
1. **Interactive 3D Cards**: Each database record is represented as a 3D card in a Three.js scene
2. **Drag Controls**: Users can click and drag cards to rearrange them in 3D space
3. **Orbit Controls**: Users can rotate and zoom the camera to explore the data from different angles

## Deployment

This application is deployed on Google Cloud Platform using:
- **Cloud Run**: Fully managed container platform
- **Cloud Build**: CI/CD platform for building and deploying containers
- **Container Registry**: Storage for Docker container images

### Prerequisites
- Google Cloud SDK
- Docker
- Python 3.9+
- Snowflake account with proper credentials

### Deployment Steps
1. Configure your GCP credentials:
   ```
   gcloud auth login
   ```

2. Set your project:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Enable required APIs:
   ```
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
   ```

4. Set up Cloud Build trigger with environment variables:
   ```
   gcloud beta builds triggers create github \
     --repo-name=snow-flask-whoami-gpc \
     --branch-pattern=main \
     --build-config=cloudbuild.yaml \
     --substitutions=_SNOWFLAKE_USERNAME=your_username,_SNOWFLAKE_PASSWORD=your_password,_SNOWFLAKE_REGION=your_region
   ```

5. Manually trigger a build:
   ```
   gcloud builds submit --config=cloudbuild.yaml .
   ```

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```
   export USERNAME=your_snowflake_username
   export PASSWORD=your_snowflake_password
   export REGION=your_snowflake_region
   ```

3. Run locally:
   ```
   python main.py
   ```

4. Or run with Docker:
   ```
   docker build -t snow-flask-whoami-gpc .
   docker run -p 8080:8080 -e PORT=8080 -e USERNAME=your_username -e PASSWORD=your_password -e REGION=your_region snow-flask-whoami-gpc
   ```

## Live Demo
The application is deployed at: https://snow-flask-whoami-gpc-k6cy6vf2la-uc.a.run.app/

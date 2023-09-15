# Who Am I : GPC

This is the GPC version of Who Am I.  It uses Google Cloud Run to build a microservice with Flask and Gunicorn that provides an API for querying information in a Snowflake Database.  The information is displayed with interactive Vega-Lite visualizations.

## Continuous Deployment

The service is built and deployed automatically using Google Cloud Build, configured in cloudbuild.yaml. Cloud Build pulls the latest code, builds the Docker container, and pushes it to Google Container Registry.

The container image is then deployed to Cloud Run using a rolling update. These builds are triggered on every code commit to the main branch, enabling continuous deployment. Additional Cloud Build triggers can be configured to rebuild on other branches or schedule recurring builds.

## Local Development

To run locally:

Replace `REGION`, `USERNAME`, `PASSWORD` with your own Snowflake credentials and match the Schema to the one provided.

```
pip install -r requirements.txt
python main.py
```

Access endpoints on http://localhost:8080

The service is now built and deployed automatically on every code change using Cloud Build and Cloud Run. This enables continuous delivery of the Who Am I microservice.
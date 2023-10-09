# Who Am I : GPC

This is the GCP version of "Who Am I." It leverages Google Cloud Run to construct a microservice using Flask and Gunicorn, offering an API for querying a Snowflake Database. In contrast, the alternate versions of "Who Am I" rely on cloud providers that do not utilize containers. The key distinction lies in Google Functions overseeing the primary Flask application, which can make managing multiple paths somewhat intricate but still [achievable](https://medium.com/google-cloud/use-multiple-paths-in-cloud-functions-python-and-flask-fc6780e560d3). The data is presented using interactive Vega-Lite visualizations.

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
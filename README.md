# Snowflake Flask App - Google Cloud Run Deployment

A containerized Flask application deployed on Google Cloud Run, featuring interactive Three.js visualizations and real-time Snowflake database connectivity with automatic scaling and global edge distribution.

## 🚀 Live Application
**URL**: https://snow-flask-whoami-gpc-357277717136.us-central1.run.app

** THIS REPO IS NO LONGER MAINTAINED **

## ✨ Features

### Interactive Visualizations
- **Homepage (`/`)**: Dual-layer visualization combining:
  - Vega-Lite bar chart showing real-time name counts from Snowflake database
  - Three.js background animation with falling data sprites creating dynamic visual data flow
- **HardData Page (`/HardData`)**: Immersive 3D data exploration:
  - Interactive 3D cards representing individual database records
  - Drag controls for spatial manipulation and rearrangement of data elements
  - Orbital camera controls for comprehensive 360° data exploration

### Technical Architecture
- **Compute**: Google Cloud Run (fully managed containerized platform)
- **Container**: Docker-based deployment with automatic scaling
- **Authentication**: RSA key-pair authentication with Snowflake
- **CI/CD**: Cloud Build with automated deployment pipeline

## 🏗️ Google Cloud Infrastructure

### Services Used
| Service | Purpose | Configuration |
|---------|---------|---------------|
| **Cloud Run** | Containerized compute | Fully managed, auto-scaling |
| **Cloud Build** | CI/CD pipeline | Automated builds and deployments |
| **Container Registry** | Image storage | Private container repository |
| **Cloud Logging** | Application logs | Centralized logging and monitoring |

## 📋 Prerequisites

- **Google Cloud SDK** (gcloud CLI) - [Installation Guide](https://cloud.google.com/sdk/docs/install)
- **Docker** (v20.10+) - [Installation Guide](https://docs.docker.com/get-docker/)
- **Python 3.11+** with pip
- **Snowflake account** with database access
- **Google Cloud Project** with billing enabled

## 🔧 Installation & Deployment

### 1. Environment Setup
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Verify configuration
gcloud config list
```

### 2. Clone and Prepare
```bash
git clone https://github.com/HatmanStack/snow-flask-whoami.git
cd snow-flask-whoami/snow-flask-whoami-gpc/
```

### 3. Configure Snowflake Authentication
```bash
# Generate RSA key pair (if not already done)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -v2 aes-256-cbc -passout pass:your-passphrase
openssl rsa -in rsa_key.p8 -passin pass:your-passphrase -pubout -out rsa_key.pub

# Configure Snowflake user with public key
# In Snowflake SQL worksheet:
# ALTER USER your_service_user SET RSA_PUBLIC_KEY = '<public_key_content>';
```

### 4. Enable Required APIs
```bash
# Enable necessary Google Cloud APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  containerregistry.googleapis.com \
  logging.googleapis.com
```

### 5. Manual Deployment
```bash
# Build and deploy using Cloud Build
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_LOCATION=your_gpc_artifact_registry_location,_SNOWFLAKE_USERNAME=your_username,_SNOWFLAKE_PASSWORD=your_rsa_private_key_passphrase,_SNOWFLAKE_ACCOUNT=your_account
```

### 6. Automated CI/CD Setup
```bash
# Create Cloud Build trigger for automated deployments
gcloud beta builds triggers create github \
  --repo-name=snow-flask-whoami-gpc \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern=main \
  --build-config=cloudbuild.yaml \
  --substitutions=_SNOWFLAKE_USERNAME=your_username,_SNOWFLAKE_PASSWORD=your_rsa_private_key_passphrase_SNOWFLAKE_ACCOUNT=your_account
```

## 💻 Local Development

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
```bash
export SNOW_USERNAME=your_snowflake_username
export SNOW_PASSWORD=your_rsa_private_key_passphrase
export SNOW_ACCOUNT=your_snowflake_account
export PORT=8080
```

### Local Testing Options

#### Option 1: Python Flask Server
```bash
python main.py
# Access at http://localhost:8080
```

#### Option 2: Docker Container
```bash
# Build container
docker build -t snow-flask-whoami-gcp .

# Run container
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e SNOW_USERNAME=your_username \
  -e SNOW_PASSWORD=your_rsa_secure_passphrase \
  -e SNOW_ACCOUNT=your_account \
  snow-flask-whoami-gcp
```

#### Option 3: Cloud Run Emulator
```bash
# Install pack CLI (if not installed)
curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.27.0/pack-v0.27.0-linux.tgz" | sudo tar -C /usr/local/bin/ --no-same-owner -xzv pack

# Build with Cloud Native Buildpacks
pack build snow-flask-whoami-gcp --builder gcr.io/buildpacks/builder:v1

# Run locally
docker run -p 8080:8080 snow-flask-whoami-gcp
```

## 📊 Monitoring & Troubleshooting

### Cloud Logging
```bash
# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=snow-flask-whoami-gpc" --limit 50

# Stream live logs
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=snow-flask-whoami-gpc"
```

### Cloud Run Metrics
```bash
# Get service details
gcloud run services describe snow-flask-whoami-gpc --region=us-central1

# List revisions
gcloud run revisions list --service=snow-flask-whoami-gpc --region=us-central1
```

### Common Issues
- **Cold Start Latency**: First request may take 2-3 seconds
- **Memory Limits**: Default 1GB, increase if needed
- **Request Timeout**: 15-minute maximum for Cloud Run
- **Concurrency**: Default 100 concurrent requests per instance

## 🗂️ Project Structure
```
snow-flask-whoami-gpc/
├── main.py                # Flask application entry point
├── Dockerfile             # Container configuration
├── cloudbuild.yaml        # Cloud Build configuration
├── requirements.txt       # Python dependencies
├── rsa_key.p8            # Snowflake private key
├── static/               # Frontend assets
│   ├── cards.js         # 3D card interactions
│   └── threejs-background.js # Background animations
└── templates/            # Jinja2 HTML templates
    ├── index.html       # Homepage with charts
    ├── charts.html      # Data visualization page
    ├── submit.html      # Data entry form
    └── thanks4submit.html # Confirmation page
```

## 🔐 Security Considerations

- **Snowflake Credentials**: Passed as build-time environment variables
- **RSA Keys**: Private key encrypted with passphrase
- **HTTPS**: Enforced by default on Cloud Run
- **IAM**: Use least-privilege service accounts
- **VPC**: Consider VPC Connector for private resources

## 🌍 Global Deployment

### Multi-Region Setup
```bash
# Deploy to multiple regions
REGIONS=("us-central1" "europe-west1" "asia-northeast1")

for region in "${REGIONS[@]}"; do
  gcloud run deploy snow-flask-whoami-gpc-${region} \
    --image gcr.io/YOUR_PROJECT_ID/snow-flask-whoami-gpc \
    --region ${region} \
    --platform managed \
    --allow-unauthenticated
done
```

### Load Balancer Configuration
```bash
# Create global load balancer
gcloud compute backend-services create snow-flask-backend \
  --global \
  --load-balancing-scheme=EXTERNAL \
  --protocol=HTTP

# Add Cloud Run backends
gcloud compute backend-services add-backend snow-flask-backend \
  --global \
  --network-endpoint-group=snow-flask-neg \
  --network-endpoint-group-region=us-central1
```

## 💰 Cost Optimization

- **Pay-per-request**: Only charged for actual requests
- **CPU Allocation**: Choose appropriate CPU allocation
- **Memory Optimization**: Right-size memory allocation
- **Request Timeout**: Optimize for faster responses
- **Free Tier**: 2M requests free monthly
- **Estimated Monthly Cost**: <$20 for moderate usage

## 🔄 Advanced CI/CD

### Cloud Build Configuration (`cloudbuild.yaml`)
```yaml
steps:
  # Build container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/snow-flask-whoami-gpc', '.']
  
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/snow-flask-whoami-gpc']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
    - 'run'
    - 'deploy'
    - 'snow-flask-whoami-gpc'
    - '--image'
    - 'gcr.io/$PROJECT_ID/snow-flask-whoami-gpc'
    - '--region'
    - 'us-central1'
    - '--platform'
    - 'managed'
    - '--allow-unauthenticated'
    - '--set-env-vars=SNOW_USERNAME=${_SNOWFLAKE_USERNAME},SNOW_PASSWORD=${_SNOWFLAKE_PASSWORD},SNOW_ACCOUNT=${_SNOWFLAKE_ACCOUNT}'

images:
- 'gcr.io/$PROJECT_ID/snow-flask-whoami-gpc'
```

## 🔧 Performance Optimization

### Container Optimization
- **Multi-stage Dockerfile**: Minimize image size
- **Python Optimization**: Use slim base images
- **Dependency Caching**: Leverage Docker layer caching
- **Startup Time**: Minimize cold start latency

### Scaling Configuration
```bash
# Configure scaling parameters
gcloud run services update snow-flask-whoami-gpc \
  --region=us-central1 \
  --cpu=1 \
  --memory=2Gi \
  --concurrency=100 \
  --max-instances=1000 \
  --min-instances=1
```

### Notes
If you have a .gcloudignore file in your repository, it is used exclusively.  If you do not have a .gcloudignore file, gcloud will use your .gitignore file instead. It is extremely common for .gitignore files to contain entries like *.p8, *.pem, or *.keys to prevent developers from accidentally committing private keys to source control. 

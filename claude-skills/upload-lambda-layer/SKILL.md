# Upload Lambda Layer Skill

Upload a zip file as an AWS Lambda layer, configured for Python 3.12-3.14 on ARM64 architecture.

## Setup

1. Install boto3:
   ```bash
   pip install boto3
   ```

2. Configure AWS credentials (one of):
   - AWS CLI: `aws configure`
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - AWS credentials file: `~/.aws/credentials`

3. Ensure you have permissions for `lambda:PublishLayerVersion`

## Usage

```bash
# Upload with defaults (us-east-1 region)
python upload_layer.py my-layer.zip --layer-name my-layer-name

# Specify custom region
python upload_layer.py my-layer.zip --layer-name my-layer --region ap-southeast-1

# With description
python upload_layer.py layer.zip --layer-name my-layer --description "My custom Lambda layer"
```

## Arguments

- `zip_file` — Path to the zip file (required)
- `--layer-name, -n` — Name for the Lambda layer (required)
- `--region, -r` — AWS region (default: us-east-1)
- `--description, -d` — Optional description for the layer

## Output

Returns the Lambda layer ARN, version, and version ARN on success.

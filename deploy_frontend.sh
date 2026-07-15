#!/bin/bash
set -e

# 1. Fetch the AWS Account ID to create a globally unique bucket name
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="finstream-dashboard-rahwa"
REGION="us-east-1" # Default region matching samconfig.toml

echo "🚀 Deploying FinStream Frontend to AWS S3..."
echo "📦 Bucket Name: $BUCKET_NAME"
echo "📍 Region: $REGION"

# 2. Check if the S3 bucket already exists
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "✅ S3 Bucket already exists."
else
    echo "🆕 Creating S3 Bucket..."
    # If region is us-east-1, LocationConstraint is not specified
    if [ "$REGION" = "us-east-1" ]; then
        aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION"
    else
        aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION" --create-bucket-configuration LocationConstraint="$REGION"
    fi
    echo "✅ S3 Bucket created successfully."
fi

# 3. Disable S3 Public Access Block (required to host static websites)
echo "🔒 Updating Public Access Block settings..."
aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# 4. Attach Bucket Policy for Public Read Access
echo "📄 Applying Public Read Bucket Policy..."
POLICY_JSON=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
EOF
)

aws s3api put-bucket-policy --bucket "$BUCKET_NAME" --policy "$POLICY_JSON"

# 5. Enable Static Website Hosting on the S3 Bucket
echo "🌐 Enabling Static Website Hosting..."
aws s3api put-bucket-website --bucket "$BUCKET_NAME" --website-configuration '{
    "IndexDocument": {
        "Suffix": "index.html"
    },
    "ErrorDocument": {
        "Key": "index.html"
    }
}'

# 6. Build the Frontend React Application
echo "🏗 Building the React Frontend..."
cd frontend
npm run build
cd ..

# 7. Upload the compiled files to S3
echo "📤 Uploading files to S3..."
aws s3 sync frontend/dist/ "s3://$BUCKET_NAME/" --delete

# 8. Output the URL
echo "🎉 Deployment Complete!"
echo "🔗 Your dashboard is live at: http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com"

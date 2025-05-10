# Check if the invited Datadog User is pending

## Decription

Show pending invited users using Lambda Function.

## File structure

```tree
.
├── README.md
├── template.yaml            # SAM template
├── layer                    # Lambda Layer for third‑party libs
│   └── requirements.txt     # pip dependencies
└── src
    └── app.py               # Lambda handler (Python 3.13)
```

## Preparation

First, SAM Install setup.  
https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html

## Create Secrets

Create your secrets in seactrets manager as follow.

- Secret name: ddOrgSecret
- Secret paramator:
  - You need rewrite YOUR_ORGANIZATION, apiKey, appKey

```json
{
    "orgs": {
        "YOUR_ORGANIZATION": {
            "keys": {
                "apiKey": "123456789",
                "appKey": "abcdefg"
            }
        }
    },
    "orgs": {
        "YOUR_ORGANIZATION": {
            "keys": {
                "apiKey": "123456789",
                "appKey": "abcdefg"
            }
        }
    }
}    
```

## Deploy

**Caution:** Deploy to your specified AWS CLI profile destination.

```bash
$ export AWS_PROFILE=YOUR_AWS_PROFILE_NAME
$ sam build
$ sam deploy \
  --stack-name dd-user-invite-pending \
  --s3-bucket YOUR_SAM_S3_BUCKET_NAME \
  --s3-prefix dd-user-invite-pending \
  --region ap-northeast-1 \
  --profile YOUR_AWS_PROFILE \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    ProjectName="dd-user-invite-pending"
```

**Example**

```bash
$ export AWS_PROFILE=YOUR_AWS_PROFILE_NAME
$ sam build
$ sam deploy \
  --stack-name dd-user-invite-pending \
  --s3-bucket aws-sam-cli-managed-default-0123456789 \
  --s3-prefix dd-user-invite-pending \
  --region ap-northeast-1 \
  --profile myprofile \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    ProjectName="dd-user-invite-pending"
```

**Notice:**

The necessary code is deployed under S3 bucket: aws-sam-cli-managed-default-0123456789.

## How to run

- Go to the TEST tab and execute the TEST button

### Result
  
- No Invited Users

```txt
Invite Pending Users
=== YOUR_DATADOG_ORGANIZATION ===
招待保留ユーザはありません
```

- Found Invited Users

```txt
Invite Pending Users
=== YOUR_DATADOG_ORGANIZATION ===
test@example.com
```

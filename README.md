# Geocode serverless application.

This is a serverless application built using Python3, AWS Lambda, and AWS DynamoDB.

The proposal is having lambda endpoints that create users, create reverse geocoding logs using Google APIs, get users
information, and get geolocation stores data.

# Setup

The first step is set up the AWS credentials as environment variables.

```
export AWS_ACCESS_KEY_ID=access-key
export AWS_SECRET_ACCESS_KEY=secret-key
export AWS_DEFAULT_REGION=us-east-1
```

###### Note: You should to create the env variable GOOGLE_GEOCODING_API_KEY in aws Lambda function.
###### Or, add the correct API key value in serverless.yml file.

### Python dependencies:

> virtualenv venv -p python3
>
> source venv/bin/activate

### Node dependencies

> pip install -r requirements.txt
>
> npm init
>
> npm install

### Serverless framework CLI

(https://www.serverless.com/framework/docs/getting-started/)

> npm install -g serverless

## Run project locally:

> sls wsgi serve

# Endpoints

### Create a user

```
[POST] /users

Create a user

{
  "name": "Andres Duque",
  "userId": "saduqz"
}

# response:
{
  "name": "Andres Duque",
  "userId": "saduqz"
}
```

### Get user information (users data and previously geocoding created).

```
[POST] /users/{user-id}

Get a user

# response
{
    "geodata": [
        {
            "address": "address used in the request",
            "created": "2021-06-06T00:32:24.292722",
            "id": "UUID",
            "latitude": "latitude",
            "longitude": "longitude",
            "maps_link": "google maps link",
            "metadata": "metadata-information",
            "user_id": "saduqz"
        },
        ...
    ],
    "name": "Andres Duque",
    "userId": "saduqz"
}
```

### Create reverse geocode from address string. e.g. "medellin"

```
[POST] /geocode/{user-id}
{
  "address": "Bogota",
  "zoom": "13z"  # This is the zoom used in google maps website. "10.5z" is the default value.
}

# response
{
    'maps_link': "google maps link",
    'latitude': "latitude",
    'longitude': longitude,
}
```

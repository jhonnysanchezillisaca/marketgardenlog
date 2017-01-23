MarketGardenLog
------------------

## Overview
MarketGardenLog is a Python web application developed with Flask, to keep a registry of a garden, allowing to create different types of plants and gardens, and filter the gardens and plants by its type.

The application implements a third-party authentication & authorization service, in this case G+ and Facebook OAuth services.

## Installation

The repository contains the virtual machine configuration to use with Vagrant in the `/vagrant` directory.

Once started and logged in the vagrant machine, go to `/vagrant/marketgardenlog/` directory.

#### 1. Create the database
To create de DB schema you need to execute ` $ python database_setup.py `

#### 2. Authentication services secrets
For the authentication system to work you need to create a Client ID and Secret and save it in a json file.

##### 2.1 Google credentials
To obtain the Client ID and Secret you have to:

1. Go to https://console.developers.google.com/apis.
2. In the section Credentials you need to create an OAuth Client ID.
3. When you're presented with a list of application types, choose Web application.
4. In the configuration page add http://localhost:5000 in the "Authorised JavaScript origins" section and http://localhost:5000/login and http://localhost:5000/gconnect in the "Authorised redirect URIs" section.
5. Download the json file with the configuration clicking in the "Download JSON button" and save it as `client_secrets.json` in the `marketgardenlog/` directory.
6. In the `login.html` file , in the signin button replace the GOOGLE_CLIENT_ID_HERE with your client id.

##### 2.2 Facebook credentials
1. Register a new application in the [Facebook Developers Page](https://developers.facebook.com/).
2. In the app page click in "+ Add Product", and add Facebook Login.
3. In the configuration of the product, in "Valid OAuth redirect URIs" add http://localhost:5000.
4. From the dashboard of the app copy the Client ID and the Secret in a new json file called `fb_client_secrets.json` using the following format:
        {
        "web": {
        "app_id": "PASTE_YOUR_APP_ID_HERE",
        "app_secret": "PASTE_YOUR_CLIENT_SECRET_HERE"
            }
        }
5. In the `login.html` file , in the Facebook login section replace the FACEBOOK_APP_ID_HERE with your app id.

#### 3. Run the application
To run the application type ` $ python marketgardenlog.py `. Now the server is running and listening in port 5000.

#### 4. Access the web page
You can view the web page in your browser going to `http://localhost:5000`

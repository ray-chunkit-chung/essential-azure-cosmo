# essential-azure-cosmos

essential-azure-cosmos

<https://learn.microsoft.com/en-us/azure/cosmos-db/introduction>

<https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/quickstart-python?tabs=azure-cli%2Cvenv-windows%2Clinux>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/tutorial-query>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-dotnet-v3>

using dockerhub desktop container dev env with vscode

## Step 1 Create a cosmos resource

We need a function app to publish the function
<https://learn.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-create-serverless>

Install azure cli

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Set app variables by saving in .env file

```bash
export SUBSCRIPTION="xxx"
export TENANT="xxx"
export LOCATION="eastus"
export RESOURCE_GROUP="xxx"
export STORAGE_ACCOUNT="xxx"
export SKU_STORAGE="Standard_LRS"
export FUNCTION_APP="xxx"
export FUNCTION_VERSION="4"
export PYTHON_VERSION="3.9"
```

Set subscription

```bash
source .env
az login --tenant $TENANT
az account set -s $SUBSCRIPTION
```

Create resource group, storage account, and functionapp service plan

```bash
source .env
az group create --name $RESOURCE_GROUP \
                --location $LOCATION
az cosmosdb create \
    --resource-group $RESOURCE_GROUP \
    --name $COSMOS_NAME \
    --locations regionName=$LOCATION \
    --kind MongoDB
```

## Step 2 example python app to talk to comsos

Get cosmos connection string and nosql endpoints

```bash
export COSMOS_CONNECTION_STRING="$(az cosmosdb keys list \
        --type connection-strings \
        --resource-group $RESOURCE_GROUP \
        --name $COSMOS_NAME \
    | jq '.connectionStrings[0].connectionString' \
    | tr -d '"')"
export NOSQL_ENDPOINT="$(az cosmosdb show \
        --resource-group $RESOURCE_GROUP \
        --name $COSMOS_NAME \
        --query "documentEndpoint" \
    | tr -d '"')"
```

Install python

```bash
sudo apt-get install -y python3 python3-dev python3-venv
# sudo ln -sf /usr/bin/python3 /usr/bin/python
# export PYTHONPATH=/usr/bin/python
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# sudo python get-pip.py

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Initiate collection
```bash
python src/initiate_collection.py
```


## Step 3 SQL Query

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-dotnet-v3>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-dotnet?tabs=azure-portal%2Clinux%2Cpasswordless%2Csign-in-azure-cli>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/tutorial-dotnet-web-app>

```sql
SELECT * 
FROM Families f 
WHERE f.id = "WakefieldFamily"
```

## Finally Delete resources

After experiment, delete all resources to avoid charging a lot of money

```bash
source .env
az group delete -y --name $RESOURCE_GROUP
```

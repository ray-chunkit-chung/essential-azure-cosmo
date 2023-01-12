# essential-azure-cosmos

essential-azure-cosmos

<https://learn.microsoft.com/en-us/azure/cosmos-db/introduction>

<https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/quickstart-python?tabs=azure-cli%2Cvenv-windows%2Clinux>

<https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/tutorial-query>

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
# az storage account create --name $STORAGE_ACCOUNT \
#                           --location $LOCATION \
#                           --resource-group $RESOURCE_GROUP \
#                           --sku $SKU_STORAGE
az cosmosdb create \
    --resource-group $RESOURCE_GROUP \
    --name $COSMOS_NAME \
    --locations regionName=$LOCATION \
    --kind MongoDB
```

## Step 8 Publish function to function app

Set function.json authLevel as anonymous to allow public visit

```json
"authLevel": "anonymous",
```

Publish function to app

```bash
func azure functionapp fetch-app-settings $FUNCTION_APP
func azure storage fetch-connection-string $STORAGE_ACCOUNT
func azure functionapp publish $FUNCTION_APP
```

Test in browser <https://xxxx.azurewebsites.net/api/myhttptrigger?name=yeaeeaeaehh>

## Bonus A C# function

Many MS demo app are in C#. So we give an example here

<https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cazurecli%2Cbash>

```bash
func init MyFunctionProj
cd MyFunctionProj
func new --template "Http Trigger" --name MyHttpTrigger
```

Visit to verify <http://localhost:7071/api/myhttptrigger?name=hahahhahaa>

Set MyHttpTrigger.cs auth level as Anonymous to allow public visit

```C#
AuthorizationLevel.Anonymous
```

Publish function to app

```bash
source .env
func azure functionapp fetch-app-settings $FUNCTION_APP
func azure storage fetch-connection-string $STORAGE_ACCOUNT
func azure functionapp publish $FUNCTION_APP
```

Verify at <https://xxxx.azurewebsites.net/api/myhttptrigger?name=1212121>

**(Optional)** Also try your luck with .Net 7 x Function Core 4
<https://devblogs.microsoft.com/dotnet/dotnet-7-comes-to-azure-functions/>

<https://learn.microsoft.com/en-us/dotnet/core/install/linux-debian>

```bash
func init MyFunctionProj --worker-runtime dotnet-isolated --target-framework net7.0
cd MyFunctionProj
func new --template "HTTP trigger"
func start
```

## Step 1 Download azure function core

Download azure function core

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
```

Check distro ver

```bash
/etc/*-release files

# Ubunto
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'

# Debian
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/$(lsb_release -rs | cut -d'.' -f 1)/prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
```

```bash
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4
```

## Step 4 Install .net sdk

```bash
wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-7.0
sudo apt-get install -y dotnet-sdk-6.0
sudo apt-get install -y dotnet-sdk-3.1
```

## Step 5 Init/Start function (Python)

```bash
mkdir EventGridTriggerMigrateData
func init EventGridTriggerMigrateData
```

choose python (or other languages)

**(Optional)** One can connect to existing storage account/function

```bash
# Download all settings from an existing function app:
func azure functionapp fetch-app-settings <FunctionAppName>

# Get the Connection string for a specific storage account:
func azure storage fetch-connection-string xxxxxx
```

**(Optional)** Install python & pip

```bash
# Install python
sudo apt-get install python3 python3-dev
sudo ln -sf /usr/bin/python3 /usr/bin/python
export PYTHONPATH=/usr/bin/python
python --version

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
```

Create a new example function

```bash
func new --template "Http Trigger" --name MyHttpTrigger
func start
```

Check in browser <http://localhost:7071/api/MyHttpTrigger?name=Azure%20Rocks>

## Step 6 Setup unit test (Python)

Coming soon...

## Finally Delete resources

After experiment, delete all resources to avoid charging a lot of money

```bash
source .env
az group delete -y --name $RESOURCE_GROUP
```

# georgessl

georgessl is an extremely simple pki manager. It shouldn't be used in any production system but for managing certificates for a project that doensn't rely on the certificates it does the job well enough. With this tool you are able to:
1. Issue root CA certificates
2. Issue indermediate CA certificates using root CA certificates
3. Sign and create certificates for websites using root CA certificates or intermediate CA certificates

To set it up run the setup.py script, which automatically creates the three folders you need for this to work (root, intermediate and signed). In order for this tool to work you **must** have OpenSSL and Python 3 installed on your system so that commands such as `openssl ...` can be run from Python.

### Notice for Windows systems

For this to work with Windows systems you need to install the command line package manager `scoop` with `openssl`, either follow the guide on their website, https://scoop.sh/, or enter the commands below into Windows Powershell 5:
1. Run `Set-ExecutionPolicy RemoteSigned -scope CurrentUser`. In case it fails try to launch powershell as administrator from the start menu.
2. Run `iwr -useb get.scoop.sh | iex`, if it doesn't work try `Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')`
3. Finally run `scoop install openssl`

### For Debian based systems

In order to install Python 3 and OpenSSL on debian based systems run the following commands in your terminal:
1. `sudo add-apt-repository ppa:deadsnakes/ppa`
2. `sudo apt update`
3. `sudo apt install python3.8 -y`
4. `sudo apt install openssl -y`

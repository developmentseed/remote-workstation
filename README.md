# Geoprocessing Workstation ☁️🌎📦

This project aims to enable the deployment of a dockerised workstation that can be SSH'd into

* [Dependencies](#dependencies)
* [General usage](#general-usage)
* [With VS Code Remote SSH](#with-vs-code-remote-ssh)
* [How this all works](#how-this-all-works)
* [Customising the container image](#customising-the-container-image)
* [Make commands](#make-commands)

# Dependencies

To be able to deploy your own workstation, you will need some prerequisites installed:

* Pyenv/Python3
* Pipenv
* NVM/Node
* NPM
* aws-cdk (via `npm install`)

# General usage

## 1. Install dev dependencies

```bash
$ pipenv install -d
```

## 2. Create an SSH keypair

```bash
$ ssh-keygen -b 2048 -t rsa -f <a-path-to-save-the-file-to> -q -N ""
```

## 3. Prepare .env file

To perform some actions, this project requires a `.env` file to be present in the base of the project with some variables present. Your `.env` file should look like:

```.env
IDENTIFIER=<an example identifier for your deployment> # eg. my-dev
SSH_PRIVATE_KEY_LOCATION="<path/to/the/private/key>" # You created this in Step 3
SSH_PUBLIC_KEY="<the contents of your public key>" # You created this in Step 3
SSH_CONFIG_LOCATION="<path/to/your/ssh/config/file>" # This is optional, if not provided, a config file will be created for you
```

## 4. Deploy the instance

```bash
$ make deploy
```

## 5. SSH to your instance

```bash
$ ssh geoprocessing-workstation-<value of IDENTIFIER>
```

# With VS Code Remote SSH

VS Code has an extension called [VS Code Remote SSH - Available here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) - With this extension you can SSH onto a machine and develop on it in VS Code (locally). It also provides other utitilies such as SSH Port Forwarding.

To use the extension, install it and then make sure you've done Steps 1-4 under [General usage](#General-usage)

## 1. Find Remote SSH command

With the plugin enabled, either open the actions menu in VS Code (MacOS is `CMD + Shift + P`), or select the little icon to the bottom left, selecting `Remote-SSH: Connect to Host...`

![Remote SSH icon in VS Code](./images/remote-ssh-icon.png)

## 2. Connect to host

You should now see a prompy with the contents of your SSH Config file (listing the hosts), you should see `geoprocessing-workstation-<IDENTIFIER>` - select that.

![Remote SSH hosts](./images/remote-ssh-hosts.png)

_Note: You might not see your workstation here, this is usually the case if you A: do not have an SSH Host config file in the default location or B: didn't provide one and the deployment has generated you one in `.ssh/config` in the root of the repository._

_You can remedy this by selecting `Configure SSH Hosts...` and then `Settings` and providing the path to the non standard location_

_The setting name is `remote.SSH.configFile`, if you'd rather search for it_

## 3. Pointers

### Files
Now that you have established a connection to the instance, you can open files/folders on it like you would normally in VS Code: `File -> Open...`

### Extensions
Because VS Code Remote SSH bootstraps an VS Code server on the running instance, we can install any VS Code extension inside it, allowing us access to language support, enhanced debugging, and various other features.

### Accessing services like Jupyter
If your instance has a service like Jupyter Notebook installed, you can run this headless and then SSH Port Forward the port it's running on to localhost:

```bash
# On the instance
$ jupyter-notebook --no-browser --port=<a-port>
```

When you then look at the Remote SSH pane, you'll see `Ports` which shows you which ports have services running on them in the instance, you can then select them to forward them on

![Remote SSH Port Forwarding](./images/remote-ssh-port-forwarding.png)

Then you can access it on `localhost:<a-port>`:

![Remote SSH Port Forwarding Jupyter](./images/remote-ssh-jupyter.png)

# How this all works

This project revolves around the ability to add a SSH client to a Docker container that we then serve via [AWS Fargate](https://aws.amazon.com/fargate/)

Below is a high level diagram of what is happening architecturally:

![High level architecture](./images/remote-ssh-setup.png)

The user runs `make deploy`, under the hood this does:

1. A CDK deploy which deploys a Fargate instance. This Fargate service is based on a docker image within `docker/`. As part of this, the users public IP is added to a security group to allow SSH access to the instance. The public key the user provided is also added into the instance
2. The `utils/generate_ssh_config.py` script is called. This first identifies the public IP address of the Fargate instance, then generates an SSH config entry for the host. If a location is provided for the config file, the entry is either added or overwritten. If the location is not provided, the `.ssh/config` file is created and the entry is added
3. Finally (external to `make deploy`), the user SSH's onto the Fargate instance

# Customising the container image

## The image

To use this project, the only essential components to ensure a Docker image has are:

* An SSH server ([`openssh-server`](https://ubuntu.com/server/docs/service-openssh))
* An entrypoint script (like `docker/docker-entrypoint.sh`) that takes the public key and adds it to the authorised keys area. It should also start the SSH daemon

From then on, whatever you do with the container is up to you (Setting up users, workspaces, dependencies, etc.)

You can remove the `Dockerfile` that is currently in the `docker/` directory and add your own, just make sure it does the same setup steps

## The instance

By default, the project deploys a container with `0.25 vCPU` and `0.5GB RAM` - These can be altered in `geoprocessing_workstation/geoprocessing_workstation_stack.py` in the `ecs.FargateTaskDefinition`. You can get more information about these mappings [here](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs/FargateTaskDefinition.html#aws_cdk.aws_ecs.FargateTaskDefinition)

# Make commands

A `Makefile` is provided to abstract commonly used commands away for ease of use, a breakdown of the commands is:

```bash
$ make lint # This lints the python source with flake8, isort and black
```

```bash
$ make format # This formats the python source with isort and black
```

```bash
$ make diff # This runs a cdk diff call, letting you know what changes would be made if you were to deploy the project
```

```bash
$ make deploy # This will run a cdk deploy and generate the SSH config entry
```

```bash
$ make destroy # This will run a cdk destroy and remove all the deployed infrastructure
```

```bash
$ make ssh_config # This will generate the SSH config entry (only really useful if for some reason the Fargate instance is re-created)
```

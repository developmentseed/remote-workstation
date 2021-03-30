# Remote Workstation ☁️🌎📦 ![CI Status](https://github.com/developmentseed/remote-workstation/actions/workflows/ci.yml/badge.svg)


This project aims to enable the deployment of a dockerised workstation that can be SSH'd into

* [Dependencies](#dependencies)
* [General usage](#general-usage)
* [With VS Code Remote SSH](#with-vs-code-remote-ssh)
* [How this all works](#how-this-all-works)
* [Customising the container image](#customising-the-container-image)
* [Make commands](#make-commands)
* [References](#references)

# Dependencies

To be able to deploy your own workstation, you will need some prerequisites installed:

* Node 14 (We recommend using NVM [Node Version Manager](https://github.com/nvm-sh/nvm))
* [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) - There is a `package.json` in the repository, it's recommended to run `npm install` in the repository root and make use of `npx <command>` rather than globally installing AWS CDK
* Python 3.8.* (We recommend using [pyenv](https://github.com/pyenv/pyenv))
* [pipenv](https://github.com/pypa/pipenv)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [Docker](https://docs.docker.com/get-docker/)

If you're developing on MacOS, all of the above (apart from AWS CDK) can be installed using [homebrew](https://brew.sh/)

If you're developing on Windows, we'd recommend using either [Git BASH](https://gitforwindows.org/) or [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
# General usage

## 1. Install dependencies

If you only intend on deploying the infrastructure _as is_, you can install only the dependencies required for deployment with:

```bash
$ make install
```

However, if you intend on developing on this project and making contributions, you can install _all_ deployment and development dependencies with:

```bash
$ make install-dev
```

## 2. Create an SSH keypair

```bash
$ ssh-keygen -b 2048 -t rsa -f <a-path-to-save-the-file-to> -q -N ""
```

## 3. Prepare .env file

To perform some actions, this project requires a `.env` file to be present in the base of the project with some variables present.

An example `.env` file is provided: `example.env`, copy and rename this to `.env` and populate it with your own values.

Below is a table explaining the values we expect (and that can be used additionally) in your `.env` file:


| Variable                      	| Value(s)                                                                         	| Required 	| Default                                                             	| Description                                                                                                                                                                     	|
|-------------------------------	|----------------------------------------------------------------------------------	|----------	|---------------------------------------------------------------------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| `SSH_PRIVATE_KEY_LOCATION`    	| `<path/to/the/private/key>`                                                      	| ✅        	| N/A                                                                 	| You created this in Step 3                                                                                                                                                      	|
| `SSH_PUBLIC_KEY_LOCATION`         | `<path/to/the/public/key>`                                              	| ✅        	| N/A                                                                 	| You created this in Step 3                                                                                                                                                      	|
| `AWS_PROFILE`                 	| `<Your named AWS CLI profile>`                                                   	| 🚫        	| default                                                             	| The AWS Profile to deploy to                                                                                                                                                    	|
| `IDENTIFIER`                  	| `<An identifier for your deployment, e.g. 'my-dev'>`                             	| 🚫        	| dev                                                                 	| This is unique to your deployed stack - If a conflict occurs, your deployment will fail                                                                                                                                          	|
| `SSH_CONFIG_LOCATION`         	| `<path/to/your/ssh/config/file>`                                                 	| 🚫        	| No value will result in a .ssh/config file created in the repo root 	| The SSH Config file to add the remote workstations details to                                                                                                                   	|
| `INSTANCE_CPU`                	| `<A value of 256/512/1024/2048/4096>`                                            	| 🚫        	| 256                                                                 	| See container CPU & Memory mappings [here](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs/FargateTaskDefinition.html#aws_cdk.aws_ecs.FargateTaskDefinition)  	|
| `INSTANCE_MEMORY`             	| `<A value of 512/1024/2048/...increments of 1024 till 30720>`                    	| 🚫        	| 512                                                                 	| See container CPU & Memory mappings  [here](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs/FargateTaskDefinition.html#aws_cdk.aws_ecs.FargateTaskDefinition) 	|
| `CONTAINER_ECR_REPOSITORY`    	| `<The value of an ECR repository name, e.g. 'my-magical-repo'>`                  	| 🚫        	| N/A                                                                 	| The name of an ECR repository in the region and account you're deploying into - **Note**: See [Customising the container image](#customising-the-container-image)                                                   	|
| `CONTAINER_DOCKER_REPOSITORY` 	| `<The value of an Dockerhub/other registry repo, e.g. 'docker/whalesay:latest'>` 	| 🚫        	| N/A                                                                 	| Must be public - Credentials are currently not supported within this project - **Note** : See [Customising the container image](#customising-the-container-image)                                                   	|
| `CONTAINER_LOCAL_PATH`        	| `<path/to/your/Dockerfile/folder - not the file itself>`                          	| 🚫        	| N/A                                                                 	| The file used to build the image must be called Dockerfile - **Note** : See [Customising the container image](#customising-the-container-image)                                                                     	|
| `TAGS_<Any value>` | `<A value to assign to this tag>` | 🚫 |  N/A  | You can add as many tags as AWS allows. To add a tag, add an entry to your `.env` file like `TAGS_MY_COOL_TAG="thisiscool"` - Your AWS tag will be named with a Pascal case name like: `MyCoolTag` with the value you provided. You can read more about tags for AWS billing and tracking infrastructure [here](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)|

## 4. Deploy the instance

```bash
$ make deploy
```

## 5. SSH to your instance

```bash
$ make ssh-to-instance
```

# With VS Code Remote SSH

VS Code has an extension called [VS Code Remote SSH - Available here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) - With this extension you can SSH onto a machine and develop on it in VS Code (locally). It also provides other utitilies such as SSH Port Forwarding.

To use the extension, install it and then make sure you've done Steps 1-4 under [General usage](#General-usage)

## 1. Find Remote SSH command

With the plugin enabled, either open the actions menu in VS Code (MacOS is `CMD + Shift + P`), or select the little icon to the bottom left, selecting `Remote-SSH: Connect to Host...`

![Remote SSH icon in VS Code](./images/remote-ssh-icon.png)

## 2. Connect to host

You should now see a prompt with the contents of your SSH Config file (listing the hosts), you should see `remote-workstation-<IDENTIFIER>` - select that.

![Remote SSH hosts](./images/remote-ssh-hosts.png)

_**Note:** You might not see your workstation here, this is usually the case if you A: do not have an SSH Host config file in the default location or B: didn't provide one and the deployment has generated you one in `.ssh/config` in the root of the repository._

_You can remedy this by selecting `Configure SSH Hosts...` and then `Settings` and providing the path to the non standard location_

_The setting name is `remote.SSH.configFile`, if you'd rather search for it_

## 3. Pointers

### Files
Now that you have established a connection to the instance, you can open files/folders on it like you would normally in VS Code: `File -> Open...`

### Extensions
Because VS Code Remote SSH bootstraps an VS Code server on the running instance, we can install any VS Code extension inside it, allowing us access to language support, enhanced debugging, and various other features.

### Port Forwarding
If you're running a service that you'd like to access via `localhost` - say a webapp or a Jupyter Notebook, VS Code Remote SSH comes with SSH Port Forwarding built in.


#### Simple example

A very easy example you can peform on the `docker/Dockerfile` image is:
```bash
# On the instance
$ echo "Hello Remote Workspace!" > index.html
$ python -m http.server 8181
```

When you then look at the Remote SSH pane, you'll see `Ports` which shows you which ports have services running on them in the instance, you can then select them to forward them on

![Remote SSH Port Forwarding](./images/remote-ssh-port-forwarding.png)

Then you can access it on `localhost:<a-port>`:

![Remote SSH Port Forwarding index.html](./images/remote-ssh-index-html.png)

_**Note:** you might also notice a prompt appear in VS Code asking if you'd like to visit the forwarded application, providing you a link to click on:_

![Remote SSH Port Forwarding prompt](./images/remote-ssh-port-forwarding-prompt.png)

#### Jupyter Example

If your image has Jupyter Notebook installed (or if you run `pip3 install jupyter` on the provided `docker/Dockerfile`), you
can setup port forwarding for a notebook instance:
```bash
# On the instance
$ jupyter-notebook --no-browser --port=<a-port>
```

Similarly to the [Simple Example](#simple-example), you will see the port you provided appear in the `Ports` selection, you can then forward it, navigate to `localhost:<a-port>` and access your notebook!

![Remote SSH Port Forwarding Jupyter Notebook](./images/remote-ssh-jupyter.png)

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
* `curl`
* An entrypoint script (like `docker/docker-entrypoint.sh`) that takes the public key and adds it to the authorised keys area. It should also start the SSH daemon

From then on, whatever you do with the container is up to you (Setting up users, workspaces, dependencies, etc.)

You can remove the `Dockerfile` that is currently in the `docker/` directory and add your own, just make sure it does the same setup steps

If you have a Docker Image or a `Dockerfile` elsewhere external to this project, we use a heirarchy of values from `.env` to get which image to use, the order is from top to bottom:

* `CONTAINER_ECR_REPOSITORY` - Highest priority
* `CONTAINER_DOCKER_REPOSITORY`
* `CONTAINER_LOCAL_PATH`
* None of the above - uses `docker/` in this repository

## The instance

By default, the project deploys a container with `0.25 vCPU` and `0.5GB RAM` - These can be altered by using `INSTANCE_CPU` and `INSTANCE_MEMORY` in your `.env` file. **NOTE**: CPU and Memory are tied, you can get more information about these mappings [here](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs/FargateTaskDefinition.html#aws_cdk.aws_ecs.FargateTaskDefinition)

# Make commands

A `Makefile` is provided to abstract commonly used commands away for ease of use, a breakdown of the commands is:

**`make install`**

> This will run `npm install` and `pipenv install` on the repo root, installing only the dependencies needed for a production deployment

**`make install-dev`**

> This will run `npm install` and `pipenv install --dev` on the repo root, installing the dependencies needed for development of this project

**`make lint`**

> This will perform a dry run of `flake8`, `isort`, and `black` and let you know what issues were found

**`make format`**

> This will peform a run of `isort` and `black`, this **will** modify files if issues were found

**`make diff`**

> This will run a `cdk diff` using the contents of your `.env` file

**`make deploy`**

> This will run a `cdk deploy` using the contents of your `.env` file. The deployment is auto-approved, so **make sure** you know what you're changing with your deployment first! (Best to run `make diff` to check!)

**`make destroy`**

> This will run a `cdk destroy` using the contents of your `.env` file. The destroy is auto-approved, so **make sure** you know what you're destroying first!

**`make ssh-config`**

> This will generate the SSH config entry (only really useful if for some reason the Fargate instance is re-created)

**`make ssh-to-instance`**

> This will SSH to the instance, if the values of `SSH_CONFIG_LOCATION` and `IDENTIFIER` are not present in `.env`, the default values of `./.ssh/config` and `dev` will be used respectively

# References

* [VS Code Remote SSH](https://code.visualstudio.com/docs/remote/ssh)
* [9 Steps to SSH into an AWS Fargate managed container](https://medium.com/ci-t/9-steps-to-ssh-into-an-aws-fargate-managed-container-46c1d5f834e2)
* [How do I retrieve the public IP for a fargate task using the CLI?](https://stackoverflow.com/questions/49354116/how-do-i-retrieve-the-public-ip-for-a-fargate-task-using-the-cli)

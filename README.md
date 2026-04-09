# Fooocus API

This provides an API wrapper around [Fooocus](https://github.com/lllyasviel/Fooocus) for your convenience and for a better developer experience.

There are scripts in here to get you up and running immediately.

## Quick Start

_Note: it is recommended that you do a `git clone` so you can get updates automatically but, this is not required_

1. Download the latest copy of this project, either via `git clone ...` from the [main page](https://github.com/Proryanator/Fooocus-API) or downloading a [.zip file](https://github.com/Proryanator/Fooocus-API/archive/refs/heads/main.zip). If you downloaded the .zip, unzip the folder
2. Follow the instructions based on your operating system: [macOS](#macos) or [Windows](#windows)
3. If you didn't do it from the operating system specific instructions; Take note of the ip address shown in the output of the server, should look like:

```shell
======================================
Starting Fooocus API...
It will be accessible on your network at:
http://[your-ip-address]:8888
======================================
```
4. Open the Fooocus mobile app, tap the top right settings icon, and enter the ip address of the computer that this is running on


### macOS

If running for the first time, do the following:

1. Open a terminal
2. `cd` into the `Fooocus-API` directory
3. Run `./setup.sh`
4. Take note of the ip address shown in the output of the server, should look like:

```shell
======================================
Starting Fooocus API...
It will be accessible on your network at:
http://[your-ip-address]:8888
======================================
```
5. Open the Fooocus mobile app, tap the top right settings icon, and enter the ip address of the computer that this is running on

If you are re-running the server after doing an initial setup, you can just run `./run.sh` for a faster startup that skips all the setup.

### Windows

1. Double-click on the `setup.bat` file (that's it!). Note, if you get any errors during the install, you may need to run `setup.bat` twice (sometimes pip install hangs)
2. Take note of the ip address shown in the output of the server, should look like:

```shell
======================================
Starting Fooocus API...
It will be accessible on your network at:
http://[your-ip-address]:8888
======================================
```
3. Open the Fooocus mobile app, tap the top right settings icon, and enter the ip address of the computer that this is running on

If you are re-running the server after doing an initial setup, you can just double-click `run.bat` for a faster startup that skips all the setup.

### Fooocus API URL

To make sure the server is up and running, connect to your computer's ip address in a browser at the following. If you see a webpage load you are good to go!

`http://{your-computer-ip}:8888/docs`

### Easy Setup Script Details

The following scripts will:

- install conda if not already installed on your system (macOS under `~/home/miniconda`, and Windows at `C:\Miniconda3`)
- create a conda environment (to run the python code in)
- run a script to download the various models that Fooocus supports from the beginning so you'll be ready to go
- launch the server for you

Feel free to only run the `run.sh` or `run.bat` files after you have done an initial setup.

### Uninstall

For Windows, delete the entire `C:\Miniconda3` folder (with admin permissions) and delete this downloaded repo folder

For macOS, uninstall miniconda following online documentation and delete this repo folder.

_All models and files will be self-contained in this repo_.
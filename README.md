# Java Server Setup Using Python

This project automates the setup of a Java server (e.g., Minecraft server) using Python. It handles downloading the required Java version, configuring the server, and opening network ports for remote access.

## Features
- Automatically downloads and installs Java (JDK 11).
- Downloads and configures the server (e.g., PaperMC).
- Allows customization of memory allocation for the server.
- Opens network ports using Serveo for remote access.
- Supports both Windows and Linux platforms.

## Requirements
- Python 3.6 or higher.
- Required Python libraries:
  - `requests`
  - `json`
- SSH client (for Serveo).
- Network access to download required files.

## Installation
Clone the repository:
   ```bash
   git clone https://github.com/PunLRyS/py-java-setup
   cd py-java-setup

Run the script:
    python server.py

Follow the prompts:

Choose the version of the server you want to install.
Specify the memory allocation for the server (default is 1024M).
The script will download and configure the server automatically.
The server will start, and the port will be opened using Serveo.
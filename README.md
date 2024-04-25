# SWE Crypto Cupcakes - Python

Welcome to SWE Crypto Cupcakes, Python Edition! The feature branches in this repo represent the evolution of a sample app. Each week we can demo a new branch, look at what has changed and why:

1. `cupcakes-api`
2. `security`
3. `jwt`
4. `oauth`

The `main` branch is the same as the finished `oauth` project branch after the 4 weeks of delivery, so get started at the first branch to see the app from the very beginning.

## Setup 
- Ensure that [python 3](https://www.python.org/downloads/) is already installed on your machine. Verify with the `python3 --version` command in a terminal.
- Clone this repository.
- In a terminal, navigate into the repository and follow the [Create an Environment](https://flask.palletsprojects.com/en/2.3.x/installation/#create-an-environment) instructions depending on your OS. This will set up your virtual environment so that all dependencies are contained within your repository, and dependencies will not be installed on your host machine.
- Follow the [Activate the Environment](https://flask.palletsprojects.com/en/2.3.x/installation/#activate-the-environment) instructions depending on your OS. This will make sure that any dependency scripts being invoked will come from your virtual environment directory, and these scripts will not be invoked from the host machine. **You will need to activate this virtual environment any time you're developing in the repository, so you have access to all dependencies and scripts within the environment.**
- Once the virtual environment has been activated, install all dependencies by running `pip install -r requirements.txt`. 
- Start the Flask server by running `flask run`.
- When you are done with local development, deactivate the virtual environment by running `deactivate` in the same terminal window where you activated the virtual environment.

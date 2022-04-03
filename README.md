# Working with Brownie within SimpleStorage contract

## Table of contents

- [General info](#general-info)
- [Learned experience during the project](#learned-experience-during-the-project)
  - [Brownie vs Web3](#brownie-vs-web3)
  - [Brownie config for environment variables](#brownie-config-for-environment-variables)
  - [Deploy to the development Ganache chain](#deploy-to-the-development-ganache-chain)
  - [Explained brownie commands](#explained-brownie-commands)
    - [brownie init](#brownie-init)
    - [brownie compile](#brownie-compile)
- [Setup](#setup)
  - [Additional file for environment variables](#additional-file-for-environment-variables)
  - [Installing dependencies](#installing-dependencies)
  - [Recommended commands for use in the project](#recommended-commands-for-use-in-the-project)

## General info

The project is about making the first steps into Brownie, one of the most popular smart contract development platforms build based on Python. It's my approach to understanding basic aspects of it using the SimpleStorage contract, which I previously discussed [here](https://github.com/pawlovskiii/web3_simple_storage). I also worked with Web3.py, which gave me experience in some of the aspects that brownie does under the hood.

## Learned experience during the project

### Brownie vs Web3

- In Web3.py we needed to write our code compiler. If we wanted to interact with one of the contracts that we deployed in the past, we'd have to keep track of all those addresses and manually update our address features.
- Within Brownie, we don't need to deploy a new contract every single time. We could work with a contract that we've already deployed. It's much easier to work with a whole bunch of different chains. We can quite easily work with Rinkeby TestNet or Mainnet (fork) on our local network.
- Brownie also makes a great testing environment.

All in all, it was crucial to work with Web3.py, to experience the low-level stuff that Brownie does for us.

### Brownie config for environment variables

Brownie has an additional feature that allows us to easily work with the environment variables.

- **brownie-config.yaml** is a special file, that brownie always looks for to grab pieces of information like environmental variables, before running scripts. Later I'll explain more about the [env](#additional-file-for-environment-variables) file.

  ```yaml
  dotenv: .env
  ```

It's way better because now we have one canonical place where we're always going to pull our private key from.

```yaml
wallets:
  from_key: ${PRIVATE_KEY}
```

### Deploy to the development Ganache chain

We could either make a **transaction** or a **call**. Brownie is smart enough to know, which one is going to be done.

In this case, since we're deploying a contract and storing a number in it, we want to make a **state change**, so it's a **transaction**.

```python
def deploySimpleStorage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
```

### Explained brownie commands

These are crucial brownie commands to work with any project. I'll provide a little introduction to each one provided.

#### brownie init

To create a sample folder with everything we need with the brownie. We should only use this command once per project.

```bash
$ brownie init
```

#### brownie compile

As opposed to the web3.py. In brownie, we can compile our code without having to write our compiler. We can simply compile all the contracts that are in our **/contracts** folder within our project.

- Brownie will automatically read the version of solidity and then store all of the compiled information in **build/contracts** folder.

  Here we got **SimpleStorage.json** and there's a lot of familiar pieces

  - **ABI**
  - **opcodes** section which is the low-level language

```bash
$ brownie compile
```

```bash
$ brownie accounts list
```

```bash
$ brownie networks list
```

```bash
$ brownie console
```

```bash
$ brownie test
```

```bash
$ brownie pm list
```

### Contract testing

We need to automate our contracts to make them do what we want. We don't always want to manually check that all of our stuff is doing what we want. We can do tests in Remix IDE, but it's way better to stick with Brownie/Python. It allows more customization, control, typical CI/CD pipelines, etc.

Everything that you can do with the **brownie test** comes directly from **PyTest**. Pytest is a mature, feature-rich test framework. It lets you write small tests with minimal code, scales well for large projects, and is highly extendable.

Typically testing in **smart contracts** or testing really in anything is going to be separated into three categories:

1. **Arrange** - set up all the pieces
2. **Act** - in this case, deploy a smart contract
3. **Assert** - set up the test case

Always keep in mind that one testing function should only test one thing at a time.

Here we're checking if the contract is correctly deployed with an initial value of 0.

```python
def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected
```

## Setup

There are three different ways of working with this project and each way requires a different approach with certain things like changing public/private keys.

1. Using [Ganache](https://trufflesuite.com/ganache/index.html)
2. Using [ganache-cli](https://www.npmjs.com/package/ganache-cli)
3. Using TestNet (e.g Rinkeby)

Ganache and ganache-cli are quite similar. The difference is that in ganache-cli you're using a command-line instead of the desktop app.

### Additional file for environment variables

You must create a file named **.env** to put there your environment variables (no matter, which way above you choose).

1. Also if you prefer working with TestNet I suggest using [MetaMask](https://metamask.io/), after creating the wallet, go straight to the account and export the private key. It has to be in hexadecimal version, so we put **0x** at the beginning (only when you use TestNet, in ganache is right away, so check it carefully).

```
export PRIVATE_KEY=0x...
```

2. Firstly you need an account on [Infura](https://infura.io/). After that, you create a new project and type its ID.

```
export WEB3_INFURA_PROJECT_ID=...
```

### Installing dependencies

To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. In this case, Node.js is only needed for installing a prettier-plugin for Solidity. Furthermore, you'll have to download [Python](https://www.python.org/downloads/) 3.6+ version to install all the required packages via pip. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/pawlovskiii/brownie_simple_storage

# Go into the repository
$ cd brownie_simple_storage

# Install ganache-cli
$ npm install -g ganache-cli

# Install dependencies
$ npm install
```

Brownie installation might give you a little headache but I will give you a whole recipe to go through this process stressless. I found this [thread](https://stackoverflow.com/questions/69679343/pipx-failed-to-build-packages) very helpful.

```bash
$ pip install cython

$ pip install eth-brownie
```

### Recommended commands for use in the project

1. The crucial step in order to do any action with the contracts.

   ```bash
   $ brownie compile
   ```

2. Brownie will spin up a local ganache chain by default to deploy to. It defaults always working with a local **ganache-cli** blockchain.

   ```bash
   $ brownie run .\scripts\deploy.py
   ```

3. Brownie testing variations command.

   ```bash
   # testing all the functions
   $ brownie test

   # single function testing
   $ brownie test -k test_deploy
   ```

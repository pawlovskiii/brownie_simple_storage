from brownie import accounts, config, SimpleStorage, network


def deploySimpleStorage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploySimpleStorage()

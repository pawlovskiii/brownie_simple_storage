from brownie import SimpleStorage, accounts

def test_deploy():
    # Arrange
    account = accounts[0]
    # Act 
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account}) # since this is really just part of the setup and not the act, that we're really testing

    # Act
    expected = 15
    transaction = simple_storage.store(expected, {"from": account})
    transaction.wait(1)
    
    # Assert
    assert expected == simple_storage.retrieve()
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Initialize the Algorand client for the default local network
algorand = AlgorandClient.default_local_net()

# Generate a dispenser account with ALGOs for funding transactions
dispenser = algorand.account.dispenser()
# print(dispenser.address)  # Uncomment to print the dispenser address

# Generate a random account for the asset creator
creator = algorand.account.random()
# print(creator.address)  # Uncomment to print the creator address
# print(algorand.account.get_information(creator.address))  # Uncomment to print creator account information

# Fund the creator account with 10 million ALGOs
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)
# print(algorand.account.get_information(creator.address))  # Uncomment to print updated creator account information

# Create the asset (BUILDHER token with unit HER)
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=333,
        asset_name="BUILDHER",
        unit_name="HER"
    )
)

# Extract the asset ID from the transaction confirmation
asset_id = sent_txn["confirmation"]["asset-index"]
# print(asset_id)  # Uncomment to print the asset ID

# Generate three receiver accounts
rec_address = [algorand.account.random() for _ in range(3)]

# Fund each receiver account with 10 million ALGOs
for receiver_acct in rec_address:
    algorand.send.payment(
        PayParams(
            sender=dispenser.address,
            receiver=receiver_acct.address,
            amount=10_000_000
        )
    )

# Opt-in each receiver account to the asset to allow receiving transfers
for receiver_acct in rec_address:
    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=receiver_acct.address,
            asset_id=asset_id
        )
    )

# Transfer 111 BUILDHER tokens from the creator to each receiver
for receiver_acct in rec_address:
    asset_transfer = algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver_acct.address,
            asset_id=asset_id,
            amount=111,
            last_valid_round=100  # Set the last valid round to prevent transaction errors
        )
    )

    # Print information about the receiver account after the transfer
    print(f"Here is the account information {receiver_acct.address}:")
    print(algorand.account.get_information(receiver_acct.address) + "\n")

#!/bin/bash

ws_server="ws://127.0.0.1:9946"

# creating wallets
btcli wallet create  --no_prompt --wallet.name subnet_owner --n_words 12 --no_password --wallet.hotkey subnet_owner_hot
btcli wallet create  --no_prompt --wallet.name miner_1 --n_words 12 --no_password --wallet.hotkey miner_1_hot
btcli wallet create  --no_prompt --wallet.name validator_1 --n_words 12 --no_password --wallet.hotkey validator_1_hot

# faucet tao to wallets
# Starting with the subnet owner we will be running it four times to ensure that the wallet has enough balance to create a subnet
# we get 300TAO each time
btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt

# faucet to miner and validator wallets will be run once i.e 300TAO each
btcli wallet faucet --wallet.name miner_1 --subtensor.chain_endpoint $ws_server --no_prompt
btcli wallet faucet --wallet.name validator_1 --subtensor.chain_endpoint $ws_server --no_prompt

# creating subnet
btcli subnet create --wallet.name subnet_owner --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# register neurons to subnet
btcli subnet register --wallet.name miner_1 --wallet.hotkey miner_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --netuid 1
btcli subnet register --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --netuid 1

# staking for validator into subnet
btcli stake add --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --all

# Now we run the validator and the miner
# python neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name miner_1 --wallet.hotkey miner_1_hot --logging.debug
# python neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name validator_1 --wallet.hotkey validator_1_hot --logging.debug





# registering validator to root network to get emissions rewards
# btcli root register --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# 
# btcli root boost --netuid 1 --increase 1 --wallet.name validator_1 --wallet.hotkey validator_1_hot  --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

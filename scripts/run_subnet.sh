#!/bin/bash

ws_server="ws://127.0.0.1:9946"

# creating wallets
btcli wallet new_coldkey --wallet.name subnet_owner
btcli wallet new_coldkey --wallet.name miner_1
btcli wallet new_coldkey --wallet.name validator_1
btcli wallet new_hotkey --wallet.name miner_1 --wallet.hotkey miner-hot1
btcli wallet new_hotkey --wallet.name validator_1 --wallet.hotkey validator_1_hot

# faucet tao to wallets
btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint ws://127.0.0.1:9946 
btcli wallet faucet --wallet.name miner_1 --subtensor.chain_endpoint ws://127.0.0.1:9946 
btcli wallet faucet --wallet.name validator_1 --subtensor.chain_endpoint ws://127.0.0.1:9946 

# creating subnet
btcli subnet create --wallet.name subnet_owner --subtensor.chain_endpoint ws://127.0.0.1:9946

# register neurons to subnet
btcli subnet register --wallet.name miner_1 --wallet.hotkey miner-hot1 --subtensor.chain_endpoint ws://127.0.0.1:9946
btcli subnet register --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946

# staking for validator into subnet
btcli stake add --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946

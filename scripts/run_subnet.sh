#!/bin/bash

ws_server="ws://127.0.0.1:9946"

# Sleep for 5 seconds to allow the chain to start
sleep 5

# Regenerate keys for subnet owner, validator and miner
btcli w regen_coldkey  --wallet.name subnet_owner --no_password --no_prompt --mnemonic common during year embark silent provide reflect shield catch roast addict ride
btcli w regen_coldkey  --wallet.name validator_1 --no_password --no_prompt --mnemonic clarify carry wrestle horn width donor buddy drill tone ring true stomach
btcli w regen_coldkey --wallet.name miner_1 --no_password --no_prompt --mnemonic member act smooth october push cactus live index other wasp famous busy
btcli w regen_hotkey  --wallet.name subnet_owner --wallet.hotkey subnet_owner_hot --no_password --no_prompt --mnemonic range craft return alien unlock draw card robot topic loop fox machine
btcli w regen_hotkey  --wallet.name validator_1 --wallet.hotkey validator_1_hot --no_password --no_prompt --mnemonic  myth napkin agent spot inform acoustic front mandate space october old coyote
btcli w regen_hotkey --wallet.name miner_1 --wallet.hotkey miner_1_hot --no_password --no_prompt --mnemonic  sauce this ride soap rescue galaxy attend soul firm reunion scale forest


# faucet tao to wallets
# Starting with the subnet owner we will be running it four times to ensure that the wallet has enough balance to create a subnet
# we get 300TAO each time
# btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
# btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
# btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt
# btcli wallet faucet --wallet.name subnet_owner --subtensor.chain_endpoint $ws_server --no_prompt

# faucet to miner and validator wallets will be run once i.e 300TAO each
# btcli wallet faucet --wallet.name miner_1 --subtensor.chain_endpoint $ws_server --no_prompt
# btcli wallet faucet --wallet.name validator_1 --subtensor.chain_endpoint $ws_server --no_prompt

# creating subnet
btcli subnet create --wallet.name subnet_owner --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# register neurons to subnet
btcli subnet register --wallet.name miner_1 --wallet.hotkey miner_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --netuid 1
btcli subnet register --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --netuid 1

# staking for validator into subnet
btcli stake add --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt --all

# Now we run the validator and the miner
python neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name miner_1 --wallet.hotkey miner_1_hot --logging.debug &> miner-log.txt &
python neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name validator_1 --wallet.hotkey validator_1_hot --logging.debug &> validator-log.txt &


# sleep for 10 seconds to allow the miner and validator to start
#sleep 10

# registering validator to root network to get emissions rewards
#btcli root register --wallet.name validator_1 --wallet.hotkey validator_1_hot --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# Boosting the validator
#btcli root boost --netuid 1 --increase 1 --wallet.name validator_1 --wallet.hotkey validator_1_hot  --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt


# Commands to check the status of wallets
#btcli wallet overview --wallet.name subnet_owner --subtensor.chain_endpoint ws://127.0.0.1:9946
#btcli wallet overview --wallet.name miner_1 --subtensor.chain_endpoint ws://127.0.0.1:9946
#btcli wallet overview --wallet.name validator_1 --subtensor.chain_endpoint ws://127.0.0.1:9946

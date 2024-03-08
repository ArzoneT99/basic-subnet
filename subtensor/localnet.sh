#!/bin/bash

: "${CHAIN:=local}"
: "${BUILD_BINARY:=0}"
: "${SPEC_PATH:=/tmp/blockchain/}"
: "${FEATURES:=pow-faucet}"

FULL_PATH="$SPEC_PATH$CHAIN.json"

echo "*** Chainspec path: $FULL_PATH"

if [ ! -d "$SPEC_PATH" ]; then
	echo "*** Creating directory ${SPEC_PATH}..."
	mkdir $SPEC_PATH
fi

if [[ $BUILD_BINARY == "1" ]]; then
	echo "*** Building substrate binary..."
	cargo build --release --features "$FEATURES"
	echo "*** Binary compiled"
fi

echo "*** Building chainspec..."
node-subtensor build-spec --disable-default-bootnode --raw --chain $CHAIN > $FULL_PATH
echo "*** Chainspec built and output to file"

echo "*** Starting localnet nodes..."
alice_start=(
	node-subtensor
	--base-path /tmp/blockchain/alice
	--chain="$FULL_PATH"
	--alice
	--port 30334
	--ws-port 9946
	--rpc-port 9934
	--validator
	--allow-private-ipv4
	--discover-local
)

bob_start=(
	node-subtensor
	--base-path /tmp/blockchain/bob
	--chain="$FULL_PATH"
	--bob
    --port 30335
	--ws-port 9947
	--rpc-port 9935
	--validator
	--allow-private-ipv4
	--discover-local
)

(trap 'kill 0' SIGINT; ("${alice_start[@]}" 2>&1) & ("${bob_start[@]}" 2>&1))
import typing
import random
import time
import bittensor as bt
import hip
from hip.base.miner import BaseMinerNeuron

class Miner(BaseMinerNeuron):
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)

    async def forward(self, synapse: hip.protocol.HIPProtocol) -> hip.protocol.HIPProtocol:
        """
        Process the incoming HIPProtocol synapse by selecting an option based on the query.
        """
        if synapse.query_type == "task1":
            # Select an option for task1
            synapse.response = await self.select_option(synapse.query, synapse.options)
        elif synapse.query_type == "task2":
            # Select an option for task2
            synapse.response = await self.select_option(synapse.query, synapse.options)
        else:
            # Handle unknown query types
            synapse.response = "Unsure"
        
        return synapse

    async def blacklist(self, synapse: hip.protocol.HIPProtocol) -> typing.Tuple[bool, str]:
        """
        Determine if the incoming request should be blacklisted.
        """
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            bt.logging.trace(f"Blacklisting unregistered hotkey {synapse.dendrite.hotkey}")
            return True, "Unrecognized hotkey"

        if not self.metagraph.validator_permit[uid]:
            bt.logging.warning(f"Blacklisting request from non-validator hotkey {synapse.dendrite.hotkey}")
            return True, "Non-validator hotkey"

        return False, "Hotkey recognized!"

    async def priority(self, synapse: hip.protocol.HIPProtocol) -> float:
        """
        Assign priority to the incoming request.
        """
        caller_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        priority = float(self.metagraph.S[caller_uid])
        bt.logging.trace(f"Prioritizing {synapse.dendrite.hotkey} with value: {priority}")
        return priority

    async def select_option(self, query: str, options: typing.List[str]) -> str:
        """
        Select an option based on the given query and available options.
        """
        try: # Present the query and options to the user through an interface
            selected_option = await self.present_options_to_user(query, options)
            bt.logging.debug(f"User selected option '{selected_option}' for query: {query}")
            return selected_option
        except Exception as e:
            bt.logging.error(f"Error selecting option for query: {query}. Error: {str(e)}")
            return "Unsure"

    async def present_options_to_user(self, query: str, options: typing.List[str]) -> str:
        """
        Present the query and options to the user through an interface and return the selected option.
        """
    # TODO: Implement the logic to present the query and options to the user through an interface
    # and return the selected option
    # For now, we'll simulate user selection by randomly choosing an option
        selected_option = random.choice(options)
        return selected_option
# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)

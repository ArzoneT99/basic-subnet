import sys
import torch
import unittest
import bittensor as bt
from neurons.validator import Validator as Validator
from neurons.miner import Miner as Miner
from hip.protocol import HIPProtocol
from hip.validator.forward import forward
from hip.utils.uids import get_random_uids
from hip.validator.reward import get_rewards
from hip.base.validator import BaseValidatorNeuron
#WORK

class TemplateValidatorNeuronTestCase(unittest.TestCase):
    """
    This class contains unit tests for the RewardEvent classes.

    The tests cover different scenarios where completions may or may not be successful and the reward events are checked that they don't contain missing values.
    The `reward` attribute of all RewardEvents is expected to be a float, and the `is_filter_model` attribute is expected to be a boolean.
    """

    def setUp(self):
        sys.argv = [sys.argv[0]] + ["--config", "tests/configs/validator.json"]

        config = BaseValidatorNeuron.config()
        config.wallet._mock = True
        config.metagraph._mock = True
        config.subtensor._mock = True
        self.neuron = Validator(config)
        self.miner_uids = get_random_uids(self, k=10)
        
    def test_run_single_step(self):
        # Test a single step
        self.neuron.run_single_step()

    def test_sync_error_if_not_registered(self):
        # Test that the validator throws an error if it is not registered on metagraph
        with self.assertRaises(Exception):
            self.neuron.config.metagraph._mock = False
            self.neuron.run_single_step()

    def test_forward(self):
        # Test that the forward function returns the correct value
        uids = get_random_uids(self, k=10)
        inputs = torch.randn(10, 1024)
        outputs = forward(self.neuron, uids, inputs)
        self.assertEqual(outputs.shape, (10, 1024))

    def test_dummy_responses(self):
        # TODO: Test that the dummy responses are correctly constructed

        responses = self.neuron.dendrite.query(
            # Send the query to miners in the network.
            axons=[
                self.neuron.metagraph.axons[uid] for uid in self.miner_uids
            ],
            # Construct a dummy query.
            synapse=HIPProtocol(dummy_input=self.neuron.step),
            # All responses have the deserialize function called on them before returning.
            deserialize=True,
        )

        for i, response in enumerate(responses):
            self.assertEqual(response, self.neuron.step * 2)

    def test_reward(self):
        # TODO: Test that the reward function returns the correct value
        responses = self.neuron.dendrite.query(
            # Send the query to miners in the network.
            axons=[self.metagraph.axons[uid] for uid in self.miner_uids],
            # Construct a dummy query.
            synapse=HIPProtocol(dummy_input=self.neuron.step),
            # All responses have the deserialize function called on them before returning.
            deserialize=True,
        )

        rewards = get_rewards(self.neuron, responses)
        expected_rewards = torch.FloatTensor([1.0] * len(responses))
        self.assertEqual(rewards, expected_rewards)

    def test_reward_with_nan(self):
        # TODO: Test that NaN rewards are correctly sanitized
        # TODO: Test that a bt.logging.warning is thrown when a NaN reward is sanitized
        responses = self.neuron.dendrite.query(
            # Send the query to miners in the network.
            axons=[self.metagraph.axons[uid] for uid in self.miner_uids],
            # Construct a dummy query.
            synapse=HIPProtocol(dummy_input=self.neuron.step),
            # All responses have the deserialize function called on them before returning.
            deserialize=True,
        )

        rewards = get_rewards(self.neuron, responses)
        expected_rewards = rewards.clone()
        # Add NaN values to rewards
        rewards[0] = float("nan")

        with self.assertLogs(bt.logging, level="WARNING") as cm:
            self.neuron.update_scores(rewards, self.miner_uids)

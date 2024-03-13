import unittest
from unittest.mock import patch
import asyncio

from hip.validator.forward import forward
from hip.protocol import HIPProtocol
from hip.validator.reward import get_rewards, weighted_means_consensus
from hip.utils.uids import get_random_uids


class TestForward(unittest.TestCase):

    @patch('hip.validator.forward.HIPProtocol')
    @patch('hip.validator.forward.get_random_uids')
    @patch('hip.validator.forward.weighted_means_consensus')
    @patch('hip.validator.forward.get_rewards')
    async def test_forward(self, mock_get_rewards, mock_weighted_means_consensus, mock_get_random_uids, mock_HIPProtocol):

        # Mock dependencies
        mock_get_random_uids.side_effect = lambda _, k: [
            f'uid{i}' for i in range(k)]
        mock_weighted_means_consensus.return_value = 0.5
        mock_get_rewards.return_value = [1.0] * 8

        validator = MagicMock()
        validator.metagraph.axons = {'uid0': 'axon0', 'uid1': 'axon1'}
        validator.metagraph.S = {'uid0': torch.tensor(
            0.8), 'uid1': torch.tensor(0.6)}
        validator.dendrite = MagicMock()

        # Call forward
        await forward(validator)

        # Check calls
        validator.dendrite.assert_has_calls([
            call(axons=['axon0', 'axon1'], synapse=[
                 mock_HIPProtocol(), mock_HIPProtocol()], deserialize=True),
            call(axons=['axon0', 'axon1'], synapse=[mock_HIPProtocol(
                consensus=0.5), mock_HIPProtocol(consensus=0.5)], deserialize=True)
        ])
        mock_weighted_means_consensus.assert_called()
        mock_get_rewards.assert_called_with(validator, ANY, ANY)
        validator.update_scores.assert_called_once()


if __name__ == '__main__':
    unittest.main()

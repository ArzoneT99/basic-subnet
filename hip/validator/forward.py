import bittensor as bt
from hip.protocol import HIPProtocol
from hip.validator.reward import get_rewards
from hip.utils.uids import get_random_uids

async def forward(self):
    """
    The forward function is called by the validator every time step.
    It is responsible for querying the network and scoring the responses.
    """
    # Get the total number of active miners
    active_miners = len(self.metagraph.uids)

    # Calculate the number of groups based on the number of active miners
    num_groups = max(1, min(32, active_miners // 8))

    # Calculate the group size based on the number of active miners and groups
    group_size = active_miners // num_groups

    # Assign miners to groups
    miner_groups = [[] for _ in range(num_groups)]
    for i, uid in enumerate(self.metagraph.uids):
        group_index = i % num_groups
        miner_groups[group_index].append(uid)

    # Generate tasks for each group
    tasks = [self.generate_task() for _ in range(num_groups)]

    # Query each group of miners with their respective task
    responses_by_group = []
    for group_index, group_uids in enumerate(miner_groups):
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in group_uids],
            synapse=[HIPProtocol(data=tasks[group_index], uid=uid) for uid in group_uids],
            deserialize=True,
        )
        responses_by_group.append(responses)

    # Establish ground truth for each group based on responses
    ground_truths = [self.establish_ground_truth(responses) for responses in responses_by_group]

    # Query each group of miners with the ground truth from the other groups
    cross_validated_responses = []
    for group_index, group_uids in enumerate(miner_groups):
        other_group_indices = [i for i in range(num_groups) if i != group_index]
        other_ground_truths = [ground_truths[i] for i in other_group_indices]
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in group_uids],
            synapse=[HIPProtocol(data=tasks[group_index], uid=uid, consensus=truth) for uid, truth in zip(group_uids, other_ground_truths)],
            deserialize=True,
        )
        cross_validated_responses.extend(responses)

    # Calculate rewards based on responses and ground truths
    rewards = get_rewards(self, cross_validated_responses, ground_truths)

    # Update scores based on rewards
    self.update_scores(rewards, self.metagraph.uids)

    bt.logging.info("Validator forward pass completed")
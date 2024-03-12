import bittensor as bt
from hip.protocol import HIPProtocol
from hip.validator.reward import get_rewards
from hip.utils.uids import get_random_uids

async def forward(self):
    # Get the total number of active miners
    active_miners = len(self.metagraph.uids)

    # Calculate the group size based on the number of active miners
    group_size = min(active_miners // 2, self.config.neuron.sample_size)

    # Select random miner UIDs for group1
    group1_uids = get_random_uids(self, k=group_size)

    # Select random miner UIDs for group2, excluding the UIDs from group1
    group2_uids = get_random_uids(self, k=group_size, exclude=group1_uids.tolist())

    # Generate tasks for each group
    task1 = self.generate_task()
    task2 = self.generate_task()

    # Query the first group of miners with task1
    responses_group1_task1 = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in group1_uids],
        synapse=[HIPProtocol(query=task1, query_type="task1", uid=uid) for uid in group1_uids],
        deserialize=True,
    )

    # Query the second group of miners with task2
    responses_group2_task2 = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in group2_uids],
        synapse=[HIPProtocol(query=task2, query_type="task2", uid=uid) for uid in group2_uids],
        deserialize=True,
    )

    # Establish ground truth for task1 based on responses from group1
    ground_truth_task1 = self.establish_ground_truth(responses_group1_task1)

    # Establish ground truth for task2 based on responses from group2
    ground_truth_task2 = self.establish_ground_truth(responses_group2_task2)

    # Query the first group of miners with task2 and ground truth
    responses_group1_task2 = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in group1_uids],
        synapse=[HIPProtocol(query=task2, query_type="task2", uid=uid, ground_truth=ground_truth_task2) for uid in group1_uids],
        deserialize=True,
    )

    # Query the second group of miners with task1 and ground truth
    responses_group2_task1 = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in group2_uids],
        synapse=[HIPProtocol(query=task1, query_type="task1", uid=uid, ground_truth=ground_truth_task1) for uid in group2_uids],
        deserialize=True,
    )

    # Calculate rewards based on responses and ground truth
    rewards_group1 = get_rewards(self, responses_group1_task1 + responses_group1_task2, ground_truth_task1, ground_truth_task2)
    rewards_group2 = get_rewards(self, responses_group2_task1 + responses_group2_task2, ground_truth_task1, ground_truth_task2)
   
   # Update scores based on rewards
    self.update_scores(rewards_group1, group1_uids)
    self.update_scores(rewards_group2, group2_uids)

    bt.logging.info("Validator forward pass completed")
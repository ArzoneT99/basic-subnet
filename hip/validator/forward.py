import bittensor as bt
from hip.protocol import HIPProtocol
from hip.validator.reward import get_rewards, weighted_means_consensus
from hip.utils.uids import get_random_uids
import asyncio
import aiohttp


async def forward(self):
    """
    The forward function is called by the validator every time step.
    It is responsible for querying the network and scoring the responses.
    """
    # Get the total number of active miners
    active_miners = len(self.metagraph.uids)

    # Calculate the number of groups based on the number of active miners
    if active_miners < 32:
        num_groups = 2
    elif active_miners < 128:
        num_groups = 4
    else:
        num_groups = 8

    # Calculate the group size based on the number of active miners and groups
    group_size = max(active_miners // num_groups, 8)

    # Assign random UIDs to groups
    miner_groups = [get_random_uids(self, k=group_size) for _ in range(num_groups)]

    # Tasks for each group
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(num_groups):
            async with session.get("http://localhost:6891/api/questions") as response:
                if response.status == 200:
                    questions = await response.json()
                    if questions["questions"]:
                        task = questions["questions"][0]["value"]
                        tasks.append(task)
                else:
                    bt.logging.warning("No questions available from the API.")
        else:
            bt.logging.warning(f"Failed to retrieve questions from the API. Status code: {response.status}")

    # Query each group of miners with their respective task
    responses_by_group = []
    weights_by_group = []
    for group_index, group_uids in enumerate(miner_groups):
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in group_uids],
            synapse=[HIPProtocol(data=tasks[group_index], uid=uid) for uid in group_uids],
            deserialize=True,
        )
        responses_by_group.append([r.response for r in responses])
        weights_by_group.append([self.metagraph.S[uid].item() for uid in group_uids])

    # Establish ground truth for each group based on responses and weights
    ground_truths = [weighted_means_consensus(self, responses, weights)
                     for responses, weights in zip(responses_by_group, weights_by_group)]

    # Query each group of miners with the ground truth from the other groups
    cross_validated_responses = []
    for group_index, group_uids in enumerate(miner_groups):
        other_group_indices = [i for i in range(num_groups) if i != group_index]
        for other_group_index in other_group_indices:
            other_ground_truth = ground_truths[other_group_index]
            responses = await self.dendrite(
                axons=[self.metagraph.axons[uid] for uid in group_uids],
                synapse=[HIPProtocol(data=tasks[group_index], uid=uid, consensus=other_ground_truth) for uid in group_uids],
                deserialize=True,
            )
            cross_validated_responses.extend(responses)

    # Calculate rewards based on responses and ground truths
    rewards = get_rewards(self, cross_validated_responses, ground_truths)

    # Update scores based on rewards
    self.update_scores(rewards, [uid for group_uids in miner_groups for uid in group_uids])

    # Calculate average performance score for each miner over the past 16 hours
    for uid in self.metagraph.uids:
        # Get the miner's responses for the past 16 hours
        miner_responses = [r for r in cross_validated_responses if r.uid == uid]

        # Calculate the average score, treating "Not Answered" as a score of zero
        scores = [1 if r.response == r.consensus else 0 for r in miner_responses]
        not_answered_count = miner_responses.count("Not Answered")
        total_responses = len(miner_responses)
        if total_responses > 0:
            average_score = (sum(scores) + not_answered_count * 0) / total_responses
        else:
            average_score = 0

        # Report the average score to Bittensor as the miner's performance metric
        self.subtensor.set_weights(
            wallet=self.wallet,
            uids=[uid],
            weights=[average_score],
        )

    bt.logging.info("Validator forward pass completed")

    # Wait for 30 seconds before the next task
    await asyncio.sleep(30)
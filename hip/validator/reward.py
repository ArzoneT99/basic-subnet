import torch
from typing import List

def reward(selected_option: str, ground_truth: str) -> float:
    """
    Calculate the reward for a miner's selected option based on the ground truth.
    Args:
        selected_option (str): Miner's selected option ("Human", "AI", or "Unsure").
        ground_truth (str): Ground truth established by the validator ("Human" or "AI").
    Returns:
        float: Reward value for the miner's selected option.
    """
    if selected_option == ground_truth:
        return 1.0
    elif selected_option == "Unsure":
        return 0.5
    else:
        return 0.0

def get_rewards(
    self,
    selected_options: List[str],
    ground_truth_task1: str,
    ground_truth_task2: str,
) -> torch.FloatTensor:
    """
    Calculate the rewards for a list of miner selected options based on the ground truth for each task.
    Args:
        selected_options (List[str]): List of miner selected options.
        ground_truth_task1 (str): Ground truth for task1 ("Human" or "AI").
        ground_truth_task2 (str): Ground truth for task2 ("Human" or "AI").
    Returns:
        torch.FloatTensor: Tensor of reward values for each miner selected option.
    """
    rewards = []
    for i, option in enumerate(selected_options):
        if i < len(selected_options) // 2:
            # First half of options correspond to task1
            rewards.append(reward(option, ground_truth_task1))
        else:
            # Second half of options correspond to task2
            rewards.append(reward(option, ground_truth_task2))
    return torch.FloatTensor(rewards).to(self.device)
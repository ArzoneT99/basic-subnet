import torch
from typing import List

def reward(selected_option: str, ground_truth: str) -> float:
    """
    Calculate the reward for a miner's selected option based on the ground truth.
    Args:
        selected_option (str): Miner's selected option ("Very Human-like", "Somewhat Human-like", "Not Human-like", or "Unsure").
        ground_truth (str): Ground truth established by the validator ("Very Human-like", "Somewhat Human-like", or "Not Human-like").
    Returns:
        float: Reward value for the miner's selected option.
    """
    if selected_option == ground_truth:
        return 1.0
    elif selected_option == "Unsure":
        return 0.5
    else:
        return 0.0

def weighted_means_consensus(self, options: List[str], weights: List[float]) -> str:
    """
    Calculate the weighted means consensus based on the selected options and their corresponding weights.
    Args:
        options (List[str]): List of selected options.
        weights (List[float]): List of weights corresponding to each option.
    Returns:
        str: The consensus option based on the weighted means.
    """
    # Assign numeric values to options
    option_values = {
        "Very Human-like": 2,
        "Somewhat Human-like": 1,
        "Not Human-like": 0,
    }

    # Convert options to numeric values
    numeric_options = [option_values[option] for option in options if option in option_values]

    # Calculate the weighted mean
    weighted_mean = sum([value * weight for value, weight in zip(numeric_options, weights)]) / sum(weights)

    # Determine the consensus option based on the weighted mean
    if weighted_mean >= 1.5:
        return "Very Human-like"
    elif weighted_mean >= 0.5:
        return "Somewhat Human-like"
    else:
        return "Not Human-like"

def get_rewards(
    self,
    selected_options: List[str],
    weights: List[float],
) -> torch.FloatTensor:
    """
    Calculate the rewards for a list of miner selected options based on the weighted means consensus.
    Args:
        selected_options (List[str]): List of miner selected options.
        weights (List[float]): List of weights corresponding to each miner's option.
    Returns:
        torch.FloatTensor: Tensor of reward values for each miner.
    """
    # Calculate the consensus using weighted means
    consensus_option = self.weighted_means_consensus(selected_options, weights)

    # Calculate the rewards based on the consensus
    rewards = [reward(option, consensus_option) for option in selected_options]

    return torch.FloatTensor(rewards).to(self.device)
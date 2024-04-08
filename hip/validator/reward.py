import torch
from typing import List
import hip
from hip.protocol import HIPProtocol
from difflib import SequenceMatcher
import time

def reward(response: hip.protocol.HIPProtocol, ground_truth: str) -> float:
    """
    Calculate the reward for a miner's response based on the ground truth and response time.
    Args:
        response (hip.protocol.HIPProtocol): Miner's response.
        ground_truth (str): Ground truth established by the validator.
    Returns:
        float: Reward value for the miner's response.
    """
    if response.response == "Not Answered":
        return 0.0

    # Calculate the response time in seconds
    response_time = time.time() - response.timestamp

    # The minmax time thresholds for full reward
    min_time_threshold = 3.1416999  # Minimum time required to receive full reward
    max_time_threshold = 60.0  # Maximum time allowed for full reward

    # Calculate the similarity ratio between the response and the ground truth
    similarity_ratio = SequenceMatcher(None, response.response.lower(), ground_truth.lower()).ratio()

    # Multiple reward points based on the similarity ratio
    if similarity_ratio >= 0.9:
        reward_value = 1.0
    elif similarity_ratio >= 0.7:
        reward_value = 0.8
    elif similarity_ratio >= 0.5:
        reward_value = 0.6
    else:
        reward_value = 0.0

    # Calculate the time-based weight
    if response_time < min_time_threshold:
        # Penalize responses submitted too quickly
        time_weight = 0.0
    elif response_time > max_time_threshold:
        # Penalize responses submitted too slowly
        time_weight = 0.0
    else:
        # Calculate the time-based weight for responses within the valid time range
        time_weight = (response_time - min_time_threshold) / (max_time_threshold - min_time_threshold)

    # Calculate the weighted reward
    reward_value = similarity_ratio * time_weight

    return reward_value
    

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
    numeric_options = [option_values[option]
                       for option in options if option in option_values]

    # Calculate the weighted mean
    weighted_mean = sum([value * weight for value,
                        weight in zip(numeric_options, weights)]) / sum(weights)

    # Determine the consensus option based on the weighted mean
    if weighted_mean >= 1.5:
        return "Very Human-like"
    elif weighted_mean >= 0.5:
        return "Somewhat Human-like"
    else:
        return "Not Human-like"
    

def get_rewards(
    self,
    responses: List[hip.protocol.HIPProtocol],
    ground_truths: List[str],
) -> torch.FloatTensor:
    """
    Calculate the rewards for a list of miner responses based on the ground truths.
    Args:
        responses (List[hip.protocol.HIPProtocol]): List of miner responses.
        ground_truths (List[str]): List of ground truths corresponding to each response.
    Returns:
        torch.FloatTensor: Tensor of reward values for each miner.
    """
    rewards = [reward(r, gt) for r, gt in zip(responses, ground_truths)]
    return torch.FloatTensor(rewards).to(self.device)

# HIP (Human Intelligence Primitave) Consensus Mechanism

The HIP consensus mechanism is designed to incentivize and reward human miners for their contributions in determining whether data is human-like. The primary goal of the HIP subnet is to prevent Bittensor from becoming a dark forest, where malicious actors can manipulate the network for their own benefit. By leveraging human intuition and judgment, the HIP consensus mechanism aims to maintain the integrity and trustworthiness of the Bittensor network.

# Code Overview

## 1. protocol.py

The `protocol.py` file defines the communication protocol between subnet validators and miners. It contains the `HIPProtocol` class, which specifies the required and optional fields for the protocol.

#### `HIPProtocol Class`

- `query`: The query or task description sent by the validator to the miner.
- `query_type`: The type of query or task.
- `uid`: The unique identifier of the miner.
- `options`: The list of options available for the miner to select from.
- `response`: The miner's selected option in response to the query.
- `weights`: The weights assigned by the validator to the miner's response.

The `HIPProtocol` class also provides `serialize` and `deserialize` methods to convert the protocol instance to bytes and vice versa for network transmission.

## 2. miner.py

The `miner.py` file contains the `Miner` class, which represents a miner in the HIP consensus mechanism. It inherits from `BaseMinerNeuron` and defines the miner's behavior.

#### `Miner Class`

- `forward`: Processes the incoming `HIPProtocol` synapse by selecting an option based on the query and available options.
- `blacklist`: Determines if an incoming request should be blacklisted based on the miner's configuration and the request's hotkey.
- `priority`: Assigns priority to incoming requests based on the caller's stake.
- `select_option`: Sends the query and options to the user and retrieves the selected option.
- `present_options_to_user`: A placeholder for implementing the logic to present the query and options to the user through an interface.

## 3. validator.py

The `validator.py` file contains the `Validator` class, which represents a validator in the HIP consensus mechanism. It inherits from `BaseValidatorNeuron` and defines the validator's behavior.

#### `Validator Class`

- `forward`: The entry point for the validator's forward pass, which delegates the responsibility to the `forward` function defined in the `hip/validator/forward.py` file.

## 4. forward.py

The `forward.py` file defines the `forward` function, which is responsible for the validator's forward pass logic.

#### `forward Function`

- Selects random miner UIDs for two groups using the `get_random_uids` function.
- Generates tasks for each group and queries the miners with the tasks using the `dendrite` method.
- Establishes the ground truth for each task based on the initial responses from the miners.
- Queries the miners again with the established ground truth and calculates the rewards using the `get_rewards` function from the `hip/validator/reward.py` file.
- Updates the scores of the miners based on the calculated rewards.

## 5. reward.py

The `reward.py` file defines the reward calculation and distribution logic for the HIP consensus mechanism.

#### `Reward Functions`

- `reward`: Calculates the reward for a miner's selected option based on the ground truth.
- `weighted_means_consensus`: Calculates the consensus option based on the selected options and their corresponding weights using the weighted means approach.
- `get_rewards`: Calculates the rewards for a list of miner selected options based on the weighted means consensus.

# Consensus Mechanism Analogy: Teachers with Two Classes of Students

Imagine two teachers, each responsible for a class of students. The teachers are tasked with evaluating the students' understanding of a particular subject matter. In this analogy, the teachers represent the validators, and the students represent the miners in the HIP consensus mechanism.

1. **Task Assignment:**
   - Each teacher (validator) prepares a set of questions (tasks) related to the subject matter.
   - The teachers distribute the questions to their respective classes of students (miners).

2. **Student Response:**
   - The students (miners) in each class work independently to provide their answers (selected options) to the questions (tasks) given by their teacher (validator).
   - The students have three options to choose from for each question: "Human," "AI," or "Unsure."

3. **Establishing Ground Truth:**
   - After collecting the initial responses from their students, each teacher (validator) determines the most common answer (majority vote) for each question within their class.
   - The majority answer for each question is considered the ground truth for that particular class.

4. **Cross-Validation:**
   - The teachers (validators) then exchange the questions (tasks) and the established ground truth with each other.
   - Each teacher distributes the questions from the other class to their own students (miners) and asks them to provide their answers (selected options) based on the established ground truth.

5. **Consensus Calculation:**
   - The teachers (validators) collect the responses from both classes of students (miners) for all the questions (tasks).
   - They calculate the weighted means consensus by considering the selected options and their corresponding weights (e.g., based on the students' past performance or reliability).
   - The weighted means consensus determines the final consensus answer for each question (task).

6. **Reward Distribution:**
   - The teachers (validators) evaluate the performance of each student (miner) based on their responses and alignment with the consensus answer.
   - Students who provided accurate responses that match the consensus answer receive higher rewards, while those who were unsure or provided incorrect responses receive lower rewards.
   - The rewards are distributed to the students (miners) based on their performance and contribution to the consensus.

Through this analogy, we can see how the HIP consensus mechanism works to achieve consensus on whether data is human-generated or machine-generated. The validators (teachers) coordinate the tasks, establish ground truth, and calculate the consensus, while the miners (students) provide their opinions and judgments. The rewards are distributed based on the miners' performance and alignment with the consensus, incentivizing them to contribute intuitvly to the network.


The HIP consensus mechanism can be summarized as follows:
1. Validators generate tasks and assign them to miners.
2. Miners provide responses to the tasks.
3. Validators establish the ground truth based on the majority vote of miner responses.
4. Validators exchange tasks and ground truth for cross-validation.
5. Miners provide responses to the cross-validated tasks.
6. The weighted means consensus is calculated for each task.
7. Rewards are distributed to miners based on their responses and alignment with the consensus.


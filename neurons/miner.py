import typing
import asyncio
import bittensor as bt
import hip
from hip.base.miner import BaseMinerNeuron
from hip.hip_service import main
import aiohttp
import time

class Miner(BaseMinerNeuron):
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)

    async def forward(self, synapse: hip.protocol.HIPProtocol) -> hip.protocol.HIPProtocol:
        """
        Process the incoming HIPProtocol synapse by selecting an option based on the task.
        """
        # Extract the task data from the synapse
        task_data = synapse.data

        # Determine the human-likeness of the task data
        human_likeness = await self.evaluate_human_likeness(task_data)

        # Set the miner's response in the synapse
        synapse.response = human_likeness

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

    async def evaluate_human_likeness(self, task_data: str) -> str:
        """
        Evaluate the human-likeness of the given task data.
        """
        try:
            # Retrieve questions from the API
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:6891/api/questions") as response:
                    if response.status == 200:
                        questions = await response.json()
                        bt.logging.debug(f"Retrieved questions successfully")
                    else:
                        bt.logging.error(f"Error retrieving questions")
                        return "Not Answered"

            # Find the question corresponding to the task data
            question = next((q for q in questions["questions"] if q["id"] == task_data["id"]), None)
            if question is None:
                bt.logging.error(f"Question not found for task data: {task_data}")
                return "Not Answered"

            # Present the question to the user through an interface
            try:
                human_likeness = await asyncio.wait_for(self.present_task_to_user(question), timeout=180)  # 3 minutes timeout
            except asyncio.TimeoutError:
                bt.logging.debug(f"User did not respond within the timeout for task data: {task_data}")
                human_likeness = "Not Answered"

            # Submit the user's answer to the API
            async with aiohttp.ClientSession() as session:
                payload = {
                    "id": task_data["id"],
                    "answer": human_likeness
                }
                async with session.post("http://localhost:6891/api/answer", json=payload) as response:
                    if response.status == 201:
                        bt.logging.debug(f"User answer submitted successfully for task data: {task_data}")
                    else:
                        bt.logging.error(f"Error submitting user answer for task data: {task_data}")
                        return "Not Answered"

            return human_likeness
        except Exception as e:
            bt.logging.error(f"Error evaluating human-likeness for task data: {task_data}. Error: {str(e)}")
            return "Not Answered"

    async def present_task_to_user(self, question: dict) -> str:
        """
        Present the question to the user through an interface and return the evaluated human-likeness.
        """
        try:
            # Extract the relevant information from the question
            question_text = question["label"]
            question_type = question["type"]
            question_options = question["options"]

            # Present the question to the user through CLI interface
            print(f"Question: {question_text}")
            if question_type == "select":
                print("Options:")
                for i, option in enumerate(question_options, start=1):
                    print(f"{i}. {option}")
                user_input = input("Enter the number corresponding to your answer: ")
                try:
                    selected_index = int(user_input) - 1
                    if 0 <= selected_index < len(question_options):
                        human_likeness = question_options[selected_index]
                    else:
                        print("Invalid selection. Defaulting to 'Not Answered'.")
                        human_likeness = "Not Answered"
                except ValueError:
                    print("Invalid input. Defaulting to 'Not Answered'.")
                    human_likeness = "Not Answered"
            else:
                user_input = input("Enter your answer: ")
                human_likeness = user_input

            return human_likeness
        except Exception as e:
            bt.logging.error(f"Error presenting task to user. Error: {str(e)}")
            return "Not Answered"

# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)
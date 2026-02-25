from src.agent.agent import get_agent
from src.agent.log import setup_logging
setup_logging()

agent = get_agent()

print("KI-Agent gestartet. Tippe 'exit' zum Beenden.\n")

while True:
    user = input("You> ")
    if user.lower() in ["exit", "quit"]:
        break

    answer = agent.ask(user)
    print("\nAgent>", answer, "\n")
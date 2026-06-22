from orchestrator.orchestrator import Orchestrator

# Secretary system main contact interface
# Can change this up to a proper interface in the future

def main():

    orchestrator = Orchestrator()

    while True:

        input_text = input(">>> ")
        if input_text.lower() == "bye":
            break


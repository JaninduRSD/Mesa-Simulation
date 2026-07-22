from model import GuessingGameModel


def main():
    model = GuessingGameModel(
        num_explorers=1000,
        max_number=10000,
        seed=7,
    )

    print(f"Hidden target number: {model.target_number}")

    model.organization.describe()

    max_steps = 100

    for _ in range(max_steps):
        if model.completed:
            break

        model.step()

    print("\nSimulation finished.")
    print(f"Completed: {model.completed}")
    print(f"Steps used: {model.step_count}")


if __name__ == "__main__":
    main()
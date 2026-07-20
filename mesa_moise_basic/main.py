from model import GuessingGameModel


def main():
    model = GuessingGameModel(
        num_explorers=3,
        max_number=20,
        seed=7,
    )

    print(f"Hidden target number: {model.target_number}")

    model.organization.describe()

    max_steps = 10

    for _ in range(max_steps):
        if model.completed:
            break

        model.step()

    print("\nSimulation finished.")
    print(f"Completed: {model.completed}")
    print(f"Steps used: {model.step_count}")


if __name__ == "__main__":
    main()
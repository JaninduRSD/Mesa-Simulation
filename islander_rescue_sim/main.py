from model import IslanderRescueModel


def main():
    model = IslanderRescueModel(
        num_scouts=20,
        num_rescuers=20,
        num_medics=10,
        num_incidents=2000,
        seed=10,
    )

    model.institution.describe()

    max_steps = 2000

    for _ in range(max_steps):
        if model.completed:
            break

        model.step()
        model.print_status()

    print("\nSimulation finished.")
    print(f"Completed: {model.completed}")
    print(f"Steps used: {model.step_count}")
    print(f"Total protocol violations: {model.violation_count}")


if __name__ == "__main__":
    main()

from model import RescueCoordinationModel


def main():
    model = RescueCoordinationModel(
        num_scouts=15,
        num_rescuers=25,
        num_medics=50,
        num_incidents=1000,
        seed=42,
    )

    model.organization.describe()

    max_steps = 170

    for _ in range(max_steps):
        if model.completed:
            break

        model.step()
        model.print_status()

    print("\nSimulation finished.")
    print(f"Completed: {model.completed}")
    print(f"Steps used: {model.step_count}")
    print(f"Total norm violations: {model.violation_count}")


if __name__ == "__main__":
    main()

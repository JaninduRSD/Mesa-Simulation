from mesa import Model

from agents import ScoutAgent, CoordinatorAgent, RescuerAgent, MedicAgent
from opera_organization import OperaOrganization


class RescueCoordinationModel(Model):
    def __init__(
        self,
        num_scouts=2,
        num_rescuers=2,
        num_medics=1,
        num_incidents=5,
        seed=None,
    ):
        super().__init__(seed=seed)

        self.organization = OperaOrganization(self)

        self.agent_list = []
        self.incidents = []
        self.step_count = 0
        self.violation_count = 0
        self.completed = False

        self.create_incidents(num_incidents)
        self.create_agents(num_scouts, num_rescuers, num_medics)

    def create_incidents(self, num_incidents):
        for i in range(num_incidents):
            self.incidents.append(
                {
                    "id": i,
                    "severity": self.random.randint(1, 5),
                    "discovered": False,
                    "reported": False,
                    "assigned_rescuer": None,
                    "rescued": False,
                    "assigned_medic": None,
                    "treated": False,
                }
            )

    def create_agents(self, num_scouts, num_rescuers, num_medics):
        for _ in range(num_scouts):
            self.agent_list.append(ScoutAgent(self))

        self.agent_list.append(CoordinatorAgent(self))

        for _ in range(num_rescuers):
            self.agent_list.append(RescuerAgent(self))

        for _ in range(num_medics):
            self.agent_list.append(MedicAgent(self))

    def get_incident(self, incident_id):
        for incident in self.incidents:
            if incident["id"] == incident_id:
                return incident

        return None

    def step(self):
        self.step_count += 1

        print("\n==============================")
        print(f"Step {self.step_count}")
        print("==============================")

        # 1. Scouts discover and report incidents
        for agent in self.agent_list:
            if agent.role_name == "Scout":
                agent.step()

        # 2. Coordinator assigns rescue/treatment tasks
        for agent in self.agent_list:
            if agent.role_name == "Coordinator":
                agent.step()

        # 3. Rescuers rescue assigned incidents
        for agent in self.agent_list:
            if agent.role_name == "Rescuer":
                agent.step()

        # 4. Coordinator checks again after rescue
        for agent in self.agent_list:
            if agent.role_name == "Coordinator":
                agent.step()

        # 5. Medics treat rescued incidents
        for agent in self.agent_list:
            if agent.role_name == "Medic":
                agent.step()

        self.check_completion()

    def check_completion(self):
        self.completed = all(
            incident["treated"] for incident in self.incidents
        )

    def print_status(self):
        print("\nCurrent Incident Status")
        print("-----------------------")

        for incident in self.incidents:
            print(
                f"Incident {incident['id']} | "
                f"severity={incident['severity']} | "
                f"discovered={incident['discovered']} | "
                f"reported={incident['reported']} | "
                f"rescued={incident['rescued']} | "
                f"treated={incident['treated']}"
            )

        print(f"\nViolations: {self.violation_count}")
        
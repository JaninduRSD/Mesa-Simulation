from mesa import Model

from agents import ScoutAgent, CoordinatorAgent, RescuerAgent, MedicAgent
from islander_institution import IslanderInstitution


class IslanderRescueModel(Model):
    def __init__(
        self,
        num_scouts=2,
        num_rescuers=2,
        num_medics=1,
        num_incidents=4,
        seed=None,
    ):
        super().__init__(seed=seed)

        self.agent_list = []
        self.incidents = []
        self.step_count = 0
        self.violation_count = 0
        self.completed = False

        self.create_incidents(num_incidents)
        self.create_agents(num_scouts, num_rescuers, num_medics)

        self.institution = IslanderInstitution(self)

    def create_incidents(self, num_incidents):
        for i in range(num_incidents):
            self.incidents.append(
                {
                    "id": i,
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

    def get_agent_by_role(self, role_name):
        for agent in self.agent_list:
            if agent.role_name == role_name:
                return agent

        return None

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

        coordinator = self.get_agent_by_role("Coordinator")

        # Scene 1: Discovery
        self.institution.current_scene_name = "discovery"
        print("\nScene: Discovery")
        for agent in self.agent_list:
            if agent.role_name == "Scout":
                agent.step()
        coordinator.step_discovery_messages()

        # Scene 2: Assignment
        self.institution.current_scene_name = "assignment"
        print("\nScene: Assignment")
        coordinator.assign_rescue()
        for agent in self.agent_list:
            if agent.role_name == "Rescuer":
                agent.process_assignment()

        # Scene 3: Rescue
        self.institution.current_scene_name = "rescue"
        print("\nScene: Rescue")
        for agent in self.agent_list:
            if agent.role_name == "Rescuer":
                agent.do_rescue()
        coordinator.process_rescue_done()

        # Scene 4: Treatment Assignment
        self.institution.current_scene_name = "treatment_assignment"
        print("\nScene: Treatment Assignment")
        coordinator.assign_treatment()
        for agent in self.agent_list:
            if agent.role_name == "Medic":
                agent.process_assignment()

        # Scene 5: Treatment
        self.institution.current_scene_name = "treatment"
        print("\nScene: Treatment")
        for agent in self.agent_list:
            if agent.role_name == "Medic":
                agent.do_treatment()
        coordinator.process_treatment_done()

        # Scene 6: Verification
        self.institution.current_scene_name = "verification"
        print("\nScene: Verification")
        coordinator.verify_all()

    def print_status(self):
        print("\nIncident Status")
        print("---------------")
        for incident in self.incidents:
            print(
                f"Incident {incident['id']} | "
                f"discovered={incident['discovered']} | "
                f"reported={incident['reported']} | "
                f"rescued={incident['rescued']} | "
                f"treated={incident['treated']}"
            )

        print(f"\nProtocol violations: {self.violation_count}")
        
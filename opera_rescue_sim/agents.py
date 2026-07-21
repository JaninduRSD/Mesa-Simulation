from mesa import Agent


class BaseRoleAgent(Agent):
    def __init__(self, model, role_name):
        super().__init__(model)
        self.role_name = role_name

    def authorized(self, action, data):
        return self.model.organization.authorize(self, action, data)


class ScoutAgent(BaseRoleAgent):
    def __init__(self, model):
        super().__init__(model, "Scout")

    def step(self):
        undiscovered = [
            incident for incident in self.model.incidents
            if not incident["discovered"]
        ]

        if not undiscovered:
            return

        incident = self.model.random.choice(undiscovered)
        incident["discovered"] = True

        action = "report_incident"
        data = {"incident_id": incident["id"]}

        if self.authorized(action, data):
            incident["reported"] = True
            print(
                f"Scout {self.unique_id} discovered and reported "
                f"Incident {incident['id']}"
            )


class CoordinatorAgent(BaseRoleAgent):
    def __init__(self, model):
        super().__init__(model, "Coordinator")

    def step(self):
        self.assign_rescuers()
        self.assign_medics()

    def assign_rescuers(self):
        available_rescuers = [
            agent for agent in self.model.agent_list
            if agent.role_name == "Rescuer" and agent.current_incident is None
        ]

        incidents_needing_rescue = [
            incident for incident in self.model.incidents
            if incident["reported"]
            and not incident["rescued"]
            and incident["assigned_rescuer"] is None
        ]

        for incident in incidents_needing_rescue:
            if not available_rescuers:
                return

            rescuer = available_rescuers.pop(0)

            action = "assign_rescue"
            data = {"incident_id": incident["id"]}

            if self.authorized(action, data):
                incident["assigned_rescuer"] = rescuer.unique_id
                rescuer.current_incident = incident["id"]

                print(
                    f"Coordinator assigned Rescuer {rescuer.unique_id} "
                    f"to Incident {incident['id']}"
                )

    def assign_medics(self):
        available_medics = [
            agent for agent in self.model.agent_list
            if agent.role_name == "Medic" and agent.current_incident is None
        ]

        incidents_needing_treatment = [
            incident for incident in self.model.incidents
            if incident["rescued"]
            and not incident["treated"]
            and incident["assigned_medic"] is None
        ]

        for incident in incidents_needing_treatment:
            if not available_medics:
                return

            medic = available_medics.pop(0)

            action = "assign_medic"
            data = {"incident_id": incident["id"]}

            if self.authorized(action, data):
                incident["assigned_medic"] = medic.unique_id
                medic.current_incident = incident["id"]

                print(
                    f"Coordinator assigned Medic {medic.unique_id} "
                    f"to Incident {incident['id']}"
                )


class RescuerAgent(BaseRoleAgent):
    def __init__(self, model):
        super().__init__(model, "Rescuer")
        self.current_incident = None

    def step(self):
        if self.current_incident is None:
            return

        incident = self.model.get_incident(self.current_incident)

        if incident is None or incident["rescued"]:
            self.current_incident = None
            return

        action = "rescue_incident"
        data = {"incident_id": incident["id"]}

        if self.authorized(action, data):
            incident["rescued"] = True
            print(
                f"Rescuer {self.unique_id} rescued "
                f"Incident {incident['id']}"
            )

            self.current_incident = None


class MedicAgent(BaseRoleAgent):
    def __init__(self, model):
        super().__init__(model, "Medic")
        self.current_incident = None

    def step(self):
        if self.current_incident is None:
            return

        incident = self.model.get_incident(self.current_incident)

        if incident is None or incident["treated"]:
            self.current_incident = None
            return

        action = "treat_incident"
        data = {"incident_id": incident["id"]}

        if self.authorized(action, data):
            incident["treated"] = True
            print(
                f"Medic {self.unique_id} treated "
                f"Incident {incident['id']}"
            )

            self.current_incident = None
            
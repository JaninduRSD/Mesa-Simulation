from mesa import Agent

from islander_institution import Message


class BaseInstitutionAgent(Agent):
    def __init__(self, model, role_name):
        super().__init__(model)
        self.role_name = role_name
        self.inbox = []

    def send(self, receiver, performative, content):
        message = Message(
            sender=self,
            receiver=receiver,
            performative=performative,
            content=content,
        )

        return self.model.institution.send_message(message)

    def clear_inbox(self):
        self.inbox.clear()


class ScoutAgent(BaseInstitutionAgent):
    def __init__(self, model):
        super().__init__(model, "Scout")

    def step(self):
        undiscovered = [
            incident for incident in self.model.incidents
            if not incident["discovered"]
        ]

        if not undiscovered:
            return

        incident = self.random.choice(undiscovered)
        incident["discovered"] = True

        coordinator = self.model.get_agent_by_role("Coordinator")

        if coordinator is not None:
            self.send(
                coordinator,
                "report_incident",
                {"incident_id": incident["id"]},
            )


class CoordinatorAgent(BaseInstitutionAgent):
    def __init__(self, model):
        super().__init__(model, "Coordinator")

    def step_discovery_messages(self):
        for message in self.inbox:
            if message.performative == "report_incident":
                incident_id = message.content["incident_id"]
                incident = self.model.get_incident(incident_id)

                if incident is not None:
                    incident["reported"] = True
                    print(f"Coordinator recorded Incident {incident_id} as reported.")

        self.clear_inbox()

    def assign_rescue(self):
        available_rescuers = [
            agent for agent in self.model.agent_list
            if agent.role_name == "Rescuer" and agent.current_incident is None
        ]

        incidents = [
            incident for incident in self.model.incidents
            if incident["reported"]
            and not incident["rescued"]
            and incident["assigned_rescuer"] is None
        ]

        for incident in incidents:
            if not available_rescuers:
                return

            rescuer = available_rescuers.pop(0)
            incident["assigned_rescuer"] = rescuer.unique_id
            rescuer.current_incident = incident["id"]

            self.send(
                rescuer,
                "assign_rescue",
                {"incident_id": incident["id"]},
            )

    def process_rescue_done(self):
        for message in self.inbox:
            if message.performative == "rescue_done":
                incident_id = message.content["incident_id"]
                incident = self.model.get_incident(incident_id)

                if incident is not None:
                    incident["rescued"] = True
                    print(f"Coordinator confirmed Incident {incident_id} rescued.")

        self.clear_inbox()

    def assign_treatment(self):
        available_medics = [
            agent for agent in self.model.agent_list
            if agent.role_name == "Medic" and agent.current_incident is None
        ]

        incidents = [
            incident for incident in self.model.incidents
            if incident["rescued"]
            and not incident["treated"]
            and incident["assigned_medic"] is None
        ]

        for incident in incidents:
            if not available_medics:
                return

            medic = available_medics.pop(0)
            incident["assigned_medic"] = medic.unique_id
            medic.current_incident = incident["id"]

            self.send(
                medic,
                "assign_treatment",
                {"incident_id": incident["id"]},
            )

    def process_treatment_done(self):
        for message in self.inbox:
            if message.performative == "treatment_done":
                incident_id = message.content["incident_id"]
                incident = self.model.get_incident(incident_id)

                if incident is not None:
                    incident["treated"] = True
                    print(f"Coordinator confirmed Incident {incident_id} treated.")

        self.clear_inbox()

    def verify_all(self):
        all_treated = all(
            incident["treated"] for incident in self.model.incidents
        )

        if all_treated:
            self.model.completed = True
            print("Coordinator verification: all incidents treated.")
        else:
            print("Coordinator verification: task not completed yet.")


class RescuerAgent(BaseInstitutionAgent):
    def __init__(self, model):
        super().__init__(model, "Rescuer")
        self.current_incident = None

    def process_assignment(self):
        for message in self.inbox:
            if message.performative == "assign_rescue":
                self.current_incident = message.content["incident_id"]
                print(
                    f"Rescuer {self.unique_id} accepted rescue assignment "
                    f"for Incident {self.current_incident}."
                )

        self.clear_inbox()

    def do_rescue(self):
        if self.current_incident is None:
            return

        coordinator = self.model.get_agent_by_role("Coordinator")

        if coordinator is not None:
            self.send(
                coordinator,
                "rescue_done",
                {"incident_id": self.current_incident},
            )

        self.current_incident = None


class MedicAgent(BaseInstitutionAgent):
    def __init__(self, model):
        super().__init__(model, "Medic")
        self.current_incident = None

    def process_assignment(self):
        for message in self.inbox:
            if message.performative == "assign_treatment":
                self.current_incident = message.content["incident_id"]
                print(
                    f"Medic {self.unique_id} accepted treatment assignment "
                    f"for Incident {self.current_incident}."
                )

        self.clear_inbox()

    def do_treatment(self):
        if self.current_incident is None:
            return

        coordinator = self.model.get_agent_by_role("Coordinator")

        if coordinator is not None:
            self.send(
                coordinator,
                "treatment_done",
                {"incident_id": self.current_incident},
            )

        self.current_incident = None
        
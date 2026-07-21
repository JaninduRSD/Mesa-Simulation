class OperaOrganization:
    """
    Simple OperA-like organization layer.

    OperA idea:
    - Agents enact roles.
    - Roles have social contracts.
    - Norms control what actions are valid.
    - Violations are logged.
    """

    def __init__(self, model):
        self.model = model

        self.contracts = {
            "Scout": {
                "commitment": "Find incidents and report them to the Coordinator.",
                "allowed_actions": {"report_incident"},
            },
            "Coordinator": {
                "commitment": "Assign rescue and treatment tasks.",
                "allowed_actions": {"assign_rescue", "assign_medic"},
            },
            "Rescuer": {
                "commitment": "Rescue assigned incidents.",
                "allowed_actions": {"rescue_incident"},
            },
            "Medic": {
                "commitment": "Treat rescued incidents.",
                "allowed_actions": {"treat_incident"},
            },
        }

    def describe(self):
        print("\nOperA-like Organization")
        print("-----------------------")
        for role, contract in self.contracts.items():
            print(f"Role: {role}")
            print(f"  Commitment: {contract['commitment']}")
            print(f"  Allowed actions: {sorted(contract['allowed_actions'])}")

    def authorize(self, agent, action, data):
        """
        Main authorization method.
        First checks role contract.
        Then checks norms.
        """

        if not self.action_allowed_by_contract(agent, action):
            self.log_violation(agent, action, "Action not allowed by role contract")
            return False

        if not self.norms_satisfied(agent, action, data):
            return False

        return True

    def action_allowed_by_contract(self, agent, action):
        role = agent.role_name
        allowed_actions = self.contracts[role]["allowed_actions"]
        return action in allowed_actions

    def norms_satisfied(self, agent, action, data):
        """
        OperA-like norms.
        These are social rules of the organization.
        """

        incident_id = data.get("incident_id")
        incident = self.model.get_incident(incident_id)

        if action == "report_incident":
            if incident is None:
                self.log_violation(agent, action, "Incident does not exist")
                return False

            if not incident["discovered"]:
                self.log_violation(agent, action, "Cannot report undiscovered incident")
                return False

        if action == "assign_rescue":
            if incident is None:
                self.log_violation(agent, action, "Incident does not exist")
                return False

            if not incident["reported"]:
                self.log_violation(agent, action, "Cannot assign unreported incident")
                return False

        if action == "assign_medic":
            if incident is None:
                self.log_violation(agent, action, "Incident does not exist")
                return False

            if not incident["rescued"]:
                self.log_violation(agent, action, "Cannot assign medic before rescue")
                return False

        if action == "rescue_incident":
            if incident is None:
                self.log_violation(agent, action, "Incident does not exist")
                return False

            if incident["assigned_rescuer"] != agent.unique_id:
                self.log_violation(agent, action, "Rescuer not assigned to this incident")
                return False

        if action == "treat_incident":
            if incident is None:
                self.log_violation(agent, action, "Incident does not exist")
                return False

            if not incident["rescued"]:
                self.log_violation(agent, action, "Cannot treat before rescue")
                return False

            if incident["assigned_medic"] != agent.unique_id:
                self.log_violation(agent, action, "Medic not assigned to this incident")
                return False

        return True

    def log_violation(self, agent, action, reason):
        self.model.violation_count += 1
        print(
            f"VIOLATION | Agent {agent.unique_id} ({agent.role_name}) "
            f"tried '{action}' → {reason}"
        )
        
class MoiseLikeOrganization:
    """
    Very simple MOISE-like organization layer.

    MOISE+ idea:
    - Structural: roles
    - Functional: missions
    - Deontic: permissions / obligations

    Here we implement only:
    - roles
    - missions
    - permissions
    """

    def __init__(self):
        self.roles = {
            "Explorer": {
                "mission": "ExploreRange",
                "permissions": {"guess", "report"},
            },
            "Aggregator": {
                "mission": "AggregateReports",
                "permissions": {"receive_report", "aggregate", "broadcast"},
            },
            "Verifier": {
                "mission": "VerifyResult",
                "permissions": {"verify"},
            },
        }

    def get_mission(self, role_name):
        return self.roles[role_name]["mission"]

    def is_allowed(self, role_name, action):
        permissions = self.roles[role_name]["permissions"]
        return action in permissions

    def describe(self):
        print("\nMOISE-like Organization")
        print("-----------------------")
        for role, data in self.roles.items():
            print(f"Role: {role}")
            print(f"  Mission: {data['mission']}")
            print(f"  Permissions: {sorted(data['permissions'])}")
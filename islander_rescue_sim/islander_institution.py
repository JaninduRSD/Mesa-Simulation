class Message:
    def __init__(self, sender, receiver, performative, content):
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content


class Scene:
    """
    ISLANDER-like scene.

    A scene defines:
    - participating roles
    - allowed message types
    - protocol rules for communication
    """

    def __init__(self, name, allowed_messages):
        self.name = name
        self.allowed_messages = allowed_messages

    def is_allowed(self, message):
        sender_role = message.sender.role_name
        receiver_role = message.receiver.role_name
        performative = message.performative

        rule = (sender_role, receiver_role, performative)

        return rule in self.allowed_messages


class IslanderInstitution:
    """
    Simple ISLANDER-like institution.

    ISLANDER idea:
    - Agents play roles.
    - Interactions happen inside scenes.
    - Each scene has a protocol.
    - Only allowed messages can be sent in each scene.
    - The institution controls scene transitions.
    """

    def __init__(self, model):
        self.model = model
        self.current_scene_name = "discovery"
        self.violation_count = 0

        self.scenes = {
            "discovery": Scene(
                "discovery",
                allowed_messages={
                    ("Scout", "Coordinator", "report_incident"),
                },
            ),

            "assignment": Scene(
                "assignment",
                allowed_messages={
                    ("Coordinator", "Rescuer", "assign_rescue"),
                },
            ),

            "rescue": Scene(
                "rescue",
                allowed_messages={
                    ("Rescuer", "Coordinator", "rescue_done"),
                },
            ),

            "treatment_assignment": Scene(
                "treatment_assignment",
                allowed_messages={
                    ("Coordinator", "Medic", "assign_treatment"),
                },
            ),

            "treatment": Scene(
                "treatment",
                allowed_messages={
                    ("Medic", "Coordinator", "treatment_done"),
                },
            ),

            "verification": Scene(
                "verification",
                allowed_messages={
                    ("Coordinator", "Coordinator", "verify_all"),
                },
            ),
        }

    @property
    def current_scene(self):
        return self.scenes[self.current_scene_name]

    def send_message(self, message):
        """
        Checks if a message is allowed in the current scene.
        If allowed, deliver it.
        If not allowed, log a protocol violation.
        """

        if self.current_scene.is_allowed(message):
            message.receiver.inbox.append(message)
            print(
                f"VALID MESSAGE | Scene={self.current_scene_name} | "
                f"{message.sender.role_name} -> {message.receiver.role_name}: "
                f"{message.performative}"
            )
            return True

        self.violation_count += 1
        self.model.violation_count += 1

        print(
            f"PROTOCOL VIOLATION | Scene={self.current_scene_name} | "
            f"{message.sender.role_name} -> {message.receiver.role_name}: "
            f"{message.performative} is not allowed"
        )

        return False

    def transition_scene(self):
        """
        Very simple scene flow.

        In real ISLANDER, the performative structure defines
        valid scene transitions. Here we implement the basic version.
        """

        if self.current_scene_name == "discovery":
            self.current_scene_name = "assignment"

        elif self.current_scene_name == "assignment":
            self.current_scene_name = "rescue"

        elif self.current_scene_name == "rescue":
            self.current_scene_name = "treatment_assignment"

        elif self.current_scene_name == "treatment_assignment":
            self.current_scene_name = "treatment"

        elif self.current_scene_name == "treatment":
            self.current_scene_name = "verification"

        elif self.current_scene_name == "verification":
            self.current_scene_name = "discovery"

    def describe(self):
        print("\nISLANDER-like Electronic Institution")
        print("------------------------------------")
        print(f"Current scene: {self.current_scene_name}")

        for scene_name, scene in self.scenes.items():
            print(f"\nScene: {scene_name}")
            for rule in scene.allowed_messages:
                sender, receiver, performative = rule
                print(f"  {sender} -> {receiver}: {performative}")
                
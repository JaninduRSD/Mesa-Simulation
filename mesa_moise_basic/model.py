from mesa import Agent, Model

from organization import MoiseLikeOrganization


class BaseAgent(Agent):
    def __init__(self, model, role_name):
        super().__init__(model)
        self.role_name = role_name
        self.mission = model.organization.get_mission(role_name)

    def allowed(self, action):
        return self.model.organization.is_allowed(self.role_name, action)


class ExplorerAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Explorer")
        self.low = 1
        self.high = model.max_number
        self.guess = None
        self.done = False

    def step(self):
        if self.done:
            return

        if not self.allowed("guess"):
            print(f"Explorer {self.unique_id} is not allowed to guess.")
            return

        self.guess = self.random.randint(self.low, self.high)

        if self.guess == self.model.target_number:
            self.done = True
            print(f"Explorer {self.unique_id} guessed correctly: {self.guess}")

        elif self.guess < self.model.target_number:
            self.low = self.guess + 1

        else:
            self.high = self.guess - 1

        if self.allowed("report"):
            report = {
                "agent_id": self.unique_id,
                "low": self.low,
                "high": self.high,
                "guess": self.guess,
                "done": self.done,
            }
            self.model.reports.append(report)
            print(
                f"Explorer {self.unique_id} reports: "
                f"guess={self.guess}, range={self.low}-{self.high}"
            )


class AggregatorAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Aggregator")
        self.global_low = 1
        self.global_high = model.max_number

    def step(self):
        if not self.allowed("aggregate"):
            print("Aggregator is not allowed to aggregate.")
            return

        if len(self.model.reports) == 0:
            return

        lows = [report["low"] for report in self.model.reports]
        highs = [report["high"] for report in self.model.reports]

        self.global_low = max([self.global_low] + lows)
        self.global_high = min([self.global_high] + highs)

        print(
            f"Aggregator updates shared range: "
            f"{self.global_low}-{self.global_high}"
        )

        if self.allowed("broadcast"):
            for agent in self.model.agents:
                if isinstance(agent, ExplorerAgent) and not agent.done:
                    agent.low = self.global_low
                    agent.high = self.global_high

            print("Aggregator broadcasts shared range to explorers.")

        self.model.reports.clear()


class VerifierAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Verifier")

    def step(self):
        if not self.allowed("verify"):
            print("Verifier is not allowed to verify.")
            return

        explorers = [
            agent for agent in self.model.agents
            if isinstance(agent, ExplorerAgent)
        ]

        if all(agent.done for agent in explorers):
            self.model.completed = True
            print("Verifier: all explorers found the target.")


class GuessingGameModel(Model):
    def __init__(self, num_explorers=3, max_number=20, seed=None):
        super().__init__(seed=seed)

        self.max_number = max_number
        self.target_number = self.random.randint(1, max_number)

        self.organization = MoiseLikeOrganization()
        self.reports = []
        self.completed = False
        self.step_count = 0

        for _ in range(num_explorers):
            ExplorerAgent(self)

        AggregatorAgent(self)
        VerifierAgent(self)

    def step(self):
        self.step_count += 1

        print("\n==============================")
        print(f"Step {self.step_count}")
        print(f"Target number is hidden.")
        print("==============================")

        # 1. Explorers act first
        for agent in list(self.agents):
            if isinstance(agent, ExplorerAgent):
                agent.step()

        # 2. Aggregator acts second
        for agent in list(self.agents):
            if isinstance(agent, AggregatorAgent):
                agent.step()

        # 3. Verifier acts last
        for agent in list(self.agents):
            if isinstance(agent, VerifierAgent):
                agent.step()
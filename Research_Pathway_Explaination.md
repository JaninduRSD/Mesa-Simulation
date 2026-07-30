# Simulation-Informed Prediction of Emergent Behaviour in Multi-Agent Systems

## 1. Proposed research title

> **Simulation-Informed Regression for Pre-Deployment Prediction of Emergent Coordination Behaviour in Multi-Agent Systems**

This project uses inexpensive multi-agent simulations to build and test a quantitative prediction model. The model estimates whether a proposed multi-agent system is likely to complete a task successfully before an expensive real LLM-based system is deployed.

---

## 2. Possible Methodology

The research can follow this process:

```text
Natural-language task supplied by the user
                ↓
Task converted into a structured workflow
                ↓
OperA/ISLANDER simulations run inexpensively
                ↓
Agent, budget and coordination measurements collected
                ↓
Regression learns relationships from many simulations
                ↓
New MAS configuration entered
                ↓
Predicted success probability and explanation returned
```

The β coefficients in the new equation are not guessed and are not copied from the original agent-scaling paper. They are learned from the new simulation dataset.

---



## 3. Why this research is needed



## 3.1 The practical problem

LLM-based multi-agent experiments can be expensive because they require:

- many API calls;
- multiple agents per task;
- repeated test instances;
- large token budgets;
- tool calls;
- several random repetitions;
- different models and team configurations.

For example, testing 200 configurations with several agents and 20 repetitions could require thousands of LLM executions. This may not be financially practical for a BSc project.

Mesa simulations provide an inexpensive alternative. They allow the researcher to vary:

- number of agents;
- capability of each agent;
- role assignment;
- task difficulty;
- budget;
- communication;
- failure probability;
- organizational framework.

The simulation can be run thousands of times locally without paying for LLM API usage.

## 3.2 What the original agent-scaling research achieved

Kim et al.’s paper, published as *Capable Language Models Can Outgrow the Benefits of Collaboration*, evaluates:

- a Single-Agent System;
- Independent MAS;
- Centralized MAS;
- Decentralized MAS;
- Hybrid MAS;
- several LLM families;
- six agentic benchmarks.

It fits a regression model relating configuration-level task performance to variables including:

- model capability;
- tool count;
- agent count;
- single-agent baseline;
- coordination overhead;
- message density;
- redundancy;
- coordination efficiency;
- error amplification;
- interaction terms.

The paper is important because it shows that adding agents does not automatically improve performance. Coordination can help, but it can also introduce overhead, duplication and error propagation.

## 3.3 Research gaps addressed by this project

This project focuses on four limitations.

### Gap 1 — Agent asymmetry is not part of the main regression

The main scaling equation does not directly represent a team such as:

```text
One powerful Coordinator
Two medium-capability specialists
Three weaker reviewing agents
```

It does not explicitly model:

- different capabilities among team members;
- capability variance;
- whether the best agent receives the correct role;
- whether a weak agent is placed in a critical position.

The repository contains a separate heterogeneous-agent analysis, but heterogeneity is not integrated into the main 19-predictor regression.

### Gap 2 — Token budget is controlled, not modelled

The paper controls reasoning budgets so architectures can be compared fairly. This is scientifically reasonable, but budget is not varied as an independent predictor in the main model.

Therefore, the model cannot directly predict:

- what happens when the total budget changes;
- what happens when one budget is divided among more agents;
- how much budget is spent on communication;
- whether agents receive insufficient individual budgets;
- whether a larger team wastes its budget through coordination.



### Gap 3 — Coordination values are fixed by architecture

In the repository, values such as coordination overhead, message density, redundancy, efficiency and error amplification are stored as one lookup entry per architecture.

For example, the same Centralized overhead value is applied regardless of:

- whether there are four agents or ten agents;
- whether the task is easy or difficult;
- whether communication is short or extensive;
- whether agents are homogeneous or heterogeneous;
- whether the token budget is small or large.

This is a major opportunity for improvement. In the proposed work, coordination measurements will be calculated separately for every simulated configuration.

### Gap 4 — Task structure is represented incompletely

The original regression includes tool count and single-agent baseline. The single-agent baseline represents part of task difficulty, but these inputs do not fully describe:

- whether the task can be divided;
- how sequential it is;
- how many independent subtasks exist;
- whether agents share state;
- how much communication is required;
- whether one failure affects later stages.

Two tasks can use the same number of tools while having completely different structures.

## 3.4 Final research gap statement

> Existing agent-scaling regression provides useful evidence about LLM-agent coordination, but its main model does not jointly represent heterogeneous agent capability, variable budget allocation, configuration-specific coordination measurements and structural task characteristics. Running sufficient LLM experiments to estimate these effects is financially difficult. Therefore, this research investigates whether enhanced organizational simulations can generate controlled quantitative data for building and evaluating an extended, simulation-informed emergence-prediction model.

---



## 4. What “emergent behaviour” means

Emergent behaviour is a system-level outcome produced by many local agent decisions and interactions. No single agent directly controls the complete outcome.

## 4.1 Beneficial emergence

Examples include:

- agents divide work successfully;
- several agents complete independent subtasks in parallel;
- specialists correct errors made by weaker agents;
- communication improves the final decision;
- the team completes the task within the deadline;
- the team uses less budget than expected.



## 4.2 Harmful emergence

Examples include:

- the Coordinator becomes overloaded;
- agents repeat the same work;
- communication consumes too much budget;
- a weak agent’s mistake spreads to later stages;
- many agents wait for one slow role;
- the team runs out of budget;
- the task is not completed within the deadline.



## 4.3 How emergence is measured in this project

The primary outcome is:

```text
Did the MAS complete the task correctly within its deadline and budget?
```

For one simulation run:

```text
Success = 1
Failure = 0
```

For one configuration repeated 20 times:

```text
Observed success probability P =
Number of successful runs
─────────────────────────
20
```

Example:

```text
Successful runs = 15
Total runs      = 20

P = 15 / 20 = 0.75
```

The configuration therefore has an observed simulated success probability of 75%.

Secondary measurements include:

- completion time;
- budget consumed;
- coordination overhead;
- message density;
- redundancy;
- error amplification;
- maximum queue size;
- number of protocol or norm violations.

---



## 5. Correct scope of the research

The proposed model predicts the behaviour of the enhanced simulations.

It does not immediately prove that a real LLM system will have exactly the same success probability.

A correct claim is:

> The model predicts emergence and performance within the tested organizational simulation space and identifies whether the proposed additional variables improve held-out simulation prediction.

An incorrect claim is:

> The model is guaranteed to predict every real LLM-based multi-agent system.

Real LLM experiments would eventually be required for external validation. That can be future work.

---



## 6. Which simulations should be used?



## 6.1 Primary simulation — ISLANDER

Relevant files:

- `Mesa-Simulation/islander_rescue_sim/islander_institution.py`
- `Mesa-Simulation/islander_rescue_sim/model.py`
- `Mesa-Simulation/islander_rescue_sim/agents.py`

ISLANDER is the best primary simulation because it has explicit messages and interaction scenes.

Its current workflow contains:

```text
Discovery
    ↓
Rescue assignment
    ↓
Rescue
    ↓
Treatment assignment
    ↓
Treatment
    ↓
Verification
```

The institution checks whether each message is permitted in the current scene.

This makes it suitable for measuring:

- number of messages;
- communication cost;
- message density;
- protocol violations;
- communication delay;
- scene-level bottlenecks;
- downstream effects of lost or incorrect messages.



## 6.2 Comparison simulation — OperA

Relevant files:

- `Mesa-Simulation/opera_rescue_sim/opera_organization.py`
- `Mesa-Simulation/opera_rescue_sim/model.py`
- `Mesa-Simulation/opera_rescue_sim/agents.py`

OperA uses:

- role contracts;
- permitted actions;
- norms;
- violation checking;
- direct shared-state changes.

It models the same broad rescue process as ISLANDER, making a matched comparison possible.

The comparison can investigate:

```text
OperA:
Action- and norm-controlled organization

ISLANDER:
Message- and scene-controlled organization
```



## 6.3 Why MOISE+ is not the primary simulation

The current MOISE+-inspired code models a number-guessing game. It is useful for studying collaborative search and information aggregation, but it is a different domain from the rescue workflow.

Using raw completion time to compare the guessing game against rescue would mix:

- organizational differences;
- task-domain differences.

MOISE+ can be:

- excluded from the main experiment; or
- used as a small supporting case study.

For a manageable BSc scope, ISLANDER and OperA are sufficient.

---



## 7. How the simulations should be improved

The current simulations are educational demonstrations. They need several controlled extensions before they can generate useful regression data.

## 7.1 Convert the rescue domain into a generic workflow

The simulator should represent a task as several connected subtasks.

Each subtask should contain:

```text
Subtask ID
Required role
Difficulty
Compute cost
Dependencies
Whether it reads or modifies shared state
Completion status
```

Example:

```text
Subtask 1: Read insurance claim
Required role: Reviewer
Difficulty: 0.40
Cost: 10 units
Dependencies: None

Subtask 2: Inspect suspicious evidence
Required role: Specialist
Difficulty: 0.70
Cost: 20 units
Dependencies: Subtask 1

Subtask 3: Produce final decision
Required role: Coordinator
Difficulty: 0.60
Cost: 15 units
Dependencies: Subtasks 1 and 2
```

This allows natural-language tasks to be converted into a common simulation format.

## 7.2 Add heterogeneous capability

Every agent receives:

- general capability;
- role-specific capability;
- action-success probability;
- assigned role.

Example:

```text
Reviewer 1 capability: 0.80
Reviewer 2 capability: 0.75
Reviewer 3 capability: 0.60
Specialist capability: 0.90
Coordinator capability: 0.85
```

When an agent performs a subtask, success depends on:

- agent capability;
- subtask difficulty;
- role match.

A simple simulation rule can be:

```text
Action success probability =
Agent role-specific capability × (1 − 0.5 × task difficulty)
```

Example:

```text
Agent capability = 0.80
Task difficulty  = 0.60

Action probability
= 0.80 × (1 − 0.5 × 0.60)
= 0.80 × 0.70
= 0.56
```

This is a modelling assumption. It must be documented and tested through different parameter settings.

## 7.3 Add budget accounting

Because the simulation does not use actual LLM tokens, the initial research should call the budget:

```text
Compute-unit budget
```

Example costs:

```text
Read task information:      5 units
Perform normal action:     10 units
Perform specialist action: 20 units
Send message:               2 units
Assign work:                3 units
Verify result:              8 units
Repeat failed action:      Original action cost again
```

Each configuration receives:

```text
Total budget B
```

The system records:

- budget spent on task work;
- budget spent on communication;
- budget spent on repeated work;
- remaining budget;
- whether the task failed because the budget ended.



## 7.4 Add variable agent counts

The experiment should vary:

- number of normal workers;
- number of specialists;
- number of Coordinators;
- total number of agents.

Example:

```text
Small team:
2 workers + 1 specialist + 1 Coordinator

Medium team:
4 workers + 2 specialists + 1 Coordinator

Large team:
8 workers + 3 specialists + 2 Coordinators
```

Coordination values are recalculated for every team. They are not fixed based only on the framework name.

## 7.5 Add communication delay and failure

ISLANDER messages can be assigned:

- compute cost;
- delivery delay;
- loss probability;
- corruption probability.

Example:

```text
Message delay: 1 simulation step
Message-loss probability: 0.05
Incorrect-message probability: 0.02
```



## 7.6 Add structured data collection

Every run should record:

- task profile;
- agent configuration;
- budget configuration;
- framework;
- actions;
- messages;
- duplicate actions;
- initial errors;
- downstream errors;
- completion;
- total steps;
- final success.

These results should be exported to CSV.

---



## 8. How a natural-language task enters the system



## 8.1 The task must be supplied first

The model does not invent the task.

The user supplies a description such as:

> Review 100 insurance claims. Three agents independently inspect claim documents, one specialist checks suspicious claims, and one Coordinator combines the findings. All claims must be completed within a fixed budget.



## 8.2 Natural language cannot go directly into the equation

The equation requires numbers. Therefore, the task must pass through a task profiler.

For a BSc project, this should be a structured form rather than another complex language model.

The form asks:

```text
How many subtasks exist?
Which subtasks can run independently?
Which subtasks depend on previous work?
Which roles are required?
How difficult is each subtask?
What is the total budget?
What is the deadline?
How much communication is required?
Does the task modify shared state?
```



## 8.3 Example structured profile

From the insurance task:

```text
Task load:                   100 claims
Normal reviewers:              3
Specialists:                   1
Coordinators:                  1
Total agents:                  5
Organization:        Centralized
Total budget:             10,000 compute units
Maximum steps:               100
Suspicious-claim rate:       20%
Normal review cost:            10 units
Specialist review cost:        20 units
Message cost:                   2 units
```

Agent capabilities must also be supplied as assumptions:

```text
Reviewer 1:   0.80
Reviewer 2:   0.75
Reviewer 3:   0.60
Specialist:   0.90
Coordinator:  0.85
```

These values may come from:

- historical agent performance, if available;
- developer estimates;
- controlled low/medium/high scenarios;
- later real-system calibration.

When no empirical measurements exist, they must be described as simulation assumptions—not factual LLM capability scores.

---



## 9. Variables in the proposed model

The following variables are designed to address the identified limitations.

## 9.1 Agent count: nₐ

```text
nₐ = Total number of agents
```

Because adding agents often has diminishing effects, the model uses:

```text
log(1 + nₐ)
```

Example:

```text
nₐ = 5
log(1 + nₐ) = log(6)
```



## 9.2 Mean agent capability: q̄

```text
q̄ =
Sum of general agent capabilities
─────────────────────────────────
Number of agents
```

Example:

```text
Capabilities = [0.80, 0.75, 0.60, 0.90, 0.85]

q̄ = 3.90 / 5 = 0.78
```



## 9.3 Capability asymmetry: s_q

Capability asymmetry is measured using the standard deviation of agent capabilities.

```text
s_q = Standard deviation of agent capabilities
```

Interpretation:

```text
s_q close to 0:
Agents have similar capability

Large s_q:
The team contains strong and weak agents
```

Asymmetry is not automatically harmful. A heterogeneous team may perform well if agents receive suitable roles.

## 9.4 Role-fit score: F_role

Each agent has a capability for its assigned role.

```text
F_role =
Sum of assigned-role capabilities
─────────────────────────────────
Number of agents
```

Example:

```text
Strong specialist assigned to specialist role: high role fit
Weak reviewer assigned as final Coordinator: low role fit
```

This separates heterogeneity from poor role assignment.

## 9.5 Budget per agent: b

```text
b = Total budget / Number of agents
```

Example:

```text
Total budget = 10,000 units
Agents       = 5

b = 10,000 / 5 = 2,000 units per agent
```



### Why total budget is not included separately

If the equation contains:

- agent count;
- total budget;
- budget per agent;

then one variable is mathematically derived from the other two:

```text
Budget per agent = Total budget / Agent count
```

Including all three can cause multicollinearity. The primary equation therefore uses:

- agent count;
- budget per agent.

Total budget remains part of the simulator configuration and output report.

## 9.6 Simulated baseline performance: P_base

Run a simple baseline configuration on the same task:

- one all-rounder agent; or
- the smallest valid team without advanced coordination.

Repeat it using several seeds:

```text
P_base =
Successful baseline runs
────────────────────────
Total baseline runs
```

This provides a simulation-based measurement of basic task difficulty.

Unlike tool count, it captures whether the simulated task is easy or difficult for the baseline system.

The original-style comparison model may also include:

```text
T_action = Number of distinct action or tool types available in the workflow
```

For the insurance example, action types might include:

```text
Read document
Search evidence
Send report
Assign specialist
Verify decision
```

This variable is retained only to compare the extended task representation against a simpler tool-count-style representation.

## 9.7 Task decomposability: D

Decomposability measures how much work can be assigned independently.

A simple definition is:

```text
D =
Subtasks that can be delegated without shared-state dependency
──────────────────────────────────────────────────────────────
Total subtasks
```

Example:

```text
80 of 100 insurance claims can be reviewed independently

D = 80 / 100 = 0.80
```



## 9.8 Task sequentiality: S

Sequentiality measures how much of the workflow lies on a dependency chain.

```text
S =
Number of subtasks on the longest dependency path
─────────────────────────────────────────────────
Total subtasks
```

Example:

```text
Read claim → Specialist review → Final decision
```

A task with long dependency chains has high sequentiality. A task containing many independent cases has lower sequentiality.

Decomposability and sequentiality should be checked for strong correlation before fitting the final model.

## 9.9 Task load: L

```text
L = Number of subtasks or work items
```

Examples:

```text
100 insurance claims
50 customer-support tickets
200 documents
```

The value may be log-transformed if it covers a wide range:

```text
log(1 + L)
```



## 9.10 Coordination overhead: O

Coordination overhead is calculated for each simulated configuration:

```text
O =
Compute units spent on coordination
───────────────────────────────────
Total compute units spent
```

Coordination includes:

- messages;
- reports;
- assignments;
- broadcasts;
- synchronization;
- verification.

Example:

```text
Coordination cost = 2,700 units
Total cost        = 10,000 units

O = 2,700 / 10,000 = 0.27
```

The configuration has 27% coordination overhead.

## 9.11 Message density: c

```text
c =
Total delivered messages
────────────────────────
Agent count × Simulation steps
```

Example:

```text
Messages = 200
Agents   = 5
Steps    = 50

c = 200 / (5 × 50) = 0.80
```



## 9.12 Redundancy: R

```text
R =
Duplicate or repeated task actions
──────────────────────────────────
Total task actions
```

Example:

```text
Duplicate reviews = 20
Total reviews     = 150

R = 20 / 150 = 0.133
```



## 9.13 Error amplification: Aₑ

Error amplification measures whether one initial error creates additional downstream failures.

```text
Aₑ =
Downstream failures attributable to injected initial errors
──────────────────────────────────────────────────────────
Number of injected initial errors
```

Example:

```text
Initial errors    = 10
Downstream errors = 15

Aₑ = 15 / 10 = 1.5
```

An Aₑ above 1 means errors are being amplified.

To estimate this safely, pilot simulations should deliberately inject a known number of initial errors.

## 9.14 Framework indicator: F

For two frameworks:

```text
F = 0 for OperA
F = 1 for ISLANDER
```

The coefficient shows the average framework difference after controlling for other measured properties.

## 9.15 Coordination efficiency as an output

Coordination efficiency can be reported as:

```text
E_c =
Successfully completed subtasks
───────────────────────────────
Total compute units
```

It should initially be treated as a secondary output rather than a predictor of success because its numerator already includes successful completion. Using it to predict success could create circularity.

---



## 10. The proposed equation

Because the primary outcome is a probability, logistic regression is used.

## 10.1 Linear score

For configuration j:

```text
z_j =
β₀
+ β₁ log(1 + nₐ,j)
+ β₂ q̄_j
+ β₃ s_q,j
+ β₄ F_role,j
+ β₅ b_j
+ β₆ P_base,j
+ β₇ D_j
+ β₈ S_j
+ β₉ log(1 + L_j)
+ β₁₀ O_j
+ β₁₁ c_j
+ β₁₂ R_j
+ β₁₃ Aₑ,j
+ β₁₄ F_j
```



## 10.2 Convert score into probability

```text
P̂_j = 1 / (1 + e^(−z_j))
```

This ensures:

```text
0 ≤ P̂_j ≤ 1
```

Example output:

```text
P̂ = 0.76
```

means:

```text
Predicted success probability = 76%
```



## 10.3 Why this equation is only a starting specification

The final model may contain fewer variables.

After collecting data, variables may be removed when:

- two variables are nearly identical;
- a variable has almost no variation;
- a variable creates strong multicollinearity;
- a simpler model predicts held-out data equally well;
- measurement is unreliable.

The goal is not to force all variables into the equation. The goal is to test whether the proposed additions improve prediction.

---



## 11. How the β coefficients are derived



## 11.1 β values are learned, not manually selected

Suppose the simulator produces:

```text
Configuration 1:
Inputs X₁
Observed successes: 18/20

Configuration 2:
Inputs X₂
Observed successes: 7/20

Configuration 3:
Inputs X₃
Observed successes: 14/20
```

Regression software searches for β values that make the predicted probabilities close to the observed outcomes across all training configurations.

## 11.2 Maximum likelihood in simple terms

For every configuration, the model predicts a probability.

If a configuration succeeded in 18 of 20 runs, a prediction near 0.90 is more believable than a prediction of 0.20.

Maximum-likelihood estimation chooses the β values that make the complete observed dataset as probable as possible.

The researcher does not calculate every coefficient manually.

Python libraries such as `statsmodels` or `scikit-learn` calculate them.

## 11.3 Interpreting coefficients



### Positive coefficient

```text
β > 0
```

means increasing the predictor is associated with higher predicted success, while other variables are held constant.

### Negative coefficient

```text
β < 0
```

means increasing the predictor is associated with lower predicted success.

### Example

```text
β for role fit = +0.80
```

suggests better role assignment is associated with higher success.

```text
β for overhead = −1.20
```

suggests higher coordination overhead is associated with lower success.

For logistic regression, exponentiating a coefficient gives an odds ratio:

```text
Odds ratio = e^β
```



## 11.4 Standardizing predictors

Variables use different scales:

```text
Capability:       0–1
Task load:        10–1,000
Budget per agent: hundreds or thousands
```

Continuous predictors should be standardized using the training data:

```text
Standardized value =
Value − Training mean
─────────────────────
Training standard deviation
```

The same training means and standard deviations must be used when predicting test and future configurations.

---



## 12. How the simulation dataset is created



## 12.1 Configuration factors

A manageable BSc experiment can vary:

```text
Framework:
OperA, ISLANDER

Agent count:
4, 6, 8, 10

Capability pattern:
Homogeneous-high
Homogeneous-medium
Heterogeneous-good-role-fit
Heterogeneous-poor-role-fit

Budget level:
Low, medium, high

Task load:
50, 100, 200

Decomposability:
Low, medium, high

Sequentiality:
Low, medium, high
```

Not every possible combination must be used. Select approximately 150–250 representative configurations.

## 12.2 Repeated seeds

Each configuration should be run using approximately 20 random seeds.

Example:

```text
200 configurations × 20 seeds
= 4,000 simulation runs
```

This is computationally manageable because the agents are simulated rather than real LLMs.

## 12.3 Why repeated seeds are needed

One run may succeed because of random chance.

Repeated seeds estimate:

- expected success probability;
- variation;
- robustness;
- rare failures.



## 12.4 Pilot and evaluation runs

Coordination overhead, message density, redundancy and error amplification are not available from the natural-language task alone.

Use:

```text
5 pilot seeds:
Estimate O, c, R and Aₑ

15 evaluation seeds:
Measure final success outcome
```

This prevents the same successful outcomes from being used both to construct the predictors and to evaluate them.

At prediction time, a new configuration undergoes a few inexpensive pilot simulations before the regression produces the final probability.

## 12.5 What one regression row contains

The regression dataset should contain one summarized row per configuration.

Example:

```text
configuration_id:          104
framework:                 ISLANDER
agent_count:               5
mean_capability:           0.78
capability_asymmetry:      0.11
role_fit:                  0.82
budget_per_agent:          2,000
baseline_performance:      0.58
decomposability:           0.80
sequentiality:             0.25
task_load:                 100
coordination_overhead:     0.27
message_density:           0.80
redundancy:                0.13
error_amplification:       1.30
evaluation_successes:      11
evaluation_trials:         15
observed_performance:      0.733
```

The first group of columns contains predictors. The final columns contain the outcome observed in the separate evaluation seeds.

## 12.6 How the software fits the equation

There are two simple implementation choices.

### Choice A — One row per configuration

Store:

```text
Number of successes
Number of trials
All predictor values
```

Fit a binomial generalized linear model using the successes and failures.

### Choice B — One row per evaluation run

Repeat the configuration inputs for each evaluation seed:

```text
Run 1: Success = 1
Run 2: Success = 0
Run 3: Success = 1
```

Fit ordinary logistic regression while ensuring all runs from the same configuration remain in the same training or test group.

Choice A is more compact. Choice B may be easier with common machine-learning libraries. Both estimate the same type of success relationship when implemented correctly.

Conceptual Python structure:

```python
X = data[predictor_columns]
y = data["success"]

model.fit(X_train, y_train)

beta_0 = model.intercept_
beta_values = model.coef_
```

The actual implementation should use a pipeline so standardization is learned from training data only.

## 12.7 What the simulations show before regression

The simulations provide useful findings even before fitting the prediction equation.

They can show:

- whether overhead rises when more agents are added;
- whether low budget per agent creates a failure threshold;
- whether heterogeneous teams outperform homogeneous teams;
- whether good role assignment makes heterogeneity beneficial;
- whether decomposable tasks benefit from larger teams;
- whether sequential tasks create waiting and bottlenecks;
- whether ISLANDER prevents invalid communication at additional cost;
- whether OperA completes work with lower communication but different norm risks;
- whether one initial error creates several downstream errors.

These results should first be presented using simple plots and averages. The regression then tests whether the same measured properties can predict unseen configurations.

---



## 13. Model-building stages

The research should not fit only one large equation. It should compare models in stages.

### Model A — Original-style baseline

```text
Success ~
log(agent count)
+ simulated baseline performance
+ action/tool-type count
+ framework
```

This approximates the simpler information available in the original scaling approach.

### Model B — Add asymmetric agents

```text
Model A
+ mean capability
+ capability asymmetry
+ role-fit score
```

This tests whether heterogeneity improves prediction.

### Model C — Add budget

```text
Model B
+ budget per agent
```

This tests whether budget allocation improves prediction.

### Model D — Add task structure

```text
Model C
+ decomposability
+ sequentiality
+ task load
```

This tests whether task structure is more informative than tool/action count alone.

### Model E — Add configuration-specific coordination

```text
Model D
+ coordination overhead
+ message density
+ redundancy
+ error amplification
```

This is the complete simulation-informed candidate model.

---



## 14. Optional interaction terms

Only a small number of theoretically meaningful interactions should be tested.

## 14.1 Agent count × budget per agent

```text
log(1 + nₐ) × b
```

This tests whether adding agents helps only when every agent retains sufficient budget.

## 14.2 Asymmetry × role fit

```text
s_q × F_role
```

This tests whether heterogeneous teams work well when strong and weak agents are assigned appropriately.

## 14.3 Agent count × decomposability

```text
log(1 + nₐ) × D
```

This tests whether larger teams help more on divisible tasks.

## 14.4 Overhead × budget per agent

```text
O × b
```

This tests whether communication overhead is especially harmful under small budgets.

The interaction model should be compared against the simpler main-effects model. Interactions should be removed when they do not improve held-out prediction.

---



## 15. Training and testing



## 15.1 Configuration-level split

Use:

```text
80% configurations for training
20% configurations for final testing
```

All seeds belonging to one configuration must remain together.

Incorrect split:

```text
Same configuration, seed 1 in training
Same configuration, seed 2 in testing
```

This would make testing too easy.

Correct split:

```text
All seeds for Configuration A in training
All seeds for Configuration B in testing
```



## 15.2 Stronger held-out test

The final test should include configurations not represented exactly in training, such as:

- unseen agent counts;
- unseen task loads;
- unseen capability combinations;
- unseen task profiles.

This better represents pre-deployment prediction.

## 15.3 Preventing preprocessing leakage

The following must be calculated using training data only:

- standardization means;
- standard deviations;
- variable selection;
- decision thresholds.

The test set is used only after the model is finalized.

---



## 16. How the claim is proven

The claim is not proven by showing that the full model has a high training score.

The claim is supported when the extended models predict unseen configurations better than the baseline.

## 16.1 Main comparison

Compare Models A–E using the same held-out test set.

The additional variables are useful if:

```text
Model B outperforms Model A:
Evidence that heterogeneity matters

Model C outperforms Model B:
Evidence that budget allocation matters

Model D outperforms Model C:
Evidence that task structure matters

Model E outperforms Model D:
Evidence that dynamic coordination measurements matter
```



## 16.2 Evaluation measurements



### Brier score

Measures the squared difference between predicted probability and actual result.

```text
Lower is better
```



### Log loss

Penalizes confident incorrect probability predictions.

```text
Lower is better
```



### ROC-AUC

Measures the ability to rank successful configurations above unsuccessful ones.

```text
Higher is better
```



### Accuracy

Measures the fraction of correct success/failure classifications after selecting a threshold.

### Recall for failure

Measures how many truly failing configurations were detected.

This is important because incorrectly declaring a dangerous configuration safe is undesirable.

### Calibration

If configurations predicted at approximately 70% success actually succeed around 70% of the time, the probabilities are calibrated.

## 16.3 Example evidence

Hypothetical results:

```text
Model A Brier score: 0.24
Model B Brier score: 0.20
Model C Brier score: 0.17
Model D Brier score: 0.14
Model E Brier score: 0.12
```

These results would show progressive improvement.

They are examples only. The actual values must come from experiments.

## 16.4 Coefficient stability

Check whether important coefficient directions remain similar across:

- different random splits;
- OperA;
- ISLANDER;
- low- and high-load tasks.

Stable relationships provide stronger evidence than one fitted dataset.

## 16.5 Simple baseline

The model must also beat a naive predictor such as:

```text
Always predict the average training success rate
```

If the proposed equation cannot outperform this simple baseline, it is not practically useful.

---



## 17. Full example from natural language to output



## 17.1 Supplied task

> Review 100 insurance claims. Three agents independently inspect claim documents, one specialist checks suspicious claims, and one Coordinator combines the findings. All claims must be completed within a fixed budget.



## 17.2 Additional supplied assumptions

```text
Total budget:              10,000 compute units
Deadline:                     100 simulation steps
Suspicious-claim rate:         20%
Review cost:                   10 units
Specialist cost:               20 units
Message cost:                   2 units

Reviewer 1 capability:       0.80
Reviewer 2 capability:       0.75
Reviewer 3 capability:       0.60
Specialist capability:       0.90
Coordinator capability:      0.85
```



## 17.3 Derived pre-simulation values

```text
Agent count nₐ:               5
Mean capability q̄:         0.78
Capability asymmetry s_q:   calculated standard deviation
Role-fit score F_role:      calculated from assigned roles
Budget per agent b:         2,000 units
Task load L:                  100
Decomposability D:           0.80
Sequentiality S:             derived from workflow dependencies
Framework F:                    1 for ISLANDER
```



## 17.4 Pilot simulation values

Hypothetical pilot results:

```text
Simulated baseline P_base:  0.58
Coordination overhead O:    0.27
Message density c:          0.80
Redundancy R:               0.13
Error amplification Aₑ:     1.30
```



## 17.5 Equation calculation

The trained model inserts the standardized values:

```text
z =
β₀
+ β₁ log(1 + 5)
+ β₂(0.78)
+ β₃(s_q)
+ β₄(F_role)
+ β₅(2,000)
+ β₆(0.58)
+ β₇(0.80)
+ β₈(S)
+ β₉ log(1 + 100)
+ β₁₀(0.27)
+ β₁₁(0.80)
+ β₁₂(0.13)
+ β₁₃(1.30)
+ β₁₄(1)
```

Suppose the fitted equation returns:

```text
z = 1.15
```

Then:

```text
P̂ = 1 / (1 + e^(−1.15))
P̂ ≈ 0.76
```



## 17.6 Natural-language output

> **Predicted task-success probability: 76%.**
>
> Under the supplied assumptions, the ISLANDER-style agent team is likely to complete the insurance-claim workflow within its budget and deadline. The task is highly decomposable, so parallel claim review is beneficial. However, the pilot simulation indicates that approximately 27% of compute is spent on coordination. The principal risks are the weaker third Reviewer and error propagation from initial reviews into the final decision. The current role assignment is relatively suitable because the strongest specialist and Coordinator occupy critical roles.

The system can additionally report:

```text
Predicted success:              76%
Predicted failure risk:         24%
Pilot coordination overhead:    27%
Pilot redundancy:               13%
Pilot error amplification:      1.30
Likely bottleneck:               Coordinator or specialist stage
Prediction scope:                Within tested simulation ranges
```

The natural-language explanation does not require another LLM. It can be generated from a fixed template populated with:

- predicted probability;
- measured pilot metrics;
- likely queue bottleneck;
- largest positive model contributions;
- largest negative model contributions.

For a standardized logistic model, the contribution of predictor k to the linear score is:

```text
Contribution_k = β_k × standardized input_k
```

Large positive contributions support success. Large negative contributions indicate risks. These are statistical associations within the simulation model, not proof of real-world causation.

---



## 18. Expected research questions



## Primary research question

> Can an extended regression model trained on enhanced organizational simulations predict the success of unseen heterogeneous and budget-constrained MAS configurations better than an original-style baseline model?



## Secondary research questions

1. Does agent capability asymmetry improve prediction after controlling for average capability?
2. Does role fit determine whether asymmetric teams help or harm performance?
3. Does budget per agent improve prediction beyond agent count?
4. Do decomposability and sequentiality describe task behaviour better than action/tool count alone?
5. Do coordination overhead and error amplification change when agent count and budget change?
6. Do configuration-specific coordination measurements improve held-out predictions?
7. Are the observed relationships similar in OperA and ISLANDER?

---



## 19. Proposed hypotheses



### H1 — Heterogeneity

Capability asymmetry alone will not consistently improve success, but asymmetry combined with high role fit will be beneficial.

### H2 — Budget allocation

Increasing agent count without maintaining sufficient budget per agent will reduce success.

### H3 — Task decomposability

Larger teams will provide greater benefits on highly decomposable tasks than highly sequential tasks.

### H4 — Dynamic overhead

Coordination overhead will increase with agent count and communication requirements rather than remaining constant for one architecture.

### H5 — Extended model

The extended simulation-informed model will achieve better held-out probability prediction than the original-style baseline model.

---



## 20. Expected research contributions

The research can contribute:

1. an enhanced organizational simulation supporting heterogeneous agents;
2. explicit compute-budget accounting;
3. generic workflow task profiles;
4. configuration-specific coordination measurements;
5. a simulation-generated experimental dataset;
6. a fitted emergence-prediction equation;
7. quantitative comparison of baseline and extended models;
8. a beginner-friendly pre-deployment prediction prototype.

The novelty is the complete connection:

```text
Task description
→ Workflow representation
→ Organizational simulation
→ Dynamic coordination measurements
→ Extended regression
→ Pre-deployment probability and explanation
```

---



## 21. Implementation plan



### Phase 1 — Shared workflow representation

Create generic workflow subtasks with:

- role requirements;
- dependencies;
- difficulty;
- costs;
- shared state.



### Phase 2 — Agent model

Add:

- general capability;
- role-specific capability;
- failure probability;
- budget.



### Phase 3 — Frameworks

Adapt:

- ISLANDER as the primary message-based framework;
- OperA as the norm/action comparison.



### Phase 4 — Metrics

Record:

- messages;
- coordination actions;
- duplicate work;
- initial and downstream errors;
- budget;
- completion.



### Phase 5 — Batch experiments

Run:

- approximately 150–250 configurations;
- approximately 20 seeds each.



### Phase 6 — Regression

Fit Models A–E.

### Phase 7 — Evaluation

Use:

- held-out configurations;
- Brier score;
- log loss;
- ROC-AUC;
- failure recall;
- calibration.



### Phase 8 — Prototype

Create:

- task-profile input form;
- pilot simulation runner;
- natural-language result generator.

---



## 22. Suggested BSc timeline



### Weeks 1–2

- finalize task representation;
- finalize variables;
- define success and failure.



### Weeks 3–5

- refactor ISLANDER;
- add heterogeneous capability;
- add compute budgets.



### Weeks 6–7

- adapt OperA;
- add metrics and CSV export;
- test simulation rules.



### Weeks 8–9

- run pilot experiments;
- refine parameter ranges;
- generate the main dataset.



### Weeks 10–11

- fit Models A–E;
- evaluate held-out prediction;
- inspect coefficients.



### Weeks 12–13

- develop input/output prototype;
- create graphs and result explanations.



### Week 14

- complete thesis analysis;
- document limitations and future validation.

---



## 23. Risks and controls



## Risk 1 — Too many variables

Control:

- compare models in stages;
- remove highly correlated predictors;
- retain a smaller final model.



## Risk 2 — Subjective task scores

Control:

- define a written scoring rubric;
- calculate decomposability and sequentiality from workflow structure;
- report all assumptions.



## Risk 3 — Simulation does not represent real LLMs

Control:

- restrict claims to simulated MAS;
- discuss real LLM validation as future work;
- use the paper only as theoretical motivation.



## Risk 4 — Circular predictors

Control:

- do not use coordination efficiency as a primary success predictor;
- calculate coordination metrics from separate pilot seeds;
- measure target success on evaluation seeds.



## Risk 5 — Data leakage

Control:

- keep all seeds from one configuration together;
- standardize using training data only;
- protect the final test set.



## Risk 6 — Artificially easy testing

Control:

- hold out agent counts, workloads or task profiles;
- compare against the average-success baseline.

---



## 24. What the research does not require

The project does not require:

- paid large-scale LLM experiments;
- deep learning;
- reinforcement learning;
- dynamic topology routing;
- Bayesian calibration;
- complex causal modelling;
- a fully automatic natural-language parser.

The core work is:

- simulation engineering;
- controlled experiments;
- logistic regression;
- quantitative evaluation.

---



## 25. Final claim template

If the results support the hypotheses, the thesis can conclude:

> This study developed an enhanced organizational multi-agent simulation and a simulation-informed logistic regression model for pre-deployment prediction of emergent coordination outcomes. In held-out simulation configurations, incorporating agent heterogeneity, role fit, budget per agent, structural task characteristics and configuration-specific coordination measurements improved probability prediction compared with an original-style baseline using mainly agent count, action/tool count and baseline performance. The results demonstrate the value of simulation for studying otherwise expensive multi-agent scaling questions, while remaining limited to the validated simulation space until real LLM-agent data become available.

If the extended model does not outperform the baseline, that is still a valid research result:

> The additional simulated variables did not produce reliable held-out improvement under the tested conditions, suggesting that either the variables were not sufficiently informative or the simulator did not reproduce the relevant coordination mechanisms.

---



## 26. Final beginner-friendly summary

The user first provides a task and its operating assumptions. The task is converted into a workflow containing subtasks, roles, dependencies, difficulty and costs. A few inexpensive Mesa simulations estimate how much communication, duplication and error propagation the proposed team creates. A logistic regression then combines those measurements with agent count, capability differences, role fit, budget and task structure. It returns the probability that the proposed MAS will complete the task within its deadline and budget.

The model is created by running many simulation configurations and allowing regression software to learn the β coefficients. Its value is proven by predicting configurations that were not used for training and comparing the extended equation against simpler baseline models.

---



## 27. Supporting literature

[1] J. F. Hübner, J. S. Sichman and O. Boissier, “MOISE+: Towards a Structural, Functional, and Deontic Model for MAS Organization,” *Proceedings of AAMAS*, 2002. [DOI](https://doi.org/10.1145/544741.544858).

[2] V. Dignum, *A Model for Organizational Interaction: Based on Agents, Founded in Logic*, Utrecht University, 2004. [Record](http://hdl.handle.net/1874/890).

[3] M. Esteva, D. de la Cruz and C. Sierra, “ISLANDER: An Electronic Institutions Editor,” *Proceedings of AAMAS*, 2002. [DOI](https://doi.org/10.1145/545056.545069).

[4] V. Grimm et al., “A Standard Protocol for Describing Individual-Based and Agent-Based Models,” *Ecological Modelling*, 2006. [DOI](https://doi.org/10.1016/j.ecolmodel.2006.04.023).

[5] F. Klügl, “A Validation Methodology for Agent-Based Simulations,” *Proceedings of the ACM Symposium on Applied Computing*, 2008. [DOI](https://doi.org/10.1145/1363686.1363696).

[6] G. ten Broeke, G. van Voorn and A. Ligtenberg, “Which Sensitivity Analysis Method Should I Use for My Agent-Based Model?,” *Journal of Artificial Societies and Social Simulation*, 2016. [DOI](https://doi.org/10.18564/jasss.2857).

[7] G. ten Broeke, G. van Voorn, A. Ligtenberg and J. Molenaar, “The Use of Surrogate Models to Analyse Agent-Based Models,” *Journal of Artificial Societies and Social Simulation*, 2021. [DOI](https://doi.org/10.18564/jasss.4530).

[8] C. Angione, E. Silverman and E. Yaneske, “Using Machine Learning as a Surrogate Model for Agent-Based Simulations,” *PLOS ONE*, 2022. [DOI](https://doi.org/10.1371/journal.pone.0263150).

[9] Y. Kim et al., “Capable Language Models Can Outgrow the Benefits of Collaboration,” *Nature Machine Intelligence*, 2026. [DOI](https://doi.org/10.1038/s42256-026-01268-y). The earlier arXiv title is *Towards a Science of Scaling Agent Systems*.
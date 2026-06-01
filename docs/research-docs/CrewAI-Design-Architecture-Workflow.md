# CrewAI Design, Architecture, Workflow

## What It Is

CrewAI is a Python framework for building agent teams and structured agent workflows. Its important split is between deterministic orchestration and autonomous agent collaboration.

## Core Product Shape

- Agents have roles, goals, tools, and task responsibilities.
- Crews are teams of agents that collaborate on a complex task.
- Flows define stateful process structure and control flow.
- A Flow can call a Crew when autonomy is useful.

## Workflow Model

CrewAI's current docs frame the production model as:

1. A Flow starts from an event or process.
2. The Flow manages state and decides the next step.
3. A complex step can be delegated to a Crew.
4. Crew agents collaborate and return a result.
5. The Flow continues based on that result.

This is a useful separation: deterministic workflow outside, autonomous agents inside controlled steps.

## Architecture Notes

- A Flow is closer to application orchestration.
- A Crew is closer to a specialized agent team.
- Tools are attached to agents so capability stays close to role.
- Production use needs state, visibility, and control over where autonomy is allowed.

## Lessons For Spider Rose

- Keep Phase 1 agents simple, but plan a later split between workflow control and agent autonomy.
- A future Spider Rose workflow should be able to say: "run these deterministic steps, then ask this group of agents."
- Agent files should describe role, goal, tools, and output contract clearly enough to later compile into LangGraph or CrewAI-like runtime objects.
- Do not let every canvas edge imply full autonomy. Some edges should be deterministic data flow.

## What To Avoid

- Adding crews/groups before single-agent creation is clean.
- Adding a second agent definition format. Spider Rose should keep Markdown agents and LangGraph only.
- Treating all workflows as chat. Some workflows are structured jobs.

## Sources

- CrewAI Introduction: https://docs.crewai.com/en/introduction
- CrewAI Flows overview: https://www.crewai.com/crewai-flows

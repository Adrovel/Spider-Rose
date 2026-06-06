import {
  AgentDetailsPopover,
  AgentEditor,
  AgentPicker,
  FloatingAddButton,
  SidebarTabs,
  WorkflowCanvas
} from "./components.js";

export default {
  title: "Spider Rose/App Components"
};

export const SidebarAgentsTab = {
  render: () => SidebarTabs({ active: "agents" })
};

export const SidebarWorkflowTab = {
  render: () => SidebarTabs({ active: "workflow" })
};

export const AgentEditorPanel = {
  render: () => AgentEditor()
};

export const FixedDemoCanvas = {
  render: () => WorkflowCanvas()
};

export const FloatingPlus = {
  render: () => {
    const stage = document.createElement("main");
    stage.className = "sr-stage";
    stage.innerHTML = FloatingAddButton();
    return stage;
  }
};

export const AgentPickerMenu = {
  render: () => {
    const stage = document.createElement("main");
    stage.className = "sr-stage";
    stage.appendChild(AgentPicker());
    return stage;
  }
};

export const AgentDetails = {
  render: () => {
    const stage = document.createElement("main");
    stage.className = "sr-stage";
    stage.innerHTML = AgentDetailsPopover();
    return stage;
  }
};

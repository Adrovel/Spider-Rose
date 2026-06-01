import {
  AgentDetailsPopover,
  AgentEditor,
  AgentPicker,
  FloatingAddButton,
  SidebarTabs,
  ToolsPanel,
  WorkflowCanvas,
  ZoomControls
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

export const SidebarToolsTab = {
  render: () => SidebarTabs({ active: "tools" })
};

export const AgentEditorPanel = {
  render: () => AgentEditor()
};

export const InfiniteCanvas = {
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

export const ZoomButtons = {
  render: () => {
    const stage = document.createElement("main");
    stage.className = "sr-stage";
    stage.innerHTML = ZoomControls();
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

export const ToolsPanelStory = {
  name: "Tools Panel",
  render: () => ToolsPanel()
};

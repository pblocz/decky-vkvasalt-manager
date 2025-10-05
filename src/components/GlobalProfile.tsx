import {
  ButtonItem,
  PanelSectionRow,
  ToggleField,
} from "@decky/ui";

interface GlobalProfileProps {
  activeProfile: string | null;
  enableOnLaunch: boolean;
  enableOnLaunchLoading: boolean;
  onToggleEnableOnLaunch: (enabled: boolean) => void;
  onRefresh: () => void;
  onViewGlobalConfig: () => void;
  onResetProfile: () => void;
}

export function GlobalProfile({
  activeProfile,
  enableOnLaunch,
  enableOnLaunchLoading,
  onToggleEnableOnLaunch,
  onRefresh,
  onViewGlobalConfig,
  onResetProfile
}: GlobalProfileProps) {
  return (
    <>
      <PanelSectionRow>
        <div style={{ fontSize: '14px', marginBottom: '8px' }}>
          <strong>Active Profile:</strong> {activeProfile || "None"}
        </div>
      </PanelSectionRow>

      <PanelSectionRow>
        <ToggleField
          label="Enable on Launch"
          description="Automatically enable vkBasalt when games start"
          checked={enableOnLaunch}
          disabled={enableOnLaunchLoading}
          onChange={onToggleEnableOnLaunch}
        />
      </PanelSectionRow>
      
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onRefresh}
        >
          Refresh
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onViewGlobalConfig}
        >
          View Global Config
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onResetProfile}
        >
          Disable
        </ButtonItem>
      </PanelSectionRow>
    </>
  );
}
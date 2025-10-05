import {
  ButtonItem,
  PanelSectionRow,
} from "@decky/ui";

export interface ProfileItemProps {
  profileName: string;
  isActive: boolean;
  isTagged: boolean;
  onActivate: (profileName: string) => void;
  onCopySteamCommand: (profileName: string) => void;
  onViewConfig: (profileName: string) => void;
}

export function ProfileItem({ profileName, isActive, isTagged, onActivate, onCopySteamCommand, onViewConfig }: ProfileItemProps) {
  return (
    <>
      <PanelSectionRow>
        <div style={{ fontSize: '14px', fontWeight: '500' }}>
          {profileName} {isActive && <span style={{ color: '#4CAF50', fontSize: '12px' }}>(active)</span>}
          {!isTagged && <span style={{ color: '#FF9800', fontSize: '12px' }}>(untagged)</span>}
        </div>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          bottomSeparator="none"
          onClick={() => onActivate(profileName)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            Activate
          </div>
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          bottomSeparator="none"
          onClick={() => onCopySteamCommand(profileName)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            Copy Steam Cmd
          </div>
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => onViewConfig(profileName)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            View Config
          </div>
        </ButtonItem>
      </PanelSectionRow>
    </>
  );
}
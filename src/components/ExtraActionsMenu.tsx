import {
  ButtonItem,
  PanelSectionRow,
} from "@decky/ui";

export interface ExtraActionsMenuProps {
  onCopyForceZinkCommand: () => void;
}

export function ExtraActionsMenu({ onCopyForceZinkCommand }: ExtraActionsMenuProps) {
  return (
    <>
      <PanelSectionRow>
        <div style={{ 
          fontSize: '13px', 
          fontWeight: '500', 
          color: '#888',
          paddingBottom: '4px',
          borderBottom: '1px solid #444',
          marginBottom: '8px'
        }}>
          Extra Actions
        </div>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          bottomSeparator="none"
          onClick={() => onCopyForceZinkCommand()}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            Copy Force Zink Cmd
          </div>
        </ButtonItem>
      </PanelSectionRow>
    </>
  );
}
import { useState, useEffect } from "react";
import {
  PanelSectionRow,
  ButtonItem,
  Dropdown,
  DropdownOption,
} from "@decky/ui";

interface ProfileSectionProps {
  profiles: string[];
  activeProfile: string | null;
  profileTags: Record<string, boolean>;
  onActivate: (profileName: string) => void;
  onCopySteamCommand: (profileName: string) => void;
  onViewConfig: (profileName: string) => void;
}

export function ProfileSection({ 
  profiles, 
  activeProfile, 
  profileTags,
  onActivate,
  onCopySteamCommand,
  onViewConfig
}: ProfileSectionProps) {
  const [selectedProfile, setSelectedProfile] = useState<string>(activeProfile || "");

  // Update selectedProfile when activeProfile changes
  useEffect(() => {
    if (activeProfile) {
      setSelectedProfile(activeProfile);
    }
  }, [activeProfile]);

  // Create dropdown options
  const dropdownOptions = profiles.map(profile => ({
    data: profile,
    label: profile === activeProfile ? `${profile} (active)` : profile
  }));

  const handleOptionChange = (option: DropdownOption) => {
    setSelectedProfile(option.data);
  };

  const isSelectedProfileTagged = selectedProfile ? (profileTags[selectedProfile] ?? false) : true;

  return (
    <>
      <PanelSectionRow>
        <div style={{ fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
          Select Profile:
        </div>
        <Dropdown
          rgOptions={dropdownOptions}
          selectedOption={selectedProfile}
          onChange={handleOptionChange}
          strDefaultLabel="Select a profile..."
        />
      </PanelSectionRow>

      {selectedProfile && (
        <>
          <PanelSectionRow>
            <div style={{ fontSize: '14px', fontWeight: '500' }}>
              {selectedProfile}{" "}
              {selectedProfile === activeProfile && (
                <span style={{ color: '#4CAF50', fontSize: '12px' }}>(active)</span>
              )}
              {!isSelectedProfileTagged && (
                <span style={{ color: '#FF9800', fontSize: '12px' }}>(untagged)</span>
              )}
            </div>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              bottomSeparator="none"
              onClick={() => onActivate(selectedProfile)}
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
              onClick={() => onCopySteamCommand(selectedProfile)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                Copy Steam Cmd
              </div>
            </ButtonItem>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              onClick={() => onViewConfig(selectedProfile)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                View Config
              </div>
            </ButtonItem>
          </PanelSectionRow>
        </>
      )}
    </>
  );
}

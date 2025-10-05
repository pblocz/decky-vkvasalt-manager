import {
  Dropdown,
  DropdownOption,
  PanelSectionRow,
} from "@decky/ui";
import { useEffect, useState } from "react";

interface DropdownProfileProps {
  profiles: string[];
  activeProfile: string | null;
}

export function DropdownProfile({ 
  profiles, 
  activeProfile, 
}: DropdownProfileProps) {
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
    }

    return (
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
    );
}
import {
  Dropdown,
  DropdownOption,
  PanelSectionRow,
} from "@decky/ui";
import { useState } from "react";

interface DropdownProfileProps {
  profiles: string[];
  activeProfile: string | null;
}

export function DropdownProfile({ 
  profiles, 
  activeProfile, 
}: DropdownProfileProps) {
    const [selectedProfile, setSelectedProfile] = useState<string>("");

    // Create dropdown options
    const dropdownOptions = profiles.map(profile => ({
        data: profile,
        label: profile === activeProfile ? `${profile} (active)` : profile
    }));

    // Find the selected option object for the dropdown
    const selectedOption = dropdownOptions.find(option => option.data === selectedProfile);

    const handleOptionChange = (option: DropdownOption) => {
        console.log("Selected option:", option);
        setSelectedProfile(option.data);
    }

    console.log("DropdownProfile Render");
    console.log(dropdownOptions);
    console.log(selectedOption);
    console.log(selectedProfile);

    return (
      <PanelSectionRow>
        <div style={{ fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
          Select Profile:
        </div>
        <Dropdown
          rgOptions={dropdownOptions}
          selectedOption={selectedOption}
          onChange={handleOptionChange}
          strDefaultLabel="Select a profile..."
        />
        </PanelSectionRow>
    );
}
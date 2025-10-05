import {
  ButtonItem,
  PanelSectionRow,
} from "@decky/ui";

interface MaintenanceSectionProps {
  profileTags: Record<string, boolean>;
  activeProfile: string | null;
  globalTagged: boolean;
  onPatchProfiles: () => void;
}

export function MaintenanceSection({ 
  profileTags, 
  activeProfile, 
  globalTagged, 
  onPatchProfiles 
}: MaintenanceSectionProps) {
  // Show maintenance section if there are untagged profiles or global profile is untagged
  const needsMaintenance = Object.values(profileTags).some(tagged => !tagged) || 
                          (activeProfile && !globalTagged);

  if (!needsMaintenance) {
    return null;
  }

  return (
    <PanelSectionRow>
      <div style={{ fontSize: '12px', color: '#FF9800', marginBottom: '4px' }}>
        Some profiles need maintenance
      </div>
      <ButtonItem
        layout="below"
        onClick={onPatchProfiles}
      >
        Fix Profile Tags
      </ButtonItem>
    </PanelSectionRow>
  );
}
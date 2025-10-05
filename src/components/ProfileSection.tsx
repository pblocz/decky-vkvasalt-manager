import { useState, useEffect } from "react";
import { DropdownProfile } from "./DropdownProfile";
import { ProfileItem } from "./ProfileItem";

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

  const handleProfileSelect = (profileName: string) => {
    setSelectedProfile(profileName);
  };

  return (
    <>
      <DropdownProfile
        profiles={profiles}
        activeProfile={activeProfile}
        onProfileSelect={handleProfileSelect}
      />

      {selectedProfile && (
        <ProfileItem
          profileName={selectedProfile}
          isActive={selectedProfile === activeProfile}
          isTagged={profileTags[selectedProfile] ?? false}
          onActivate={onActivate}
          onCopySteamCommand={onCopySteamCommand}
          onViewConfig={onViewConfig}
        />
      )}
    </>
  );
}

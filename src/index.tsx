import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses
} from "@decky/ui";
import {
  callable,
  definePlugin,
  toaster,
} from "@decky/api"
import { useState, useEffect } from "react";
import { VscSettingsGear } from "react-icons/vsc";
import { copyWithVerification } from "./utils/clipboardUtils";

// Backend function calls
const listProfiles = callable<[], string[]>("list_profiles");
const getActiveProfile = callable<[], string | null>("get_active_profile");
const activateProfileGlobally = callable<[profile_name: string], boolean>("activate_profile_globally");
const getSteamCommand = callable<[profile_name: string], string>("get_steam_command");
const resetProfile = callable<[], boolean>("reset_profile");
const checkProfileTags = callable<[], Record<string, boolean>>("check_profile_tags");
const patchUntaggedProfiles = callable<[], boolean>("patch_untagged_profiles");
const isGlobalProfileTagged = callable<[], boolean>("is_global_profile_tagged");

interface ProfileItemProps {
  profileName: string;
  isActive: boolean;
  isTagged: boolean;
  onActivate: (profileName: string) => void;
  onCopySteamCommand: (profileName: string) => void;
}

function ProfileItem({ profileName, isActive, isTagged, onActivate, onCopySteamCommand }: ProfileItemProps) {
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
          onClick={() => onCopySteamCommand(profileName)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            Copy Steam Cmd
          </div>
        </ButtonItem>
      </PanelSectionRow>
    </>
  );
}

function Content() {
  const [profiles, setProfiles] = useState<string[]>([]);
  const [activeProfile, setActiveProfile] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [profileTags, setProfileTags] = useState<Record<string, boolean>>({});
  const [globalTagged, setGlobalTagged] = useState<boolean>(false);

  const refreshProfiles = async () => {
    try {
      setLoading(true);
      const [profileList, active, tags, globalTag] = await Promise.all([
        listProfiles(),
        getActiveProfile(),
        checkProfileTags(),
        isGlobalProfileTagged()
      ]);
      setProfiles(profileList);
      setActiveProfile(active);
      setProfileTags(tags);
      setGlobalTagged(globalTag);
    } catch (error) {
      console.error('Failed to load profiles:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load vkBasalt profiles"
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshProfiles();
  }, []);

  const handleActivateProfile = async (profileName: string) => {
    try {
      const success = await activateProfileGlobally(profileName);
      if (success) {
        setActiveProfile(profileName);
        toaster.toast({
          title: "Success",
          body: `Activated profile: ${profileName}`
        });
      } else {
        toaster.toast({
          title: "Error",
          body: `Failed to activate profile: ${profileName}`
        });
      }
    } catch (error) {
      console.error('Failed to activate profile:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to activate profile"
      });
    }
  };

  const handleCopySteamCommand = async (profileName: string) => {
    try {
      const command = await getSteamCommand(profileName);
      const result = await copyWithVerification(command);
      
      if (result.success) {
        toaster.toast({
          title: "Copied!",
          body: `Steam command copied to clipboard${result.verified ? ' (verified)' : ''}`
        });
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to copy Steam command"
        });
      }
    } catch (error) {
      console.error('Failed to copy command:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to copy Steam command"
      });
    }
  };

  const handleResetProfile = async () => {
    try {
      const success = await resetProfile();
      if (success) {
        setActiveProfile(null);
        toaster.toast({
          title: "Success",
          body: "vkBasalt disabled"
        });
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to reset profile"
        });
      }
    } catch (error) {
      console.error('Failed to reset profile:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to reset profile"
      });
    }
  };

  const handlePatchProfiles = async () => {
    try {
      const success = await patchUntaggedProfiles();
      if (success) {
        await refreshProfiles(); // Refresh to show updated status
        toaster.toast({
          title: "Success",
          body: "Profile tags updated"
        });
      } else {
        toaster.toast({
          title: "Info",
          body: "No profiles needed patching"
        });
      }
    } catch (error) {
      console.error('Failed to patch profiles:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to patch profile tags"
      });
    }
  };

  if (loading) {
    return (
      <PanelSection title="vkBasalt Profile Manager">
        <PanelSectionRow>
          <div>Loading profiles...</div>
        </PanelSectionRow>
      </PanelSection>
    );
  }

  if (profiles.length === 0) {
    return (
      <PanelSection title="vkBasalt Profile Manager">
        <PanelSectionRow>
          <div style={{ fontSize: '14px', color: '#888' }}>
            No profiles found. Please install vkbasalt-manager and create profiles.
          </div>
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={refreshProfiles}
          >
            Refresh
          </ButtonItem>
        </PanelSectionRow>
      </PanelSection>
    );
  }

  return (
    <PanelSection title="vkBasalt Profile Manager">
      <PanelSectionRow>
        <div style={{ fontSize: '14px', marginBottom: '8px' }}>
          <strong>Active Profile:</strong> {activeProfile || "None"}
        </div>
      </PanelSectionRow>
      
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={refreshProfiles}
        >
          Refresh
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={handleResetProfile}
        >
          Disable
        </ButtonItem>
      </PanelSectionRow>

      {/* Show maintenance section if there are untagged profiles or global profile is untagged */}
      {(Object.values(profileTags).some(tagged => !tagged) || (activeProfile && !globalTagged)) && (
        <PanelSectionRow>
          <div style={{ fontSize: '12px', color: '#FF9800', marginBottom: '4px' }}>
            Some profiles need maintenance
          </div>
          <ButtonItem
            layout="below"
            onClick={handlePatchProfiles}
          >
            Fix Profile Tags
          </ButtonItem>
        </PanelSectionRow>
      )}

      {profiles.map((profile) => (
        <ProfileItem
          key={profile}
          profileName={profile}
          isActive={profile === activeProfile}
          isTagged={profileTags[profile] ?? false}
          onActivate={handleActivateProfile}
          onCopySteamCommand={handleCopySteamCommand}
        />
      ))}
    </PanelSection>
  );
};

export default definePlugin(() => {
  return {
    // The name shown in various decky menus
    name: "vkBasalt Profile Manager",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>vkBasalt Profile Manager</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <VscSettingsGear />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("vkBasalt Profile Manager unloading")
    },
  };
});
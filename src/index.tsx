import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  ToggleField,
  Dropdown,
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
import { showConfigModal } from "./components/ConfigModal";

// Backend function calls
const listProfiles = callable<[], string[]>("list_profiles");
const getActiveProfile = callable<[], string | null>("get_active_profile");
const activateProfileGlobally = callable<[profile_name: string], boolean>("activate_profile_globally");
const getSteamCommand = callable<[profile_name: string], string>("get_steam_command");
const resetProfile = callable<[], boolean>("reset_profile");
const checkProfileTags = callable<[], Record<string, boolean>>("check_profile_tags");
const patchUntaggedProfiles = callable<[], boolean>("patch_untagged_profiles");
const isGlobalProfileTagged = callable<[], boolean>("is_global_profile_tagged");
const getEnableOnLaunchStatus = callable<[], boolean>("get_enable_on_launch_status");
const setEnableOnLaunch = callable<[enabled: boolean], boolean>("set_enable_on_launch");
const getGlobalConfig = callable<[], string>("get_global_config");
const getProfileConfig = callable<[profile_name: string], string>("get_profile_config");

function Content() {
  const [profiles, setProfiles] = useState<string[]>([]);
  const [activeProfile, setActiveProfile] = useState<string | null>(null);
  const [selectedProfile, setSelectedProfile] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [profileTags, setProfileTags] = useState<Record<string, boolean>>({});
  const [globalTagged, setGlobalTagged] = useState<boolean>(false);
  const [enableOnLaunch, setEnableOnLaunchState] = useState<boolean>(false);
  const [enableOnLaunchLoading, setEnableOnLaunchLoading] = useState<boolean>(false);

  const refreshProfiles = async () => {
    try {
      setLoading(true);
      const [profileList, active, tags, globalTag, enableStatus] = await Promise.all([
        listProfiles(),
        getActiveProfile(),
        checkProfileTags(),
        isGlobalProfileTagged(),
        getEnableOnLaunchStatus()
      ]);
      setProfiles(profileList);
      setActiveProfile(active);
      setProfileTags(tags);
      setGlobalTagged(globalTag);
      setEnableOnLaunchState(enableStatus);
      
      // Set selected profile to active profile or first profile
      if (active && profileList.includes(active)) {
        setSelectedProfile(active);
      } else if (profileList.length > 0) {
        setSelectedProfile(profileList[0]);
      }
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

  const handleActivateProfile = async () => {
    if (!selectedProfile) return;
    
    try {
      const success = await activateProfileGlobally(selectedProfile);
      if (success) {
        setActiveProfile(selectedProfile);
        toaster.toast({
          title: "Success",
          body: `Activated profile: ${selectedProfile}`
        });
      } else {
        toaster.toast({
          title: "Error",
          body: `Failed to activate profile: ${selectedProfile}`
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

  const handleCopySteamCommand = async () => {
    if (!selectedProfile) return;
    
    try {
      const command = await getSteamCommand(selectedProfile);
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

  const handleViewConfig = async () => {
    if (!selectedProfile) return;
    
    try {
      const config = await getProfileConfig(selectedProfile);
      showConfigModal(
        `Profile Configuration: ${selectedProfile}`,
        config,
        selectedProfile
      );
    } catch (error) {
      console.error('Failed to load profile config:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load profile configuration"
      });
    }
  };

  const handleViewGlobalConfig = async () => {
    try {
      const config = await getGlobalConfig();
      showConfigModal(
        "Global vkBasalt Configuration",
        config || "No global configuration found"
      );
    } catch (error) {
      console.error('Failed to load global config:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load global configuration"
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

  const handleToggleEnableOnLaunch = async (enabled: boolean) => {
    setEnableOnLaunchLoading(true);
    try {
      const success = await setEnableOnLaunch(enabled);
      if (success) {
        setEnableOnLaunchState(enabled);
        toaster.toast({
          title: enabled ? "Enabled" : "Disabled",
          body: `vkBasalt ${enabled ? "will" : "won't"} launch automatically with games`
        });
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to change enable on launch setting"
        });
      }
    } catch (error) {
      console.error('Failed to toggle enable on launch:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to change enable on launch setting"
      });
    } finally {
      setEnableOnLaunchLoading(false);
    }
  };

  // Create dropdown options
  const dropdownOptions = profiles.map(profile => ({
    data: profile,
    label: profile === activeProfile ? `${profile} (active)` : profile
  }));

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
        <ToggleField
          label="Enable on Launch"
          description="Automatically enable vkBasalt when games start"
          checked={enableOnLaunch}
          disabled={enableOnLaunchLoading}
          onChange={handleToggleEnableOnLaunch}
        />
      </PanelSectionRow>
      
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={handleViewGlobalConfig}
        >
          View Global Config
        </ButtonItem>
      </PanelSectionRow>

      {/* Profile Selection Dropdown */}
      <PanelSectionRow>
        <div style={{ fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
          Select Profile:
        </div>
        <Dropdown
          rgOptions={dropdownOptions}
          selectedOption={selectedProfile}
          onChange={(option) => setSelectedProfile(option.data)}
          strDefaultLabel="Select a profile..."
        />
        {/* Show untagged warning for selected profile */}
        {selectedProfile && !profileTags[selectedProfile] && (
          <div style={{ fontSize: '12px', color: '#FF9800', marginTop: '4px' }}>
            ⚠️ This profile is untagged
          </div>
        )}
      </PanelSectionRow>

      {/* Action Buttons for Selected Profile */}
      {selectedProfile && (
        <>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              bottomSeparator="none"
              onClick={handleActivateProfile}
            >
              Activate Globally
            </ButtonItem>
          </PanelSectionRow>
          
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              bottomSeparator="none"
              onClick={handleCopySteamCommand}
            >
              Copy Steam Command
            </ButtonItem>
          </PanelSectionRow>
          
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              onClick={handleViewConfig}
            >
              View Config
            </ButtonItem>
          </PanelSectionRow>
        </>
      )}

      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={handleResetProfile}
        >
          Disable vkBasalt
        </ButtonItem>
      </PanelSectionRow>

      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={refreshProfiles}
        >
          Refresh
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
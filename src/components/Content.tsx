import {
    ButtonItem,
    PanelSection,
    PanelSectionRow,
} from "@decky/ui";
import { ProfileItem } from "./ProfileItem";
import { MaintenanceSection } from "./MaintenanceSection";
import { GlobalProfile } from "./GlobalProfile";
import { DropdownProfile } from "./DropdownProfile";
import { useProfiles } from "../hooks/useProfiles";
import { useProfileActions } from "../hooks/useProfileActions";



export function Content() {
    // Custom hooks handle all the complex logic
    const profileState = useProfiles();
    const profileActions = useProfileActions();

    const {
        profiles,
        activeProfile,
        loading,
        profileTags,
        globalTagged,
        enableOnLaunch,
        enableOnLaunchLoading,
        refreshProfiles,
        activateProfile,
        resetProfile,
        patchProfiles,
        toggleEnableOnLaunch
    } = profileState;

    const {
        copySteamCommand,
        viewProfileConfig,
        viewGlobalConfig
    } = profileActions;

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
            <GlobalProfile
                activeProfile={activeProfile}
                enableOnLaunch={enableOnLaunch}
                enableOnLaunchLoading={enableOnLaunchLoading}
                onToggleEnableOnLaunch={toggleEnableOnLaunch}
                onRefresh={refreshProfiles}
                onViewGlobalConfig={viewGlobalConfig}
                onResetProfile={resetProfile}
            />

            <MaintenanceSection
                profileTags={profileTags}
                activeProfile={activeProfile}
                globalTagged={globalTagged}
                onPatchProfiles={patchProfiles}
            />

            <DropdownProfile
                profiles={profiles}
                activeProfile={activeProfile}
            />

            {profiles.map((profile) => (
                <ProfileItem
                    key={profile}
                    profileName={profile}
                    isActive={profile === activeProfile}
                    isTagged={profileTags[profile] ?? false}
                    onActivate={activateProfile}
                    onCopySteamCommand={copySteamCommand}
                    onViewConfig={viewProfileConfig}
                />
            ))}
        </PanelSection>
    );
}
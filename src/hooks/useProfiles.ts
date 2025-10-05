import { useState, useEffect, useCallback } from "react";
import { toaster } from "@decky/api";
import { VkBasaltService } from "../services/vkBasaltService";

export interface ProfileState {
  profiles: string[];
  activeProfile: string | null;
  profileTags: Record<string, boolean>;
  globalTagged: boolean;
  enableOnLaunch: boolean;
  loading: boolean;
  enableOnLaunchLoading: boolean;
}

/**
 * Hook for managing vkBasalt profile state and operations
 * Centralizes all profile-related business logic
 */
export function useProfiles() {
  const [state, setState] = useState<ProfileState>({
    profiles: [],
    activeProfile: null,
    profileTags: {},
    globalTagged: false,
    enableOnLaunch: false,
    loading: true,
    enableOnLaunchLoading: false,
  });

  const refreshProfiles = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true }));
      const data = await VkBasaltService.loadInitialData();
      
      setState(prev => ({
        ...prev,
        profiles: data.profiles,
        activeProfile: data.activeProfile,
        profileTags: data.profileTags,
        globalTagged: data.globalTagged,
        enableOnLaunch: data.enableOnLaunch,
        loading: false,
      }));
    } catch (error) {
      console.error('Failed to load profiles:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load vkBasalt profiles"
      });
      setState(prev => ({ ...prev, loading: false }));
    }
  }, []);

  const activateProfile = useCallback(async (profileName: string) => {
    try {
      const success = await VkBasaltService.activateProfileGlobally(profileName);
      if (success) {
        setState(prev => ({ ...prev, activeProfile: profileName }));
        toaster.toast({
          title: "Success",
          body: `Activated profile: ${profileName}`
        });
        return true;
      } else {
        toaster.toast({
          title: "Error",
          body: `Failed to activate profile: ${profileName}`
        });
        return false;
      }
    } catch (error) {
      console.error('Failed to activate profile:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to activate profile"
      });
      return false;
    }
  }, []);

  const resetProfile = useCallback(async () => {
    try {
      const success = await VkBasaltService.resetProfile();
      if (success) {
        setState(prev => ({ ...prev, activeProfile: null }));
        toaster.toast({
          title: "Success",
          body: "vkBasalt disabled"
        });
        return true;
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to reset profile"
        });
        return false;
      }
    } catch (error) {
      console.error('Failed to reset profile:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to reset profile"
      });
      return false;
    }
  }, []);

  const patchProfiles = useCallback(async () => {
    try {
      const success = await VkBasaltService.patchUntaggedProfiles();
      if (success) {
        await refreshProfiles(); // Refresh to show updated status
        toaster.toast({
          title: "Success",
          body: "Profile tags updated"
        });
        return true;
      } else {
        toaster.toast({
          title: "Info",
          body: "No profiles needed patching"
        });
        return false;
      }
    } catch (error) {
      console.error('Failed to patch profiles:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to patch profile tags"
      });
      return false;
    }
  }, [refreshProfiles]);

  const toggleEnableOnLaunch = useCallback(async (enabled: boolean) => {
    setState(prev => ({ ...prev, enableOnLaunchLoading: true }));
    try {
      const success = await VkBasaltService.setEnableOnLaunch(enabled);
      if (success) {
        setState(prev => ({ ...prev, enableOnLaunch: enabled }));
        toaster.toast({
          title: enabled ? "Enabled" : "Disabled",
          body: `vkBasalt ${enabled ? "will" : "won't"} launch automatically with games`
        });
        return true;
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to change enable on launch setting"
        });
        return false;
      }
    } catch (error) {
      console.error('Failed to toggle enable on launch:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to change enable on launch setting"
      });
      return false;
    } finally {
      setState(prev => ({ ...prev, enableOnLaunchLoading: false }));
    }
  }, []);

  useEffect(() => {
    refreshProfiles();
  }, [refreshProfiles]);

  return {
    ...state,
    refreshProfiles,
    activateProfile,
    resetProfile,
    patchProfiles,
    toggleEnableOnLaunch,
  };
}
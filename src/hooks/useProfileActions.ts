import { useCallback } from "react";
import { toaster } from "@decky/api";
import { VkBasaltService } from "../services/vkBasaltService";
import { copyWithVerification } from "../utils/clipboardUtils";
import { showConfigModal } from "../components/ConfigModal";

/**
 * Hook for profile-related actions like copying commands and viewing configs
 * Separates action logic from state management
 */
export function useProfileActions() {
  const copySteamCommand = useCallback(async (profileName: string) => {
    try {
      const command = await VkBasaltService.getSteamCommand(profileName);
      const result = await copyWithVerification(command);
      
      if (result.success) {
        toaster.toast({
          title: "Copied!",
          body: `Steam command copied to clipboard${result.verified ? ' (verified)' : ''}`
        });
        return true;
      } else {
        toaster.toast({
          title: "Error",
          body: "Failed to copy Steam command"
        });
        return false;
      }
    } catch (error) {
      console.error('Failed to copy command:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to copy Steam command"
      });
      return false;
    }
  }, []);

  const viewProfileConfig = useCallback(async (profileName: string) => {
    try {
      const config = await VkBasaltService.getProfileConfig(profileName);
      showConfigModal(
        `Profile Configuration: ${profileName}`,
        config,
        profileName
      );
      return true;
    } catch (error) {
      console.error('Failed to load profile config:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load profile configuration"
      });
      return false;
    }
  }, []);

  const viewGlobalConfig = useCallback(async () => {
    try {
      const config = await VkBasaltService.getGlobalConfig();
      showConfigModal(
        "Global vkBasalt Configuration",
        config || "No global configuration found"
      );
      return true;
    } catch (error) {
      console.error('Failed to load global config:', error);
      toaster.toast({
        title: "Error",
        body: "Failed to load global configuration"
      });
      return false;
    }
  }, []);

  return {
    copySteamCommand,
    viewProfileConfig,
    viewGlobalConfig,
  };
}
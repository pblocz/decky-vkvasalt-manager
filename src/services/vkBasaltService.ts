import { callable } from "@decky/api";

/**
 * Centralized service for all vkBasalt backend API calls
 * This provides a clean abstraction layer between the UI and backend
 */
export class VkBasaltService {
  // Profile management
  static readonly listProfiles = callable<[], string[]>("list_profiles");
  static readonly getActiveProfile = callable<[], string | null>("get_active_profile");
  static readonly activateProfileGlobally = callable<[profile_name: string], boolean>("activate_profile_globally");
  static readonly getSteamCommand = callable<[profile_name: string], string>("get_steam_command");

  // Profile tagging
  static readonly checkProfileTags = callable<[], Record<string, boolean>>("check_profile_tags");
  static readonly patchUntaggedProfiles = callable<[], boolean>("patch_untagged_profiles");
  static readonly isGlobalProfileTagged = callable<[], boolean>("is_global_profile_tagged");

  // Configuration management
  static readonly getEnableOnLaunchStatus = callable<[], boolean>("get_enable_on_launch_status");
  static readonly setEnableOnLaunch = callable<[enabled: boolean], boolean>("set_enable_on_launch");
  static readonly getGlobalConfig = callable<[], string>("get_global_config");
  static readonly getProfileConfig = callable<[profile_name: string], string>("get_profile_config");

  // Configuration editing
  static readonly getParsedProfileConfig = callable<[profile_name: string], Record<string, any>>("get_parsed_profile_config");

  /**
   * Load all initial data needed for the profile manager
   */
  static async loadInitialData() {
    const [profileList, active, tags, globalTag, enableStatus] = await Promise.all([
      this.listProfiles(),
      this.getActiveProfile(),
      this.checkProfileTags(),
      this.isGlobalProfileTagged(),
      this.getEnableOnLaunchStatus()
    ]);

    return {
      profiles: profileList,
      activeProfile: active,
      profileTags: tags,
      globalTagged: globalTag,
      enableOnLaunch: enableStatus
    };
  }
}
import os
import shutil
from pathlib import Path
from typing import List, Optional

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio

class Plugin:
    def __init__(self):
        self.vkbasalt_config_dir = Path.home() / ".config" / "vkBasalt"
        self.profiles_dir = self.vkbasalt_config_dir / "profiles"
        self.global_config = self.vkbasalt_config_dir / "vkBasalt.conf"
        
    async def list_profiles(self) -> List[str]:
        """List available vkBasalt profiles"""
        try:
            if not self.profiles_dir.exists():
                decky.logger.info("Profiles directory does not exist")
                return []
            
            profiles = []
            for conf_file in self.profiles_dir.glob("*.conf"):
                profiles.append(conf_file.stem)
            
            decky.logger.info(f"Found profiles: {profiles}")
            return sorted(profiles)
        except Exception as e:
            decky.logger.error(f"Error listing profiles: {e}")
            return []

    async def get_active_profile(self) -> Optional[str]:
        """Get the currently active profile name"""
        try:
            if not self.global_config.exists():
                return None
                
            # Check if the global config is a symlink pointing to a profile
            if self.global_config.is_symlink():
                target = self.global_config.readlink()
                if target.parent == self.profiles_dir:
                    return target.stem
                    
            # Check if the content matches any profile
            if self.global_config.exists():
                global_content = self.global_config.read_text()
                for profile_file in self.profiles_dir.glob("*.conf"):
                    if profile_file.read_text() == global_content:
                        return profile_file.stem
                        
            return None
        except Exception as e:
            decky.logger.error(f"Error getting active profile: {e}")
            return None

    async def activate_profile_globally(self, profile_name: str) -> bool:
        """Activate a profile by copying it to the global config location"""
        try:
            profile_path = self.profiles_dir / f"{profile_name}.conf"
            if not profile_path.exists():
                decky.logger.error(f"Profile {profile_name} does not exist")
                return False
                
            # Ensure the config directory exists
            self.vkbasalt_config_dir.mkdir(parents=True, exist_ok=True)
            
            # Remove existing global config if it exists
            if self.global_config.exists() or self.global_config.is_symlink():
                self.global_config.unlink()
                
            # Copy the profile to global config
            shutil.copy2(profile_path, self.global_config)
            
            decky.logger.info(f"Activated profile: {profile_name}")
            return True
        except Exception as e:
            decky.logger.error(f"Error activating profile {profile_name}: {e}")
            return False

    async def get_steam_command(self, profile_name: str) -> str:
        """Generate Steam launch command for a specific profile"""
        profile_path = self.profiles_dir / f"{profile_name}.conf"
        return f"VKBASALT_CONFIG_FILE={profile_path} %command%"

    async def reset_profile(self) -> bool:
        """Reset/disable vkBasalt by removing the global config"""
        try:
            if self.global_config.exists() or self.global_config.is_symlink():
                self.global_config.unlink()
                decky.logger.info("Reset vkBasalt configuration")
                return True
            return True
        except Exception as e:
            decky.logger.error(f"Error resetting profile: {e}")
            return False

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.loop = asyncio.get_event_loop()
        decky.logger.info("vkBasalt Profile Manager loaded!")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("vkBasalt Profile Manager unloading...")
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Goodbye World!")
        pass

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky.logger.info("vkBasalt Profile Manager migration")

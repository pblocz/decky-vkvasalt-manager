import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict
import re

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
        
    def _extract_profile_name_from_tag(self, content: str) -> Optional[str]:
        """Extract profile name from content tag"""
        match = re.search(r'^#\s*vkBasalt\s+Profile:\s*(.+?)$', content, re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else None
        
    def _ensure_profile_tag_in_content(self, content: str, profile_name: str) -> str:
        """Add or update profile tag to content with correct profile name"""
        existing_name = self._extract_profile_name_from_tag(content)
        
        # If tag exists and is correct, no changes needed
        if existing_name == profile_name:
            return content
            
        new_tag = f"# vkBasalt Profile: {profile_name}"
        lines = content.split('\n')
        
        # If tag exists but is wrong, replace it
        if existing_name:
            for i, line in enumerate(lines):
                if re.search(r'^#\s*vkBasalt\s+Profile:', line, re.IGNORECASE):
                    lines[i] = new_tag
                    return '\n'.join(lines)
        
        # If no tag exists, add it at the beginning after any existing leading comments
        insert_index = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            insert_index = i
            break
            
        lines.insert(insert_index, new_tag)
        return '\n'.join(lines)
        
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
                    
            if self.global_config.exists():
                # Try to read profile name from tag first (faster and more reliable)
                global_content = self.global_config.read_text()
                profile_name = self._extract_profile_name_from_tag(global_content)
                if profile_name:
                    # Verify the profile actually exists
                    profile_path = self.profiles_dir / f"{profile_name}.conf"
                    if profile_path.exists():
                        return profile_name
                        
                # Fall back to content comparison if tag is missing or invalid
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
            
            # Read profile content and ensure it has a proper tag
            content = profile_path.read_text()
            tagged_name = self._extract_profile_name_from_tag(content)
            
            # Add tag if missing or incorrect
            if tagged_name != profile_name:
                content = self._ensure_profile_tag_in_content(content, profile_name)
                # Update the original profile file with the tag
                profile_path.write_text(content)
                decky.logger.info(f"Updated tag in profile during activation: {profile_name}")
            
            # Remove existing global config if it exists
            if self.global_config.exists() or self.global_config.is_symlink():
                self.global_config.unlink()
                
            # Write the tagged content to global config
            self.global_config.write_text(content)
            
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

    async def check_profile_tags(self) -> Dict[str, bool]:
        """Check which profiles have proper name tags"""
        try:
            result = {}
            if not self.profiles_dir.exists():
                return result
                
            for profile_file in self.profiles_dir.glob("*.conf"):
                profile_name = profile_file.stem
                content = profile_file.read_text()
                tagged_name = self._extract_profile_name_from_tag(content)
                # Profile is properly tagged if it has a tag matching its filename
                result[profile_name] = tagged_name == profile_name
                
            decky.logger.info(f"Profile tag check result: {result}")
            return result
        except Exception as e:
            decky.logger.error(f"Error checking profile tags: {e}")
            return {}

    async def patch_untagged_profiles(self) -> bool:
        """Add missing name tags to profiles that don't have them"""
        try:
            if not self.profiles_dir.exists():
                return False
                
            patched_any = False
            for profile_file in self.profiles_dir.glob("*.conf"):
                profile_name = profile_file.stem
                content = profile_file.read_text()
                tagged_name = self._extract_profile_name_from_tag(content)
                
                # Add tag if missing or incorrect
                if tagged_name != profile_name:
                    new_content = self._ensure_profile_tag_in_content(content, profile_name)
                    profile_file.write_text(new_content)
                    decky.logger.info(f"Updated tag in profile: {profile_name}")
                    patched_any = True
                    
            return patched_any
        except Exception as e:
            decky.logger.error(f"Error patching untagged profiles: {e}")
            return False

    async def is_global_profile_tagged(self) -> bool:
        """Check if the currently active global profile has a proper tag"""
        try:
            if not self.global_config.exists():
                return False
                
            content = self.global_config.read_text()
            profile_name = self._extract_profile_name_from_tag(content)
            
            # Check if the tagged name corresponds to an existing profile
            if profile_name:
                profile_path = self.profiles_dir / f"{profile_name}.conf"
                return profile_path.exists()
                
            return False
        except Exception as e:
            decky.logger.error(f"Error checking global profile tag: {e}")
            return False

    async def get_enable_on_launch_status(self) -> bool:
        """Check if enableOnLaunch is enabled in the global config"""
        try:
            if not self.global_config.exists():
                return False
                
            content = self.global_config.read_text()
            # Look for enableOnLaunch = True line (case insensitive)
            match = re.search(r'^\s*enableOnLaunch\s*=\s*True\s*$', content, re.MULTILINE | re.IGNORECASE)
            return match is not None
        except Exception as e:
            decky.logger.error(f"Error getting enable on launch status: {e}")
            return False

    async def set_enable_on_launch(self, enabled: bool) -> bool:
        """Enable or disable the enableOnLaunch flag in global config"""
        try:
            # Ensure the config directory exists
            self.vkbasalt_config_dir.mkdir(parents=True, exist_ok=True)
            
            content = ""
            if self.global_config.exists():
                content = self.global_config.read_text()
            
            lines = content.split('\n')
            setting_line = f"enableOnLaunch = {'True' if enabled else 'False'}"
            
            # Look for existing enableOnLaunch line
            found_index = -1
            for i, line in enumerate(lines):
                if re.match(r'^\s*enableOnLaunch\s*=', line, re.IGNORECASE):
                    found_index = i
                    break
            
            if found_index >= 0:
                # Update existing line
                lines[found_index] = setting_line
            else:
                # Add new line at the beginning (after any existing comments)
                insert_index = 0
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if not stripped or stripped.startswith('#'):
                        continue
                    insert_index = i
                    break
                lines.insert(insert_index, setting_line)
            
            # Write back to file
            self.global_config.write_text('\n'.join(lines))
            
            decky.logger.info(f"Set enableOnLaunch to {enabled}")
            return True
        except Exception as e:
            decky.logger.error(f"Error setting enable on launch: {e}")
            return False

    async def get_global_config(self) -> str:
        """Get the contents of the global vkBasalt configuration file"""
        try:
            if not self.global_config.exists():
                return ""
            return self.global_config.read_text()
        except Exception as e:
            decky.logger.error(f"Error reading global config: {e}")
            return ""

    async def get_profile_config(self, profile_name: str) -> str:
        """Get the contents of a specific profile configuration file"""
        try:
            profile_path = self.profiles_dir / f"{profile_name}.conf"
            if not profile_path.exists():
                decky.logger.error(f"Profile {profile_name} does not exist")
                return ""
            return profile_path.read_text()
        except Exception as e:
            decky.logger.error(f"Error reading profile config {profile_name}: {e}")
            return ""

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

This is a Decky plugin with a **single sidebar UI** and no profile editing/renaming in the MVP, I’ll also align the backend section with the [Decky](https://github.com/SteamDeckHomebrew/decky-plugin-template).

Here’s the updated **Project Definition Document**:

---

# Project Definition: vkBasalt Profile Manager (Decky Plugin MVP)

## 1. Background & Context

### 1.1 vkBasalt: how it is enabled

vkBasalt is a Vulkan post-processing layer for Linux.
Officially, enabling vkBasalt requires setting an environment variable before launching a game:

* **Environment variable**

  ```bash
  ENABLE_VKBASALT=1 %command%
  ```

  (in Steam launch options or shell wrapper)

* **Config file discovery order**
  vkBasalt reads config from these paths (first match wins):

  1. `$VKBASALT_CONFIG_FILE` (if set)
  2. `vkBasalt.conf` in the working directory
  3. `$XDG_CONFIG_HOME/vkBasalt/vkBasalt.conf` (`~/.config/vkBasalt/vkBasalt.conf`)
  4. `$XDG_DATA_HOME/vkBasalt/vkBasalt.conf` (`~/.local/share/vkBasalt/vkBasalt.conf`)
  5. `/etc/vkBasalt.conf`
  6. `/etc/vkBasalt/vkBasalt.conf`
  7. `/usr/share/vkBasalt/vkBasalt.conf`

Other useful env vars:

* `VKBASALT_LOG_LEVEL` → controls logging verbosity
* `VKBASALT_LOG_FILE` → specifies a custom log file path

---

### 1.2 vkBasalt Manager (Vaddum’s script)

The **vkbasalt-manager** ([GitHub][2]) project provides an easy way to install vkBasalt and shaders on the Steam Deck.

* It offers features like:

  * Auto install (vkBasalt + ReShade shaders) ([GitHub][2])
  * Shader management: enable / disable effects via GUI ([GitHub][2])
  * Advanced parameter editing
  * Toggle key configuration
  * Config viewing, reset to defaults, uninstall ([GitHub][2])

#### File / folder layout used by the vkbasalt-manager


* Configuration file location: `~/.config/vkBasalt/vkBasalt.conf` ([GitHub][2])
* Shaders location: `~/.config/reshade/Shaders/` ([GitHub][2])
* Library install location: `~/.local/lib/libvkbasalt.so` ([GitHub][2])
* Desktop shortcut: `~/Desktop/VkBasalt-Manager.desktop` ([GitHub][2])
* Profiles location:  `~/.config/vkBasalt/profiles/<profile-name>.conf` ([GitHub][2])

⚠️ **Important:** vkbasalt-manager is responsible for profile creation/editing. The Decky plugin should only *list* and *activate* profiles.

---

## 2. High-Level Feature List (MVP)

### MVP Features

* **List available profiles**
  Detect profiles stored by vkbasalt-manager.
* **Show active profile**
  Indicate which profile is currently active.
* **Switch profiles**
  Allow user to activate a selected profile (overwrite or symlink `vkBasalt.conf`).
* **Generate Steam command**

  * Copies this string for the chosen profile:

    ```
    VKBASALT_CONFIG_FILE=/home/deck/.config/vkBasalt/profiles/<profile>.conf %command%
    ```
  * User can paste it into Steam’s game Launch Options


### Deferred Features (Future)

* Profile editing (parameters, shader toggles)
* Renaming, duplicating, deleting profiles
* Per-game profile mapping
* Import/export profiles
* Hotkey/toggle key editor
* Live reload during gameplay
* Shader management

---

## 3. Backend (Decky Plugin Format)

The backend will follow the [Decky plugin template](https://github.com/SteamDeckHomebrew/decky-plugin-template).

### 3.1 Core backend responsibilities

* **Profile discovery**
  Scan `~/.config/vkBasalt/profiles/` (or vkbasalt-manager's storage path) for available configs.
* **Activation**
  Copy or symlink the chosen profile's `vkBasalt.conf` into `~/.config/vkBasalt/vkBasalt.conf`.
* **State tracking**
  Report which profile is active to the frontend.
* **Reset**
  Remove or replace `vkBasalt.conf` with a blank/default version.
* **Profile tagging**
  Ensure profiles contain name tags as comments for identification, and patch missing tags when needed. document accordingly
* **Enable on launch toggle**
  Enable or disable the `enableOnLaunch = True` flag in the global profile configuration, and report current status.
* **Configuration viewing**
  Read and return the contents of the global `vkBasalt.conf` and individual profile configuration files for display in the UI.

### 3.2 Plugin API methods

These methods will be exposed via the Decky backend (`backend.py` in the template):

* `list_profiles() → [profile_names]`
* `get_active_profile() → str | None`
* `activate_profile_globally(name: str) → bool`
* `get_steam_command(name: str) → str`
* `check_profile_tags() → dict[str, bool]`
* `patch_untagged_profiles() → bool`
* `is_global_profile_tagged() → bool`
* `get_enable_on_launch_status() → bool`
* `set_enable_on_launch(enabled: bool) → bool`
* `get_global_config() → str`
* `get_profile_config(name: str) → str`

---

#### Example of `get_steam_command`

If a profile `cas.conf` exists in `~/.config/vkBasalt/profiles/`, return:

```
VKBASALT_CONFIG_FILE=/home/deck/.config/vkBasalt/profiles/cas.conf %command%
```

## 4. UI / Frontend Design (Decky Sidebar)

Since Decky plugins run in a **sidebar**, the UI should be minimal and navigable with the Steam Deck’s controls. No multi-page design.

### UI Elements

* **Header:** `vkBasalt Profile Manager`

* **Active Profile Indicator:**

  * Shows name of currently active profile, or “None” if disabled.

* **Profile List (scrollable):**

  * Each profile has three options:

    1. **[Activate Globally]** → sets it as global `vkBasalt.conf`
    2. **[Copy Steam Command]** → copies launch option string to clipboard
    3. **[View Config]** → opens modal showing profile configuration contents

* **View Global Config Button:**
  * Button to view current global `vkBasalt.conf` contents in a modal


### Example Flow

```
vkBasalt Profile Manager
-------------------------
Active Profile: CAS Sharpening
Enable on Launch: ON [Toggle]

[View Global Config]

Profiles:
  Default
  [Activate]
  [Copy Steam Cmd] 
  [View Config]
  ---
  CAS Sharpening  (active)
  [Activate]
  [Copy Steam Cmd] 
  [View Config]
  ---
  Vibrant Colors
  [Activate]
  [Copy Steam Cmd] 
  [View Config]
  ---
  FXAA + SMAA
  [Activate]
  [Copy Steam Cmd] 
  [View Config]
  ---
```

1. User opens Decky sidebar.
2. User scrolls list
3.1. Presses A on “Activate” → backend switches global profile
3.2. Presses A on “Copy Steam Cmd” → command copied to clipboard (toast notification shows “Copied!”)

---

## 5. Integration with vkBasalt Manager

* Profiles are **created/edited** in vkbasalt-manager (desktop).
* Decky plugin only **lists and switches** profiles.
* Ensure plugin does not overwrite profiles, only swaps symlinks/copies.
* If vkbasalt-manager is missing, plugin can show a message:
  “vkbasalt-manager not detected. Please install it to manage profiles.”

---

✅ This refined spec is aligned with your MVP goals:

* **No editing/renaming in Decky** (defer to desktop manager)
* **Single sidebar UI** for profile switching
* **Backend in Decky plugin format** with a few simple RPC methods
* **two main actions (global enable + Steam command copy)**


## Project structure

### 1. File/Folder Structure

```
vkbasalt-decky-plugin/
│
├── py_modules/
│   └── __init__.py
│
│── src/
│   ├── index.tsx  # React entrypoint, Decky UI sidebar
│   ├── services/
│   │   └── vkBasaltService.ts  # Centralized API service layer
│   ├── hooks/
│   │   ├── useProfiles.ts      # Profile state management hook
│   │   └── useProfileActions.ts # Profile action hooks (copy, view config)
│   ├── utils/
│   │   └── clipboardUtils.ts   # Reliable clipboard utilities for gaming mode
│   └── components/
│       ├── Content.tsx         # Main component (simplified with hooks)
│       ├── ProfileItem.tsx     # Individual profile list item
│       ├── GlobalProfile.tsx   # Global profile controls
│       ├── MaintenanceSection.tsx # Profile maintenance utilities
│       └── ConfigModal.tsx     # Modal component for displaying configurations
│
│── package.json   # Decky frontend metadata
│
│── plugin.json        # Plugin manifest
│── main.py {required if you are using the python backend of decky-loader: serverAPI}
├── README.md
└── LICENSE(.md) [required, filename should be roughly similar, suffix not needed]
```

### 2. Architecture Overview

The frontend follows a clean architecture pattern with separation of concerns:

#### 2.1 Service Layer (`src/services/`)
- **`vkBasaltService.ts`**: Centralized API service that provides a clean abstraction over all backend calls
- Includes a `loadInitialData()` method that efficiently fetches all required data in parallel
- All backend callable functions are organized in a single class for maintainability

#### 2.2 Custom Hooks (`src/hooks/`)
- **`useProfiles.ts`**: Manages all profile-related state and business logic
  - Handles loading, activating, resetting profiles
  - Manages enable-on-launch toggle
  - Provides profile tagging and maintenance operations
- **`useProfileActions.ts`**: Handles user actions like copying commands and viewing configurations
  - Separated from state management for better code organization
  - Includes error handling and user feedback via toasts

#### 2.3 Components (`src/components/`)
- **`Content.tsx`**: Main container component, now much simpler and focused on UI coordination
- **`ProfileItem.tsx`**: Reusable component for individual profile display
- **`GlobalProfile.tsx`**: Controls for active profile and global settings
- **`MaintenanceSection.tsx`**: Profile maintenance utilities (tagging, etc.)
- **`ConfigModal.tsx`**: Modal for displaying configuration contents

#### 2.4 Architecture Benefits

This new structure provides several advantages:

- **Separation of Concerns**: Business logic, API calls, and UI rendering are clearly separated
- **Reusability**: Custom hooks can be easily reused or tested independently
- **Maintainability**: Changes to API structure only require updates in the service layer
- **Testability**: Each layer can be unit tested in isolation
- **Performance**: Parallel data loading and optimized re-renders through focused state management
- **Developer Experience**: Cleaner, more readable code with clear responsibilities

### 3. Clipboard Utilities

The plugin includes specialized clipboard utilities (`src/utils/clipboardUtils.ts`) designed to work reliably in Steam Deck's gaming mode environment. These utilities provide multiple fallback methods for copying text, including the proven input simulation method that works when standard clipboard APIs may fail.

### 4. `plugin.json`
```
{
  "name": "vkBasalt Profile Manager",
  "author": "YourName",
  "version": "0.1.0",
  "backend": "backend",
  "frontend": "frontend",
  "description": "Switch between vkBasalt profiles created by vkbasalt-manager",
  "license": "MIT"
}
```

---

### 5.1 Profile Tagging System

Each vkBasalt profile should contain a comment tag at the top identifying its name. This enables the plugin to identify which profile is currently active by reading the global `vkBasalt.conf` file.

#### Tag Format

Profile files should include a comment at the top:
```
# vkBasalt Profile: <profile-name>
```

For example, a profile named "CAS Sharpening" would have:
```
# vkBasalt Profile: CAS Sharpening
effects = cas
# ... rest of config
```

#### Tagging API Methods

* **`check_profile_tags() → dict[str, bool]`**
  Returns a dictionary mapping profile names to whether they have proper tags.
  
* **`patch_untagged_profiles() → bool`**
  Adds missing name tags to profiles that don't have them. Returns `True` if any profiles were patched.
  
* **`is_global_profile_tagged() → bool`**
  Checks if the currently active global `vkBasalt.conf` has a profile tag, enabling identification of the active profile.

#### Active Profile Detection

The plugin can determine the active profile in two ways:
1. **By file comparison** - Compare global config with profile files
2. **By tag reading** - Read the profile tag from the global config (faster and more reliable)

If the global config lacks a tag, the plugin should offer to patch it or fall back to file comparison.


### 5.2 Enable on Launch Implementation

The `enableOnLaunch` feature allows users to control whether vkBasalt automatically activates when games start, without requiring manual environment variable setup.

#### Backend Implementation (`main.py`)

* **`get_enable_on_launch_status() → bool`**
  - Reads the global `vkBasalt.conf` file
  - Searches for `enableOnLaunch = True` line
  - Returns `True` if found and enabled, `False` otherwise

* **`set_enable_on_launch(enabled: bool) → bool`**
  - Modifies the global `vkBasalt.conf` file
  - Adds/removes/updates the `enableOnLaunch = True/False` line
  - Preserves other configuration settings
  - Returns success status

#### Frontend Implementation (`src/hooks/useProfiles.ts` & `src/components/GlobalProfile.tsx`)

* Toggle switch component in `GlobalProfile.tsx` showing current enableOnLaunch status
* Business logic handled in `useProfiles.ts` hook with `toggleEnableOnLaunch` method
* Displays loading state during toggle operation
* Shows toast notifications for success/failure feedback
* State management is centralized and reusable across components

#### Configuration Details

The `enableOnLaunch` flag in vkBasalt configuration:
- When `enableOnLaunch = True`: vkBasalt automatically applies effects to all Vulkan applications
- When `enableOnLaunch = False` or absent: vkBasalt only activates with explicit environment variables
- This provides a global on/off switch independent of profile selection

### 5.3 ConfigModal Component

The `ConfigModal` component (`src/components/ConfigModal.tsx`) provides a modal dialog for displaying configuration file contents in a user-friendly format.

#### Features

* **Syntax highlighting** - Configuration files are displayed with appropriate syntax highlighting for better readability
* **Scrollable content** - Large configuration files can be scrolled within the modal
* **Copy to clipboard** - Users can copy the entire configuration content to clipboard
* **Responsive design** - Modal adapts to different screen sizes and orientations
* **Steam Deck optimized** - Button layout and navigation designed for gamepad controls

#### Props Interface

```typescript
interface ConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  content: string;
  profileName?: string;
}
```

#### Usage Examples

**Global Configuration Modal:**
```typescript
<ConfigModal
  isOpen={showGlobalConfig}
  onClose={() => setShowGlobalConfig(false)}
  title="Global vkBasalt Configuration"
  content={globalConfigContent}
/>
```

**Profile Configuration Modal:**
```typescript
<ConfigModal
  isOpen={showProfileConfig}
  onClose={() => setShowProfileConfig(false)}
  title={`Profile Configuration: ${selectedProfile}`}
  content={profileConfigContent}
  profileName={selectedProfile}
/>
```

#### Backend Integration

The modal component integrates with these backend methods:
* `get_global_config()` - Retrieves current global configuration
* `get_profile_config(name: str)` - Retrieves specific profile configuration
````
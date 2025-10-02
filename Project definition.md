This is a Decky plugin with a **single sidebar UI** and no profile editing/renaming in the MVP, I’ll refine the document accordingly. I’ll also align the backend section with the [Decky plugin template](https://github.com/SteamDeckHomebrew/decky-plugin-template).

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
  Scan `~/.config/vkBasalt/profiles/` (or vkbasalt-manager’s storage path) for available configs.
* **Activation**
  Copy or symlink the chosen profile’s `vkBasalt.conf` into `~/.config/vkBasalt/vkBasalt.conf`.
* **State tracking**
  Report which profile is active to the frontend.
* **Reset**
  Remove or replace `vkBasalt.conf` with a blank/default version.

### 3.2 Plugin API methods

These methods will be exposed via the Decky backend (`backend.py` in the template):

* `list_profiles() → [profile_names]`
* `get_active_profile() → str | None`
* `activate_profile_globally(name: str) → bool`
* `get_steam_command(name: str) → str`

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

  * Each profile has two options:

    1. **[Activate Globally]** → sets it as global `vkBasalt.conf`
    2. **[Copy Steam Command]** → copies launch option string to clipboard


### Example Flow

```
vkBasalt Profile Manager
-------------------------
Active Profile: CAS Sharpening

Profiles:
  [Activate] [Copy Steam Cmd] Default
  [Activate] [Copy Steam Cmd] CAS Sharpening  (active)
  [Activate] [Copy Steam Cmd] Vibrant Colors
  [Activate] [Copy Steam Cmd] FXAA + SMAA
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
│   └── components/
│       └── ProfileList.tsx
│
│── package.json   # Decky frontend metadata
│
│── plugin.json        # Plugin manifest
│── main.py {required if you are using the python backend of decky-loader: serverAPI}
├── README.md
└── LICENSE(.md) [required, filename should be roughly similar, suffix not needed]
```

### 2. `plugin.json`
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
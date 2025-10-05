import {
  staticClasses
} from "@decky/ui";
import {
  definePlugin,
} from "@decky/api"
import { VscSettingsGear } from "react-icons/vsc";
import { Content } from "./components/Content";



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
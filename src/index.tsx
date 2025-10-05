import {
  staticClasses
} from "@decky/ui";
import {
  definePlugin,
} from "@decky/api"
// import { GiStoneStack } from "react-icons/gi";
import { GiStonePile } from "react-icons/gi";
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
    icon: <GiStonePile />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("vkBasalt Profile Manager unloading")
    },
  };
});
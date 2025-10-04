import { VFC } from "react";
import {
  DialogButton,
  Field,
  Focusable,
  ModalRoot,
  ModalRootProps,
  showModal,
} from "@decky/ui";
import { copyToClipboard } from "../utils/clipboardUtils";

interface ConfigModalProps extends ModalRootProps {
  title: string;
  content: string;
  profileName?: string;
}

const ConfigModal: VFC<ConfigModalProps> = ({
  title,
  content,
  profileName,
  closeModal,
  ...modalProps
}) => {
  const handleCopyToClipboard = async () => {
    try {
      await copyToClipboard(content);
      // Show a simple notification - in a real implementation you might want to use a toast
      console.log("Configuration copied to clipboard");
    } catch (error) {
      console.error("Failed to copy to clipboard:", error);
    }
  };

  return (
    <ModalRoot {...modalProps} closeModal={closeModal}>
      <div style={{ 
        padding: "20px", 
        minHeight: "400px", 
        maxHeight: "600px", 
        display: "flex", 
        flexDirection: "column" 
      }}>
        <Field label={title} />
        
        <div style={{ 
          flex: 1, 
          marginBottom: "20px", 
          overflow: "hidden",
          display: "flex",
          flexDirection: "column"
        }}>
          <textarea
            value={content}
            readOnly
            style={{
              flex: 1,
              fontFamily: "monospace",
              fontSize: "12px",
              backgroundColor: "#1a1a1a",
              color: "#e0e0e0",
              border: "1px solid #444",
              borderRadius: "4px",
              padding: "10px",
              overflow: "auto",
              whiteSpace: "pre",
              wordWrap: "break-word",
              resize: "none"
            }}
          />
        </div>

        <Focusable style={{ 
          display: "flex", 
          gap: "10px", 
          justifyContent: "flex-end" 
        }}>
          <DialogButton onClick={handleCopyToClipboard}>
            Copy to Clipboard
          </DialogButton>
          <DialogButton onClick={closeModal}>
            Close
          </DialogButton>
        </Focusable>
      </div>
    </ModalRoot>
  );
};

export const showConfigModal = (
  title: string,
  content: string,
  profileName?: string
): void => {
  showModal(
    <ConfigModal
      title={title}
      content={content}
      profileName={profileName}
    />
  );
};

export default ConfigModal;

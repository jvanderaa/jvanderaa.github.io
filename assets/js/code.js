function extractCodeText(highlightDiv) {
  if (!highlightDiv) return "";

  const codeEl =
    highlightDiv.querySelector(".lntable .lntd:last-child code") ||
    highlightDiv.querySelector("code[data-lang]") ||
    highlightDiv.querySelector(".chroma > code, pre.chroma > code") ||
    highlightDiv.querySelector("code");

  if (codeEl) {
    // Chroma wraps each line's code in `.cl` spans (separate from `.ln` inline
    // line numbers). Reading `.textContent` avoids the double-newline inflation
    // that `.innerText` produces when `.chroma .line { display: flex }` is set,
    // while preserving intentional blank lines verbatim.
    const codeLines = codeEl.querySelectorAll(".cl");
    if (codeLines.length > 0) {
      return Array.from(codeLines, (el) => el.textContent).join("").replace(/\n$/, "");
    }
    return (codeEl.textContent || "").replace(/\n$/, "");
  }

  return (highlightDiv.innerText || "").replace(/\n$/, "");
}

if (typeof window !== "undefined" && typeof document !== "undefined") {
  const scriptBundle = document.getElementById("script-bundle");
  const copyText = scriptBundle ? scriptBundle.getAttribute("data-copy") : "Copy";
  const copiedText = scriptBundle ? scriptBundle.getAttribute("data-copied") : "Copied";

  function createCopyButton(highlightDiv) {
    const button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.ariaLabel = copyText;
    button.innerText = copyText;
    button.addEventListener("click", () => copyCodeToClipboard(button, highlightDiv));
    addCopyButtonToDom(button, highlightDiv);
  }

  async function copyCodeToClipboard(button, highlightDiv) {
    const codeToCopy = extractCodeText(highlightDiv);

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(codeToCopy);
      } else {
        copyCodeBlockExecCommand(codeToCopy, highlightDiv);
      }
    } catch (_) {
      copyCodeBlockExecCommand(codeToCopy, highlightDiv);
    } finally {
      codeWasCopied(button);
    }
  }

  function copyCodeBlockExecCommand(codeToCopy, highlightDiv) {
    const textArea = document.createElement("textarea");
    textArea.className = "copy-textarea";
    textArea.value = codeToCopy;
    highlightDiv.insertBefore(textArea, highlightDiv.firstChild);
    textArea.select();
    textArea.setSelectionRange(0, codeToCopy.length);
    document.execCommand("copy");
    highlightDiv.removeChild(textArea);
  }

  function codeWasCopied(button) {
    button.blur();
    button.innerText = copiedText;
    setTimeout(function () {
      button.innerText = copyText;
    }, 2000);
  }

  function addCopyButtonToDom(button, highlightDiv) {
    highlightDiv.insertBefore(button, highlightDiv.firstChild);
    const wrapper = document.createElement("div");
    wrapper.className = "highlight-wrapper";
    highlightDiv.parentNode.insertBefore(wrapper, highlightDiv);
    wrapper.appendChild(highlightDiv);
  }

  window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".highlight").forEach((highlightDiv) => createCopyButton(highlightDiv));
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { extractCodeText };
}

var scriptBundle = document.getElementById("script-bundle");
var copyText = scriptBundle ? scriptBundle.getAttribute("data-copy") : "Copy";
var copiedText = scriptBundle ? scriptBundle.getAttribute("data-copied") : "Copied";

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
  let codeToCopy;
  // Check if we are using table-based line numbers (linenos=table)
  // structure: .highlight > .chroma > .lntable > tbody > tr > td.lntd:last-child > pre > code
  const tableCode = highlightDiv.querySelector(".lntable .lntd:last-child code");
  
  if (tableCode) {
    codeToCopy = tableCode.innerText;
  } else {
    // Standard Hugo/Congo behavior: .highlight > .chroma > code (wrapped)
    // The original theme used ":last-child > .chroma > code" which is fragile.
    // We try a more robust approach:
    const standardCode = highlightDiv.querySelector("code[data-lang]");
    if (standardCode) {
        codeToCopy = standardCode.innerText;
    } else {
        // Fallback to original selector if data-lang is missing (some plain blocks)
        const element = highlightDiv.querySelector(":last-child > .chroma > code");
        codeToCopy = element ? element.innerText : "";
    }
  }

  // Sanity check: if codeToCopy is empty/null, try strictly the .chroma > code (standard case)
  if (!codeToCopy) {
      const simpleCode = highlightDiv.querySelector(".chroma > code");
      if (simpleCode) codeToCopy = simpleCode.innerText;
  }
  
  // If still nothing, extract all text as fallback (might include line numbers but better than crash)
  if (!codeToCopy) {
      console.warn("Could not find code element for copy");
      codeToCopy = highlightDiv.innerText;
  }

  // FORCE CORRECTION: The simple blocks often contain double newlines due to display:block Spans
  // We normalize this by replacing 3 or more newlines with 2, and 2 with 1, 
  // but we need to be careful not to merge intended empty lines.
  // Actually, standard behavior often results in \n\n for every line break.
  // Let's inspect if we can just use textContent? No, textContent ignores CSS display and might merge things weirdly.
  // Better: Regex replace \n\n with \n if it looks like a systematic issue.
  if (codeToCopy) {
      // Common issue: "Line 1\n\nLine 2\n\n" -> "Line 1\nLine 2"
      // But we must preserve intentional blank lines which might appear as \n\n\n
      
      // If every line is followed by an blank line, it's likely the double-spacing bug.
      // Heuristic: If there are NO single \n characters between non-whitespace, but LOTS of \n\n, it is the bug.
      
      // Attempt 1: naive replacement of \n\n with \n
      // This solves the immediate "too many newlines" issue shown in user output.
      // User showed:
      // # Change ...
      //
      // sudo ...
      //
      // That is double spacing.
      codeToCopy = codeToCopy.replace(/\n\n/g, "\n");
  }

  try {
    result = await navigator.permissions.query({ name: "clipboard-write" });
    if (result.state == "granted" || result.state == "prompt") {
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
  const textArea = document.createElement("textArea");
  textArea.contentEditable = "true";
  textArea.readOnly = "false";
  textArea.className = "copy-textarea";
  textArea.value = codeToCopy;
  highlightDiv.insertBefore(textArea, highlightDiv.firstChild);
  const range = document.createRange();
  range.selectNodeContents(textArea);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  textArea.setSelectionRange(0, 999999);
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

window.addEventListener("DOMContentLoaded", (event) => {
  document.querySelectorAll(".highlight").forEach((highlightDiv) => createCopyButton(highlightDiv));
});

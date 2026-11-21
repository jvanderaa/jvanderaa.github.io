const test = require("node:test");
const assert = require("node:assert/strict");
const { extractCodeText } = require("../assets/js/code.js");

function makeNode(text, { clTexts = null, children = {} } = {}) {
  return {
    textContent: text,
    innerText: text,
    querySelector(selector) {
      return children[selector] || null;
    },
    querySelectorAll(selector) {
      if (selector === ".cl" && clTexts) {
        return clTexts.map((t) => ({ textContent: t }));
      }
      return [];
    },
  };
}

test("preserves intentional blank lines in standard Chroma fenced blocks", () => {
  const clTexts = [
    "class BranchContext(Context):\n",
    "    def site_address(self):\n",
    '        return ""\n',
    "\n",
    "    def validate_site_pattern(self):\n",
    '        if self["rack_units"] < 2:\n',
    "            raise DesignValidationError()\n",
  ];
  const codeEl = makeNode(clTexts.join(""), { clTexts });
  const highlightDiv = makeNode("", { children: { "code[data-lang]": codeEl } });

  const expected = [
    "class BranchContext(Context):",
    "    def site_address(self):",
    '        return ""',
    "",
    "    def validate_site_pattern(self):",
    '        if self["rack_units"] < 2:',
    "            raise DesignValidationError()",
  ].join("\n");

  assert.equal(extractCodeText(highlightDiv), expected);
});

test("preserves multiple consecutive blank lines", () => {
  const clTexts = ["a = 1\n", "\n", "\n", "b = 2\n"];
  const codeEl = makeNode(clTexts.join(""), { clTexts });
  const highlightDiv = makeNode("", { children: { "code[data-lang]": codeEl } });

  assert.equal(extractCodeText(highlightDiv), "a = 1\n\n\nb = 2");
});

test("ignores inline line-number spans when .cl spans exist", () => {
  const clTexts = ["first:\n", "\n", "second:\n"];
  // Raw textContent would include line numbers "1first:\n2\n3second:\n"
  const codeEl = makeNode("1first:\n2\n3second:\n", { clTexts });
  const highlightDiv = makeNode("", { children: { "code[data-lang]": codeEl } });

  assert.equal(extractCodeText(highlightDiv), "first:\n\nsecond:");
});

test("prefers the code column for linenos=table blocks", () => {
  const clTexts = ["- name: allocate\n", "  hosts: all\n"];
  const tableCodeEl = makeNode(clTexts.join(""), { clTexts });
  const highlightDiv = makeNode("1\n2\n- name: allocate\n  hosts: all\n", {
    children: { ".lntable .lntd:last-child code": tableCodeEl },
  });

  assert.equal(extractCodeText(highlightDiv), "- name: allocate\n  hosts: all");
});

test("falls back cleanly to code.textContent when no .cl spans exist", () => {
  const plainCodeEl = makeNode("echo hi\n\necho bye\n");
  const highlightDiv = makeNode("", { children: { code: plainCodeEl } });

  assert.equal(extractCodeText(highlightDiv), "echo hi\n\necho bye");
});

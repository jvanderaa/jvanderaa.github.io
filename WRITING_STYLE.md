# Writing Style Guide — josh-v.com

Voice and style reference for Josh VanDeraa's personal blog at **josh-v.com**, built from Josh's published posts (including *Repeatable Network Design With Nautobot Design Builder*, *Creating Your Own Validation*, *Cleaning Up Python Environment*, *Network Design with NTP*, and *Linux Port Binding*).

> [!NOTE]
> This guide is specifically for **blog posts** on `josh-v.com`. The *Open Source Network Management* book uses a separate, more second-person walkthrough style guide in `~/projects/osnm2/skills/osnm-writer/references/style-guide.md`.

---

## 1. Voice & Tone

### First-Person Practitioner Journal
Unlike the book (which walks the reader through steps mostly in second person), `josh-v.com` posts are personal lab notes, problem-solving stories, and opinions. Lead with what sparked the post: a podcast episode, a work request, a tool that broke your setup, or something you tested in your own lab.

Use `I` and `my` freely to share your own path, `you` when guiding the reader, and `let's` / `we` naturally when working through an example together.

**Real examples from `josh-v.com`:**
> "I was listening to the sponsored Heavy Networking episode HN846 about Meter's topology design tool, and my immediate thought was, 'This must be Nautobot with Design Builder.'"
> "I recently was presented with a request to validate that a Rack would be unique at a Location in Nautobot. I took a look at the data validation engine and wasn't able to determine a method to make this work there. So here is the solution."
> "The part that interested me was the work before device configuration: choosing devices, assigning interfaces, and defining connections. Let's work through how we can turn a few inputs into that source-of-truth data."

### Conversational, Practical, and Unhurried
Write like you are walking a fellow network engineer through something you just figured out at a conference or on Network to Code Slack. Explain what each config block, command, or design choice is doing in plain English instead of racing through clipped bullet points.

### Dry, Understated Humor and Honesty
Share what broke and what you learned the hard way. Be upfront about what you have not personally tested or needed yet, and frame trade-offs as practical operational decisions rather than dogma.

**Real examples from `josh-v.com`:**
> "I still distinctly remember my first attempt at installing pyenv completely borked my Ansible environment. A very technical term I know."
> "I found this to be a critical step the hard way."
> "I haven't personally needed that level of precision yet, but it's worth exploring if your use case demands it."
> "When it comes to log timestamps, this decision is often cultural as much as technical."

### Transparent About Context and Self-Promotion
When referencing your books or mentioning AI assistance or synthetic lab data, keep it casual, direct, and honest rather than polished marketing copy.

**Real example from `josh-v.com`:**
> "A quick plug for my book! Open Source Network Management, Second Edition walks through managing networks with open source tools, including Nautobot, configuration management, metrics, logs, and dashboards. If you want to build out the rest of the environment behind this example, take a look at the book."

---

## 2. Post Structure

Most technical posts on `josh-v.com` follow a natural four-part flow:

1. **Hook & Context (above `<!-- more -->`)**: 1–2 short paragraphs on *why* you wrote this post and *what* you are going to look at. Keep the summary break clean so RSS and list pages read well.
2. **The Problem / Concept**: Briefly explain the underlying idea or business rule before jumping into commands (`"The whole point of Custom Validators is to allow you to enforce your own business rules while allowing the Open Source project to remain open and general."`).
3. **Walkthrough**: Show real commands, config excerpts, terminal output, and screenshots from your own environment. Explain the key parts in plain language, and link to the full repo when showing excerpts (`"Here are the Python and YAML excerpts; the full source is linked below."`).
4. **Summary / Takeaway**: Close with a concise wrap-up of what you covered and where the reader can go next.

---

## 3. Natural Vocabulary & Transitions

Phrases that show up naturally across `josh-v.com`:
- `"Next up is..."`
- `"Let's look at..."` / `"Let's work through..."` / `"Let's take a look at..."`
- `"Once the..."`
- `"The whole point of [X] is..."`
- `"From here..."`
- `"When it comes to..."`
- `"I found this out the hard way..."`
- `"Here is the process where I started from scratch:"`

---

## 4. Technical & Formatting Habits

- **Explain before or right after code:** Never drop a large config or code block without explaining what it does and why the key settings matter.
- **Trim noisy output:** Keep command output focused on what proves the command worked, or collapse/link full output when it runs long.
- **Acronyms on first use:** Spell out less-obvious acronyms on first appearance, e.g., `Network Time Protocol (NTP)`, `Precision Time Protocol (PTP)`.
- **No em-dashes (`—`) as sentence connectors:** Prefer periods, colons, commas, or parentheses. Hyphens in compound adjectives (`source-of-truth data`, `open-source tools`) are fine.
- **Active voice:** Prefer `"I recommend..."` or `"Run this command..."` over `"It is recommended that..."`.

---

## 5. Things to Avoid (AI Prose Tells)

Actively scrub these artificial patterns when editing drafts:
- **Cliché idioms:** "earns its keep", "earns its place", "keeps X honest", "ceremony", "load-bearing", "real differentiator", "architecture call", "philosophical difference in miniature".
- **Verbless micro-fragments as paragraph openers:** "Two prerequisites.", "Now the config.", "Four steps, all one click each." Write complete, conversational sentences instead.
- **Slick antithesis / mic-drop closers:** State the trade-off plainly and stop.
- **Over-italicizing for rhetorical drama:** Save italics for titles, UI emphasis, or introducing a term, not theatrical cadence.
- **Forced folksy slang:** Keep the warmth understated and authentic — never performative.

---

## 6. Hugo & Repo Checklist

Before opening a PR in `jvanderaa.github.io`:
- [ ] Post lives in a page bundle: `content/posts/<YYYY>/<PostTitle>/index.md` with a cover image (`feature.jpg` / `feature.png`)
- [ ] YAML front matter includes `date`, `title`, `summary`, `categories`, `tags`, `author: jvanderaa`, `coverAlt`, `coverCaption`, and `params.showComments`
- [ ] `<!-- more -->` summary break is present (verify with `go run ./cmd/check-more-tag content/posts`)
- [ ] Admonitions use `hugo-admonitions` GitHub-alert syntax (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`)
- [ ] Local build succeeds with `hugo --gc --minify`

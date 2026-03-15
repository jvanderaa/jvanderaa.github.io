---
date: 2026-03-14
slug: ai-rss-fix
categories:
- life
- automation
- openclaw
title: "AI: The Quick RSS Feed Fix"
summary: >
  AI continues to help me take care of things that I have solved previously, but without having to have myself re-learn the exact details. I have solved RSS feed issues previously and understand how they work. Now I just want them to be working. So I turned to Harry to give a helping hand.
toc: true
tags:
  - ai
  - harry
author: jvanderaa
coverAlt: AI assistant repairing broken RSS feed connections
coverCaption: |
    Photo by Harry - The AI Aide System
params:
  showComments: true
---

Earlier in the day today I took notice that my RSS feeds were not working, most likely from when I made the migration from Material for MkDocs blog post over to the Hugo site. I'm still not regretting making the change. But I needed to take care of the issue. So instead of taking the time to check into what my RSS feed set up was, I wanted to just have the issue taken care of. So naturally I turned my attention over to Harry to help take care of this.

## Issue Identified - Too Many URLs

Over the years I have had two different feeds show up from my blogs, so a little bit of technical debt for sure. And I'm going to keep that debt in place most likely. It doesn't hurt too bad at this point. As I checked out my [Feedly](https://feedly.com) setup I saw that there were 2 URLs for the feeds and they both were not being found. So I copied and pasted the URLs from the Feedly URLs and asked Harry to figure out what needed to be done to solve this:

![Request to Harry to check a couple of URLs](request-light.png#light-mode "Conversation with Harry to check on the feed URLs.")
![Request to Harry to check a couple of URLs](request-dark.png#dark-mode "Conversation with Harry to check on the feed URLs.")

Harry immediately dove in and started to take a look at the URLs that were given, the Hugo configuration, and what would need to change in order to get the feeds to be working again. Harry provided me with a couple of options.

![Recommendations provided by Harry](recommendations-light.png#light-mode "Harry presented a couple of recommendations.")
![Recommendations provided by Harry](recommendations-dark.png#dark-mode "Harry presented a couple of recommendations.")

I actually audibled at this point to suggest that I wanted the pages to where they should be from a Hugo perspective, but also the pages that we had in the previous RSS feeds. At which point then Harry was off to the races.

## Harry - The Fix

After I opened up an [issue on GitHub](https://github.com/jvanderaa/jvanderaa.github.io/issues/265) with input from Harry. Harry was on it from there. Harry drafted a [PR](https://github.com/jvanderaa/jvanderaa.github.io/pull/266) for me to review. Once I approved the PR and merged, I passed that information along and Harry was then onto the verification stages.

> [!NOTE]+ Why Harry Doing This Work
> I could have done all of this on my own with the assistance, but I am pushing to see what we could enable and become eventual full self servicing.

The verification failed however. 

![Verfication - Failed](first_verification-light.png#light-mode "Verification - Failed")
![Verfication - Failed](first_verification-dark.png#dark-mode "Verification - Failed")

With the new information there, we had some conversation that clarified that the blog is now moved away from GitHub Pages and hosted on Cloudflare Pages. With that in mind a new suggestion came in that I was not aware of, but using [Cloudflare Redirects](https://developers.cloudflare.com/rules/url-forwarding/). And with that a follow on PR was on the way.

![Redirects Suggestion](redirects_suggestion-light.png#light-mode "Harry suggested using Cloudflare Redirects")
![Redirects Suggestion](redirects_suggestion-dark.png#dark-mode "Harry suggested using Cloudflare Redirects")

After the follow on PR that put everything into place, we now have all of the feeds being updated. I was able to confirm the following day on Feedly that the previous RSS feeds were now populating articles.

![Feedly Verification](feedly-light.png#light-mode "Feedly now showing articles since the move to Hugo.")
![Feedly Verification](feedly-dark.png#dark-mode "Feedly now showing articles since the move to Hugo.")

## Summary

Things are continuing to evolve and grow with having Harry working on things alongside. There are still many unknowns. And are things perfect yet? Not quite there. It will continue to be an evolution. But at this point, Harry is there working along side me.

>[!NOTE]- Why the name Harry?
> This was one that I asked my kids to help me out with. At this point it was their choice and it's good to give a name/personality to work alongside.

-Josh
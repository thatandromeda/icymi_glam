---
layout: home
---

[@ICYMI_GLAM](https://glammr.us/@icymi_glam) is a bot that boosts things that have been popular lately in the greater library world. It works better the more people follow it, but it respects user consent.

## FAQ

### How does it know what to boost?

It scans the timeline of users it's following for posts that meet the following criteria:
* they have been popular lately;
* their visibility is `public`;
* their users' bios do not include `#nobot` or `#noindex`.

### How does it decide whom to follow?

If you follow `@icymi_glam`, and your bio does _not_ include `#nobot` or `#noindex`, it will reply with a request to follow you. If you respond with "I consent", it will follow back.

### What if I don't want it to follow me any more?

If you unfollow it, it will unfollow you. Alternately, if you'd like to follow it but not have it scan your timeline, add `#nobot` or `#noindex` to your bio.

### Do I have to have an account on glammr.us to interact with the bot?

No. As long as glammr.us federates with your server, you're set.

### I'm the kind of nerd who wants to read the code in order to \{make my own, verify your claims, contribute a PR...\}

Cool, I love nerds! [Go for it.](https://github.com/thatandromeda/mastodon_digest)

### Who maintains this?

[Andromeda Yelton](https://ohai.social/@thatandromeda).

Standing on the shoulders of giants here, I've modified the code from [Mau Foronda's mastodon digest](https://github.com/mauforonda/mastodon_digest), which in turn was forked from [Matt Hodges' original](https://github.com/hodgesmr/mastodon_digest). All of us make heavy use of the pretty sweet [mastodon.py library](https://mastodonpy.readthedocs.io/).

### I \{have a question not represented here, want to report a bug, have an idea for a feature...\}

Get in touch with me on [mastodon](https://ohai.social/@thatandromeda) or [github](https://github.com/thatandromeda/mastodon_digest).

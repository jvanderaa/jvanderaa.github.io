from textwrap import dedent
import urllib.parse
import re

x_intent = "https://twitter.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
linkedin_sharer = "https://www.linkedin.com/cws/share/"
mastodon_share = "https://mastodonshare.com/"
bluesky_share = " https://bsky.app/intent/compose"
include = re.compile(r"posts/[1-9].*")

include_files = ["book.md", "nautobot_book.md"]
exclude_files = ["about.md", "links.md", "index.md"]

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']

    # if not include.match(page.url):
    #     return markdown

    page = kwargs['page']
    config = kwargs['config']
    file_name = page.file.src_path

    # Check if the page should be excluded
    if file_name in exclude_files:
        return markdown

    # Check if the page is in the posts directory or specific included files
    if not file_name.startswith("posts/") and file_name not in include_files:
        return markdown

    page_url = config.site_url+page.url
    page_title = urllib.parse.quote(page.title+'\n')

    return markdown + dedent(f"""\n
    [Share on :fontawesome-brands-linkedin-in:]({linkedin_sharer}?url={page_url}){{ .custom-share-button }}
    [Share on :simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .custom-share-button }}
    [Share on :simple-facebook:]({fb_sharer}?u={page_url}){{ .custom-share-button }}
    [Share on :fontawesome-brands-mastodon:]({mastodon_share}?url={page_url}){{ .custom-share-button }}
    [Share on :fontawesome-brands-bluesky:]({bluesky_share}?text={page_url}){{ .custom-share-button }}
    """)

---
authors: [jvanderaa]
comments: true
date: 2023-06-15
slug: moving-to-hugo
categories: ["blog"]
title: Moving to Hugo
toc: true
---

In this post I dive into more about my migration of the blog site to Hugo static content system. I will dive into primarily the why and how during this post. This also dives into the few changes that I had to make in order to make the change over from a Jekyll site to the Hugo site.

<!-- more -->

## Why Migrate?

While I do not have a ton of posts, I do have a few that I like to get out into the wild periodically. As I looked around the landscape of the blog pages these days, I was starting to see my page a bit dated. I had previously went with the Jekyll Minimal Mistakes theme. The theme itself was wonderful and quite extensible. However, one of my concerns besides the look was the lack of updates coming out on the theme. Not that I was going to be taking advantage of every new feature, there seems to have been a slow down.

The second reason is that I've been experimenting some more with GoLang and recently found a better understanding of how GoLang's templating engine works. Although admittedly as I write this, I know that I will need to re-learn again this as I have not put it into practice, and it is not completely native in my mind. But knowing how the templating language works, will allow me to be able to be more extensible for the site in the future. And when comparing wanting to learn Ruby templating vs GoLang templating. GoLang is definitely further on the list.

## Migration Activities

To make the migration, there were several steps that I had to take and one optional step that I took along the way.

* Migrate Jekyll to Hugo repo
  * There is a helpful Hugo migration script that will read a Jekyll blog organization and update the structure to Hugo
  * There were a few minor challenges with the migration, that it didn't take a few things into account that VS Code search was helpful for
* Update the existing markdown files for the new syntax
* Migration from GitLab Pages to GitHub Pages (Optional)

Let's go into a few of these topics.

## Migration from Jekyll to Hugo

I ended up doing a two parts on this. I followed the post here about doing so, which generally went well -  [https://chenhuijing.com/blog/migrating-from-jekyll-to-hugo/](https://chenhuijing.com/blog/migrating-from-jekyll-to-hugo/). I stopped after making the import to a repo named `migrate`. By doing this I had all of my data from the previous blog into a format for Hugo. On the repo that would become my GitHub Pages repository, I set up a new Hugo site using the `hugo` CLI tool. So that I would start fresh.

My fresh site I decided to go with the [Congo](https://github.com/jpanther/congo) theme. I had done some research on what themes were available and went with Congo for it's freshness and sharpness to it. The documentation provided as well for each of the settings went deep. In checking the repository I also found that it was being actively maintained. I definitely liked the idea that it was being updated.

### Blog Posts - Base

From there I moved a few of the markdown files into the new repository and ran the command `hugo server` to get a local instance up and running. Taking a look at the posts, things started working very quickly. I was able to see my latest posts and was able to explore changes to the layout rapidly.

### Blog Posts - Images

One of the biggest changes for me is that I went ahead and moved the images from the `assets` directory in the Jekyll world into the `static/images/` directory. This allowed me to change the URL path on the images to being `/images/{{ imageFilePath/Name }}`. Thankfully VS Code has a global find and replace that I was then able to replace all of the previous paths with that of the new path. And just like that the images were up and running.

### Blog Posts - Code Highlighting

Code highlighting was one of the bigger changes that I needed to accomplish in making the migration over from Jekyll. I had previously created some syntax highlighting with line numbers that were part of a Jekyll plugin. So my code looked like:

```
{% highlight yaml linenos %}
...YAML HERE ...
{% endhighlight %}
```

I used VS Code's Regex find and replace to help with this. I searched for:

```
\{% highlight (\w+) linenos %\}
```

And replaced it with the following, without the spaces between the braces (I need to figure out the Hugo escape method):

```
 { {< highlight $1 "linenos=table" >} }
```

The endhighlight section was much easier. That was done with just a find and replace of finding `{% endhighlight %}` with the replacement of the `{ {< /endhighlight >} }` command (again without the spaces between the braces).

At that point the code highlighting for multiple languages is complete.

### Blog Posts - Jinja Formatting

As part of the Jekyll formatting of the blog posts, the Ansible and Python Jinja formatting would get interpreted as a Jekyll template code. In order to get around that Jekyll had a `{% raw %}` with a corresponding {% endraw %} to allow for the Jinja formatting to show up. Well, now in Hugo and GoLang it would show up in the output. So this was a find and replace of both of those combinations and to remove them.

## Migration from GitLab Pages to GitHub Pages

Why I did this, this was more administrative than anything else. The rest of my world is done within GitHub with the open source projects that I work on. So this was a move that had a small bit of challenges. The primary piece was using GitHub Actions as the source of the GitHub Pages. I tried a few different combinations and in the end using the GitHub recommended Actions page when following the GitHub Pages set up, then GitHub Pages would get published.

My original reason for hosting on GitLab Pages was that GitLab Pages had supported HTTPS and custom domains. Both of these features have made their way into GitHub Pages at this point.

## Summary

So far I'm back pretty happy with the initial migration. The process is familiar and works well. The previewing capabilities are terrific. And I'm pretty happy with the cleaner interface.

Happy automating!

Josh
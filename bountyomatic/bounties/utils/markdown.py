import bleach
import markdown

# Global Vars
URLIZE_RE = '(%s)' % '|'.join([
    r'<(?:f|ht)tps?://[^>]*>',
    r'\b(?:f|ht)tps?://[^)<>\s]+[^.,)<>\s]',
    r'\bwww\.[^)<>\s]+[^.,)<>\s]',
    r'[^(<\s]+\.(?:com|net|org)\b',
])


class UrlizePattern(markdown.inlinepatterns.Pattern):
    """ Return a link Element given an autolink (`http://example/com`). """
    def handleMatch(self, m):
        url = m.group(2)

        if url.startswith('<'):
            url = url[1:-1]

        text = url

        if not url.split('://')[0] in ('http', 'https', 'ftp'):
            url = 'http://' + url

        el = markdown.util.etree.Element("a")
        el.set('href', url)
        el.set('target', '_blank')
        el.text = markdown.util.AtomicString(text)
        return el


class UrlizeExtension(markdown.Extension):
    """ Urlize Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace autolink with UrlizePattern """
        md.inlinePatterns['urlize'] = UrlizePattern(URLIZE_RE, md)
urlizeExtension = UrlizeExtension()


class BountyMarkdownExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['image_link']
        del md.inlinePatterns['image_reference']
bountyMarkdownExtension = BountyMarkdownExtension()


class CommentMarkdownExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['image_link']
        del md.inlinePatterns['image_reference']
commentMarkdownExtension = CommentMarkdownExtension()


def parse_bounty(raw_text):
    return markdown.markdown(
        bleach.clean(raw_text), [bountyMarkdownExtension], safe_mode='escape')


def parse_comment(raw_text):
    return markdown.markdown(
        bleach.clean(raw_text),
        [commentMarkdownExtension, urlizeExtension],
        safe_mode='escape')

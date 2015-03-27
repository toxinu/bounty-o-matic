import bleach
import markdown


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
        bleach.clean(raw_text), [commentMarkdownExtension], safe_mode='escape')

from packtools.sps.utils import xml_utils


class TOC:

    def __init__(self):
        self.sections = None
        self.documents = None

    def add_document_sections(self, doc_id, doc_sections):
        if not self.sections:
            self.sections = {}
        if not self.documents:
            self.documents = {}

        pairs = doc_sections.lang_text_pairs
        if pairs:
            lang_text_pairs_set = set(pairs)
            for lang_text_pair in pairs:
                self.sections.setdefault(lang_text_pair, set())
                self.sections[lang_text_pair].update(lang_text_pairs_set)
            self.documents[doc_id] = pairs[0]

    def group_by_lang(self, group_by_lang_and_text):
        docs = {}
        for doc_id, section_lang_and_text in self.documents.items():
            docs[doc_id] = [
                {"lang": lang, "text": text}
                for lang, text in self.sections[section_lang_and_text]
            ]
        return docs


class ArticleSubjectHeadings:
    """
    <article-categories>
        <subj-group subj-group-type="heading">
            <subject>Biotechnology</subject>
        </subj-group>
    </article-categories>
    """

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def items(self):
        return (
            [self.main_section] +
            self.subarticle_sections
        )

    @property
    def main_section(self):
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".", ".//subj-group[@subj-group-type='heading']/subject"):
            return {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
            }

    @property
    def subarticle_sections(self):
        _titles = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".//sub-article[@article-type='translation']",
                ".//subj-group[@subj-group-type='heading']/subject"):
            _title = {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
            }
            _titles.append(_title)
        return _titles

    @property
    def grouped_by_lang(self):
        return {
            item['lang']: item['text']
            for item in self.items
        }

    @property
    def lang_text_pairs(self):
        return [
            (item['lang'], item['text'])
            for item in self.items
        ]

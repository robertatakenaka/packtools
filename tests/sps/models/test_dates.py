import unittest
from unittest.mock import Mock, patch
from lxml import etree
from packtools.sps.models.article_and_subarticles import FulltextNode
from packtools.sps.models.dates import ArticleDates, FulltextDates, Date


class TestDate(unittest.TestCase):
    def setUp(self):
        self.xml = """
            <date>
                <year>2024</year>
                <month>01</month>
                <day>02</day>
                <season>Winter</season>
            </date>
        """
        self.node = etree.fromstring(self.xml)
        self.date = Date(self.node)

    def test_complete_date(self):
        self.assertEqual(self.date.year, "2024")
        self.assertEqual(self.date.month, "01")
        self.assertEqual(self.date.day, "02")
        self.assertEqual(self.date.season, "Winter")

    def test_data_property(self):
        expected = {"year": "2024", "month": "01", "day": "02", "season": "Winter"}
        self.assertEqual(self.date.data, expected)

    def test_partial_date(self):
        xml = """
            <date>
                <year>2024</year>
                <month>01</month>
            </date>
        """
        node = etree.fromstring(xml)
        date = Date(node)
        expected = {"year": "2024", "month": "01"}
        self.assertEqual(date.data, expected)


class TestFulltextDates(unittest.TestCase):
    def setUp(self):
        self.xml = """
            <article>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                        <day>02</day>
                    </pub-date>
                    <pub-date date-type="collection">
                        <year>2024</year>
                        <month>01</month>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2023</year>
                            <month>12</month>
                            <day>01</day>
                        </date>
                        <date date-type="accepted">
                            <year>2023</year>
                            <month>12</month>
                            <day>15</day>
                        </date>
                    </history>
                </article-meta>
            </article>
        """
        self.xmltree = etree.fromstring(self.xml)
        self.dates = FulltextDates(self.xmltree)

    def test_epub_date(self):
        epub_date = self.dates.epub_date
        self.assertIsNotNone(epub_date)
        self.assertEqual(epub_date["year"], "2024")
        self.assertEqual(epub_date["month"], "01")
        self.assertEqual(epub_date["day"], "02")
        self.assertEqual(epub_date["type"], "pub")

    def test_collection_date(self):
        collection_date = self.dates.collection_date
        self.assertIsNotNone(collection_date)
        self.assertEqual(collection_date["year"], "2024")
        self.assertEqual(collection_date["month"], "01")
        self.assertEqual(collection_date["type"], "collection")

    def test_history_dates(self):
        history_dates = self.dates.history_dates_list
        self.assertEqual(len(history_dates), 2)

        received_date = next(d for d in history_dates if d["type"] == "received")
        self.assertEqual(received_date["year"], "2023")
        self.assertEqual(received_date["month"], "12")
        self.assertEqual(received_date["day"], "01")

        accepted_date = next(d for d in history_dates if d["type"] == "accepted")
        self.assertEqual(accepted_date["year"], "2023")
        self.assertEqual(accepted_date["month"], "12")
        self.assertEqual(accepted_date["day"], "15")

    def test_legacy_epub_date(self):
        xml = """
            <article>
                <article-meta>
                    <pub-date pub-type="epub">
                        <year>2024</year>
                        <month>01</month>
                    </pub-date>
                </article-meta>
            </article>
        """
        xmltree = etree.fromstring(xml)
        dates = FulltextDates(xmltree)
        epub_date = dates.epub_date
        self.assertIsNotNone(epub_date)
        self.assertEqual(epub_date["year"], "2024")
        self.assertEqual(epub_date["month"], "01")

    def test_missing_dates(self):
        xml = """
            <article>
                <article-meta>
                </article-meta>
            </article>
        """
        xmltree = etree.fromstring(xml)
        dates = FulltextDates(xmltree)
        self.assertIsNone(dates.epub_date)
        self.assertIsNone(dates.collection_date)
        self.assertEqual(dates.history_dates_list, [])


class TestArticleDates(unittest.TestCase):
    def setUp(self):
        self.xml = """
            <article>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                        <day>02</day>
                    </pub-date>
                </article-meta>
            </article>
        """
        self.xmltree = etree.fromstring(self.xml)
        self.article_dates = ArticleDates(self.xmltree)

    def test_delegation_to_fulltext_dates(self):
        self.assertEqual(
            self.article_dates.epub_date, self.article_dates.main_dates.epub_date
        )

    def test_invalid_attribute(self):
        with self.assertRaises(AttributeError):
            self.article_dates.invalid_attribute


import unittest
from unittest.mock import Mock, patch
from lxml import etree


class TestFulltextNode(unittest.TestCase):
    def setUp(self):
        xml = """
        <article xml:lang="pt" article-type="research-article">
            <sub-article id="s1" xml:lang="en" article-type="translation">
                <front-stub></front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(xml)
        self.article_node = FulltextNode(self.xmltree)
        self.sub_article_node = FulltextNode(self.xmltree.find(".//sub-article"))

    def test_fulltext_node_article(self):
        """Test FulltextNode properties for main article"""
        self.assertEqual(self.article_node.tag, "article")
        self.assertEqual(self.article_node.id, None)
        self.assertEqual(self.article_node.lang, "pt")
        self.assertEqual(self.article_node.article_type, "research-article")

    def test_fulltext_node_sub_article(self):
        """Test FulltextNode properties for sub-article"""
        self.assertEqual(self.sub_article_node.tag, "sub-article")
        self.assertEqual(self.sub_article_node.id, "s1")
        self.assertEqual(self.sub_article_node.lang, "en")
        self.assertEqual(self.sub_article_node.article_type, "translation")

    def test_fulltext_node_data_article(self):
        """Test data property for main article"""
        expected = {
            "tag": "article",
            "id": None,
            "lang": "pt",
            "article_type": "research-article",
        }
        self.assertDictEqual(self.article_node.data, expected)

    def test_fulltext_node_data_sub_article(self):
        """Test data property for sub-article"""
        expected = {
            "tag": "sub-article",
            "id": "s1",
            "lang": "en",
            "article_type": "translation",
        }
        self.assertDictEqual(self.sub_article_node.data, expected)


class TestFulltextDatesSubArticles(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        xml = """
        <article xml:lang="pt" article-type="research-article">
            <sub-article id="s1" xml:lang="en" article-type="translation">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>05</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2022</year>
                            <month>11</month>
                            <day>10</day>
                        </date>
                        <date date-type="accepted">
                            <year>2023</year>
                            <month>02</month>
                            <day>15</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(xml)
        self.subarticle = self.xmltree.find(".//sub-article")
        self.dates = FulltextDates(self.subarticle)

    def test_sub_article_data(self):
        """Test parent data from FulltextNode is correctly inherited"""
        expected_parent = {
            "tag": "sub-article",
            "id": "s1",
            "lang": "en",
            "article_type": "translation",
        }
        self.assertEqual(self.dates.data["parent"], expected_parent)

    def test_sub_article_epub_date(self):
        """Test epub date extraction includes parent data"""
        epub_date = self.dates.epub_date
        expected = {
            "year": "2023",
            "month": "05",
            "day": "01",
            "type": "pub",
            "parent": {
                "tag": "sub-article",
                "id": "s1",
                "lang": "en",
                "article_type": "translation",
            }
        }
        self.assertDictEqual(epub_date, expected)

    def test_sub_article_history_dates(self):
        """Test history dates include parent data"""
        history_dates = self.dates.history_dates_list
        expected = [
            {
                "year": "2022",
                "month": "11",
                "day": "10",
                "type": "received",
                "parent": {
                    "tag": "sub-article",
                    "id": "s1",
                    "lang": "en",
                    "article_type": "translation",
                },
            },
            {
                "year": "2023",
                "month": "02",
                "day": "15",
                "type": "accepted",
                "parent": {
                    "tag": "sub-article",
                    "id": "s1",
                    "lang": "en",
                    "article_type": "translation",
                },
            },
        ]
        self.assertEqual(len(history_dates), 2)
        for expected_date, actual_date in zip(expected, history_dates):
            self.assertDictEqual(expected_date, actual_date)

    def test_sub_article_data_complete(self):
        """Test full data method output includes all required fields"""
        data = self.dates.data
        expected_keys = {
            "parent",  # Base FulltextNode data
            "pub",  # Date specific data
            "article_date",
            "collection_date",
            "history_dates",
            "translations_data",
            "subdocs_data",
            "received",  # History dates
            "accepted",
        }
        self.assertEqual(set(data.keys()), expected_keys)


class TestTranslationsAndSubArticles(unittest.TestCase):
    def setUp(self):
        self.xml = """
        <article xml:lang="pt" article-type="research-article">
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>04</month>
                        <day>17</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2022</year>
                            <month>10</month>
                            <day>08</day>
                        </date>
                    </history>
                </article-meta>
            </front>
            <sub-article id="s1" xml:lang="en" article-type="translation">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59553</article-id>
                    <title-group>
                        <article-title>The Dance Body as an Arena of Values</article-title>
                    </title-group>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>05</month>
                        <day>01</day>
                    </pub-date>
                </front-stub>
            </sub-article>
            <sub-article id="s2" xml:lang="es" article-type="reviewer-report">
                <front-stub>
                    <title-group>
                        <article-title>Parecer I</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.xml)
        self.dates = FulltextDates(self.xmltree)

    def test_translations_property(self):
        """Test that translations property returns only translation sub-articles with correct data"""
        translations = self.dates.translations

        self.assertEqual(len(translations), 1)
        self.assertIn("s1", translations)

        translation = translations["s1"]
        self.assertEqual(translation.fulltext_node.get("article-type"), "translation")
        self.assertEqual(translation.data["parent"]["lang"], "en")

    def test_subdocs_property(self):
        """Test that subdocs property returns non-translation sub-articles with correct data"""
        subdocs = self.dates.subdocs

        self.assertEqual(len(subdocs), 1)
        self.assertIn("s2", subdocs)

        review = subdocs["s2"]
        self.assertEqual(review.fulltext_node.get("article-type"), "reviewer-report")
        self.assertEqual(review.data["parent"]["lang"], "es")

    def test_main_article_data(self):
        """Test main article data includes proper parent information"""
        data = self.dates.data
        expected_parent = {
            "tag": "article",
            "id": None,
            "lang": "pt",
            "article_type": "research-article",
        }
        self.assertEqual(data["parent"], expected_parent)

    def test_translations_data_structure(self):
        """Test translations data includes proper parent information"""
        data = self.dates.data["translations_data"]
        translation_data = data["s1"]

        self.assertEqual(translation_data["parent"]["tag"], "sub-article")
        self.assertEqual(translation_data["parent"]["id"], "s1")
        self.assertEqual(translation_data["parent"]["lang"], "en")
        self.assertEqual(translation_data["parent"]["article_type"], "translation")


class TestFulltextDatesItems(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.xml = """
        <article xml:lang="pt" article-type="research-article">
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>04</month>
                        <day>17</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2022</year>
                            <month>10</month>
                            <day>08</day>
                        </date>
                    </history>
                </article-meta>
            </front>
            <sub-article id="s1" xml:lang="en" article-type="translation">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>05</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2022</year>
                            <month>11</month>
                            <day>10</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
            <sub-article id="s2" xml:lang="es" article-type="reviewer-report">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2023</year>
                        <month>06</month>
                        <day>01</day>
                    </pub-date>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.xml)
        self.dates = FulltextDates(self.xmltree.find("."))

    def test_items_generator(self):
        """Test that items returns a generator"""
        items = self.dates.items
        self.assertTrue(hasattr(items, "__iter__"))
        self.assertTrue(hasattr(items, "__next__"))

    def test_main_article_items(self):
        """Test first item represents main article data"""
        first_item = next(self.dates.items)
        expected = {
            "parent": {
                "tag": "article",
                "id": None,
                "lang": "pt",
                "article_type": "research-article",
            },
            "pub": {
                "year": "2023",
                "month": "04",
                "day": "17",
                "type": "pub",
                "parent": {
                    "tag": "article",
                    "id": None,
                    "lang": "pt",
                    "article_type": "research-article",
                },
            },
            "article_date": {
                "year": "2023",
                "month": "04",
                "day": "17",
                "type": "pub",
                "parent": {
                    "tag": "article",
                    "id": None,
                    "lang": "pt",
                    "article_type": "research-article",
                },
            },
            "collection_date": None,
            "history_dates": [
                {
                    "year": "2022",
                    "month": "10",
                    "day": "08",
                    "type": "received",
                    "parent": {
                        "tag": "article",
                        "id": None,
                        "lang": "pt",
                        "article_type": "research-article",
                    },
                }
            ],
            "received": {
                "year": "2022",
                "month": "10",
                "day": "08",
                "type": "received",
                "parent": {
                    "tag": "article",
                    "id": None,
                    "lang": "pt",
                    "article_type": "research-article",
                },
            },
        }
        self.assertDictEqual(first_item, expected)

    def test_translation_items(self):
        """Test translation sub-article data is yielded correctly"""
        items = list(self.dates.items)
        translation_data = next(
            item for item in items if item.get("parent", {}).get("id") == "s1"
        )

        self.assertEqual(translation_data["parent"]["article_type"], "translation")
        self.assertEqual(translation_data["pub"]["year"], "2023")
        self.assertEqual(translation_data["pub"]["month"], "05")
        self.assertEqual(translation_data["received"]["year"], "2022")
        self.assertEqual(translation_data["received"]["month"], "11")

    def test_reviewer_report_items(self):
        """Test reviewer report sub-article data is yielded correctly"""
        items = list(self.dates.items)
        review_data = next(
            item for item in items if item.get("parent", {}).get("id") == "s2"
        )

        self.assertEqual(review_data["parent"]["article_type"], "reviewer-report")
        self.assertEqual(review_data["pub"]["year"], "2023")
        self.assertEqual(review_data["pub"]["month"], "06")
        self.assertEqual(review_data["history_dates"], [])

    def test_items_count(self):
        """Test correct number of items are yielded"""
        items = list(self.dates.items)
        # Should have main article + translation + reviewer report
        self.assertEqual(len(items), 3)

    def test_items_order(self):
        """Test items are yielded in correct order"""
        items = list(self.dates.items)
        ids = [item.get("parent", {}).get("id") for item in items]
        expected_order = [None, "s1", "s2"]
        self.assertEqual(ids, expected_order)

    def test_empty_article_items(self):
        """Test items behavior with empty article"""
        xml = """
        <article xml:lang="pt" article-type="research-article">
            <front>
                <article-meta></article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        dates = FulltextDates(xmltree)
        items = list(dates.items)

        self.assertEqual(len(items), 1)  # Only main article data
        self.assertIsNone(items[0]["pub"])
        self.assertEqual(items[0]["history_dates"], [])


if __name__ == "__main__":
    unittest.main()

from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils

from packtools.sps.validation.article_authors import ArticleAuthorsValidation

credit_taxonomy_terms_and_urls = [
    {
        "term": "Conceptualization",
        "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
    },
    {
        "term": "Data curation",
        "uri": "https://credit.niso.org/contributor-roles/data-curation/",
    }
]


class ArticleAuthorsValidationTest(TestCase):
    def test_without_role(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_and_content_type_empty(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role></role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role></role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">None</role>',
                'message': '''Got <role content-type="None">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">None</role>',
                'message': '''Got <role content-type="None">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_without_content_type(self):
        self.maxDiff = None
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>VENEGAS-MARTÍNEZ</surname>
                                    <given-names>FRANCISCO</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1"/>
                                <role>Data curation</role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role>Conceptualization</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">Data curation</role>',
                'message': '''Got <role content-type="None">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">Conceptualization</role>',
                'message': '''Got <role content-type="None">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_no_text_with_content_type(self):
        self.maxDiff = None
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>VENEGAS-MARTÍNEZ</surname>
                                    <given-names>FRANCISCO</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1"/>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/"></role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_wrong_role_and_content_type(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_success_role(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)


class ArticleAuthorsValidationOrcidTest(TestCase):
    def test_validation_format_orcid(self):
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-01-58-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">00-0001-5518-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                "result": "error",
                "error_type": "Format invalid",
                "message": "The author FRANCISCO VENEGAS-MARTÍNEZ has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).",
                "author": {
                    "surname": "VENEGAS-MARTÍNEZ",
                    "prefix": "Prof",
                    "suffix": "Nieto",
                    "given_names": "FRANCISCO",
                    "orcid": "0990-01-58-4853",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
            {
                "result": "error",
                "error_type": "Format invalid",
                "message": "The author Vanessa M. Higa has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).",
                "author": {
                    "surname": "Higa",
                    "given_names": "Vanessa M.",
                    "orcid": "00-0001-5518-4853",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
        ]
        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_without_orcid(self):
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                "result": "error",
                "error_type": "Orcid not found",
                "message": "The author FRANCISCO VENEGAS-MARTÍNEZ does not have an orcid. Please add a valid orcid.",
                "author": {
                    "surname": "VENEGAS-MARTÍNEZ",
                    "prefix": "Prof",
                    "suffix": "Nieto",
                    "given_names": "FRANCISCO",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
            {
                "result": "error",
                "error_type": "Orcid not found",
                "message": "The author Vanessa M. Higa does not have an orcid. Please add a valid orcid.",
                "author": {
                    "surname": "Higa",
                    "given_names": "Vanessa M.",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_success_orcid(self):
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                "result": "success",
                "message": "The author FRANCISCO VENEGAS-MARTÍNEZ has a valid orcid.",
                "author": {
                    "surname": "VENEGAS-MARTÍNEZ",
                    "prefix": "Prof",
                    "suffix": "Nieto",
                    "given_names": "FRANCISCO",
                    "orcid": "0990-0001-0058-4853",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
            {
                "result": "success",
                "message": "The author Vanessa M. Higa has a valid orcid.",
                "author": {
                    "surname": "Higa",
                    "given_names": "Vanessa M.",
                    "orcid": "0000-3333-1238-6873",
                    "rid": ["aff1"],
                    "rid-aff": ["aff1"],
                    "aff_rids": ["aff1"],
                    "contrib-type": "author",
                },
            },
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

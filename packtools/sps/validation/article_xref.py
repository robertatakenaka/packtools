from packtools.sps.models.v2.article_xref import ArticleXref
from packtools.sps.validation.utils import format_response


class ArticleXrefValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article_xref = ArticleXref(xml_tree)
        self.elements_requires_xref_rid = (
            "fig",
            "disp-formula",
            "table-wrap",
            "ref",
        )
        ids = set(self.article_xref.elems_by_id("*").keys())
        rids = set(self.article_xref.xrefs_by_rid().keys())

        self.missing_xrefs = list(ids - rids)
        self.missing_elems = list(rids - ids)

    def validate_xref_rid_has_corresponding_element_id(self, error_level="ERROR"):
        """
            Checks if all `rid` attributes (source) in `<xref>` elements have corresponding `id` attributes (destination)
            in the XML document.

        Parameters
        ----------
        element_name : str
            The name of the element to be validated.
        error_level : str, optional
            The level of error reporting (default is "ERROR").

        Yields
        ------
        dict
            A dictionary containing the following keys:
            - title (str): The title of the validation.
            - xpath (str): The XPath query used to locate the elements being validated.
            - validation_type (str): The type of validation being performed (e.g., "match").
            - response (str): The result of the validation ("OK" or "ERROR").
            - expected_value (str): The expected `rid` value.
            - got_value (str or None): The actual value found or `None` if not found.
            - message (str): A message explaining the result of the validation.
            - advice (str): A recommendation or advice based on the validation result.
            - error_level (str): The level of error reporting.
            - data (dict): Additional data related to the validation context, which includes:
                - parent (str): The parent element's tag.
                - parent_id (str or None): The `id` of the parent element, if available.
                - parent_article_type (str): The type of the article (e.g., "research-article").
                - parent_lang (str): The language of the parent element.
                - tag (str): The tag of the element being validated.
                - attributes (dict): A dictionary of the element's attributes.
        """

        elements_by_id = self.article_xref.elems_by_id("*")
        for rid, xrefs in self.article_xref.xrefs_by_rid().items():
            for xref in xrefs:
                element_data = elements_by_id.get(rid)
                is_valid = bool(element_data)
                element_name = xref.get("element_name") or element_data.get("tag")
                ref_type = xref.get("ref-type")
                if ref_type:
                    ref_type_attr = f' ref-type="{ref_type}"'
                else:
                    ref_type_attr = ''

                xref_content = xref.get("content")
                advice = (
                    f'Found <xref rid="{rid}"{ref_type_attr}>{xref_content}</xref>, but not found the corresponding <{element_name} id="{rid}">. Check if the value id="" and rid="" are correct'
                )

                yield format_response(
                    title=f'<xref> is linked to <{element_name}>',
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=f'{element_name} which id="{rid}"',
                    obtained=element_data,
                    advice=advice,
                    data={"xref": xref, "element": element_data, "missing_xrefs": self.missing_xrefs, "missing_elems": self.missing_elems},
                    error_level=error_level,
                )

    def validate_element_id_has_corresponding_xref_rid(self, elements_requires_xref_rid=None, error_level="ERROR"):
        """
            Checks if all `id` attributes (destination) in the XML document have corresponding `rid` attributes (source)
            in `<xref>` elements.

        Parameters
        ----------
        element_name : str
            The name of the element to be validated.
        error_level : str, optional
            The level of error reporting (default is "ERROR").

        Yields
        ------
        dict
            A dictionary containing the following keys:
            - title (str): The title of the validation.
            - xpath (str): The XPath query used to locate the elements being validated.
            - validation_type (str): The type of validation being performed (e.g., "match").
            - response (str): The result of the validation ("OK" or "ERROR").
            - expected_value (str): The expected `id` value.
            - got_value (str or None): The actual value found or `None` if not found.
            - message (str): A message explaining the result of the validation.
            - advice (str): A recommendation or advice based on the validation result.
            - error_level (str): The level of error reporting.
            - data (dict): Additional data related to the validation context, which includes:
                - parent (str): The parent element's tag.
                - parent_id (str or None): The `id` of the parent element, if available.
                - parent_article_type (str): The type of the article (e.g., "research-article").
                - parent_lang (str): The language of the parent element.
                - tag (str): The tag of the element being validated.
                - attributes (dict): A dictionary of the element's attributes.
        """
        elements_requires_xref_rid = self.elements_requires_xref_rid

        default_error_level = error_level
        xrefs_by_rid = self.article_xref.xrefs_by_rid()


        for id, elems in self.article_xref.elems_by_id("*").items():
            for elem_data in elems:
                tag = elem_data.get("tag")
                if tag in elements_requires_xref_rid:
                    error_level = "CRITICAL"
                    expectation = "must"
                else:
                    error_level = default_error_level
                    expectation = "can"
                
                xrefs = xrefs_by_rid.get(id)
                is_valid = bool(xrefs)
                ref_type = elem_data.get("ref-type")
                label = elem_data.get("label")

                advice = (
                    f'Found <{tag} id="{id}">, but no corresponding <xref rid="{id}" ref-type="{ref_type}"> found. '
                    f'Mark {label}, mention to <{tag} id="{id}">, with <xref rid="{id}" ref-type="{ref_type}">'
                )
                yield format_response(
                    title=f'<{tag}> is linked to <xref>',
                    parent=elem_data.get("parent"),
                    parent_id=elem_data.get("parent_id"),
                    parent_article_type=elem_data.get("parent_article_type"),
                    parent_lang=elem_data.get("parent_lang"),
                    item=elem_data.get("tag"),
                    sub_item="@id",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=f'<xref rid="{id}" ref-type="{ref_type}">',
                    obtained=xrefs,
                    advice=advice,
                    data={"element": elem_data, "xref": xrefs, "missing_xrefs": self.missing_xrefs, "missing_elems": self.missing_elems},
                    error_level=error_level,
                )

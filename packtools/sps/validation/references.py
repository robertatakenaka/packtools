from packtools.sps.models.references import XMLReferences
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationReferencesException
from packtools.sps.validation.utils import build_response, get_future_date


class ReferenceValidation:
    def __init__(self, reference_data, params):
        self.reference_data = reference_data
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.publication_type_list = list(self.params["publication_type_requires"].keys())
        self.requires = self.params["publication_type_requires"].get(self.publication_type) or ["source", "year"]

    @property
    def publication_type(self):
        return self.reference_data.get("publication_type")

    @property
    def reference(self):
        return self.reference_data.get("ref_id") or self.reference_data.get("mixed_citation") or self.reference_data

    def get_default_params(self):
        return {
            # Error levels for different validations
            "year_error_level": "ERROR",
            "source_error_level": "ERROR",
            "article_title_error_level": "ERROR",
            "authors_error_level": "ERROR",
            "publication_type_error_level": "ERROR",
            "comment_error_level": "ERROR",
            "mixed_citation_sub_tags_error_level": "ERROR",
            "mixed_citation_error_level": "ERROR",
            "title_tag_by_dtd_version_error_level": "ERROR",

            # Allowed tags in mixed citations
            "allowed_tags": [
                "bold",
                "italic",
                "sup",
                "sub",
                "ext-link",
                # "named-content"
            ],
            
            "dtd_version": "1.1"  # Default DTD version
        }

    def _validate_item(
        self,
        label,
        item_name,
        element_name=None,
        valid=None,
        advice=None,
        expected=None,
        error_level=None,
        validation_type=None,
    ):
        value = self.reference_data.get(item_name)
        element_name = element_name or item_name
        advice = advice or f"Mark {label} with <{element_name}>"
        expected = expected or f"reference {element_name}"

        advice = f'{self.reference} : {advice}'

        if valid is None:
            valid = bool(value)
        yield build_response(
            title=f"reference {element_name}",
            parent=self.reference_data,
            item="element-citation",
            sub_item=element_name,
            is_valid=valid,
            validation_type=validation_type or "exist",
            expected=expected,
            obtained=value,
            advice=advice,
            data=self.reference_data,
            error_level=error_level,
        )

    def validate_year(self):
        # data do artigo que cita a referência
        end_year = self.reference_data["citing_pub_year"]
        if not end_year:
            raise ValueError("ReferenceValidation.validate_year requires valid value for end_year")
        year = self.reference_data.get("year")
        try:
            is_valid = int(year) <= int(end_year)
        except (TypeError, ValueError):
            is_valid = False

        if year:
            advice = (
                f"Mark the reference year ({year}) with <year> and it must be previous or equal to {end_year}"
            )
            expected = f"reference year ({year}) <= {end_year}"
        else:
            advice = (
                f"Mark the reference year with <year> and it must be previous or equal to {end_year}"
            )
            expected = f"reference year <= {end_year}"
        yield from self._validate_item(
            "reference year",
            "year",
            valid=is_valid,
            advice=advice,
            expected=expected,
            error_level=self.params["year_error_level"],
            validation_type="format"
        )

    def validate_source(self):
        if "source" in self.requires:
            yield from self._validate_item(
                "reference source",
                "source", error_level=self.params["source_error_level"])

    def validate_article_title(self):
        if "article-title" in self.requires:
            article_title = self.reference_data.get("article_title")
            yield from self._validate_item(
                "article title",
                "article_title", "article-title", error_level=self.params["article_title_error_level"])

    def validate_authors(self):
        if "person-group" in self.requires:
            number_authors = (
                len(self.reference_data.get("all_authors"))
                if self.reference_data.get("all_authors")
                else 0
            )
            valid = number_authors > 0
            yield from self._validate_item(
                "reference authors",
                "all_authors",
                element_name="person-group//name or person-group//collab",
                valid=valid,
                advice=f'Mark reference authors with <name> (person) or <collab> (institutional)',
                error_level=self.params["authors_error_level"],
            )

    def validate_publication_type(self):
        publication_type_list = self.publication_type_list
        error_level = self.params["publication_type_error_level"]
        if publication_type_list is None:
            raise ValidationReferencesException(
                "Function requires list of publications type"
            )
        publication_type = self.publication_type
        valid = publication_type in publication_type_list
        advice = (
            f'Complete publication-type="" in <element-citation publication-type=""> with valid value: {publication_type_list}'
        )
        yield from self._validate_item(
            "reference type",
            "publication_type", advice=advice,
            error_level=error_level, expected=publication_type_list, validation_type="value in list"
        )

    def validate_comment_is_required_or_not(self):
        comment = self.reference_data.get("comment_text", {})
        text_before_extlink = self.reference_data.get("text_before_extlink")

        ext_link_text = comment.get("ext_link_text")
        full_comment = comment.get("full_comment")
        text_between = comment.get("text_between")
        has_comment = comment.get("has_comment")

        scenarios = [
            {
                "condition": has_comment and not full_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"<comment></comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": f"Wrap {text_before_extlink}<ext-link>{ext_link_text}</ext-link> with <comment> tag",
            },
            {
                "condition": has_comment
                and not full_comment
                and not text_before_extlink,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment></comment><ext-link>{ext_link_text}</ext-link>",
                "advice": "Remove the <comment> tag because there is no text before <ext-link>",
            },
            {
                "condition": not has_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": f"Wrap the {text_before_extlink}<ext-link>{ext_link_text}</ext-link> with <comment> tag",
            },
            {
                "condition": full_comment and not text_between,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment><ext-link>{ext_link_text}</ext-link></comment>",
                "advice": "Remove the <comment> tag because there is no text before <ext-link>",
            },
        ]


        for scenario in scenarios:
            advice = scenario["advice"]
            advice = f'{self.reference} : {advice}'

            if scenario["condition"]:
                yield build_response(
                    title="comment is required or not",
                    parent=self.reference_data,
                    item="element-citation",
                    sub_item="comment",
                    is_valid=False,
                    validation_type="exist",
                    expected=scenario["expected"],
                    obtained=scenario["obtained"],
                    advice=advice,
                    data=self.reference_data,
                    error_level=self.params["comment_error_level"],
                )

    def validate_mixed_citation_sub_tags(self):
        allowed_tags = self.params["allowed_tags"]
        if found_sub_tags := self.reference_data.get("mixed_citation_sub_tags"):
            remaining_tags = list(set(found_sub_tags) - set(allowed_tags))
            if remaining_tags:
                yield build_response(
                    title="mixed-citation sub elements",
                    parent=self.reference_data,
                    item="mixed-citation",
                    sub_item=None,
                    is_valid=False,
                    validation_type="exist",
                    expected=allowed_tags,
                    obtained=self.reference_data.get("mixed_citation_sub_tags"),
                    advice=f"remove {remaining_tags} from mixed-citation",
                    data=self.reference_data,
                    error_level=self.params["mixed_citation_sub_tags_error_level"],
                )

    def validate_mixed_citation(self):
        valid = self.reference_data.get("mixed_citation")
        advice = f"{self.reference}: mark the full reference with <mixed-citation>"
        yield build_response(
            title="mixed-citation",
            parent=self.reference_data,
            item="mixed-citation",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="mixed-citation",
            obtained=None,
            advice=advice,
            data=self.reference_data,
            error_level=self.params["mixed_citation_error_level"],
        )

    def validate_title_tag_by_dtd_version(self):
        chapter_title = self.reference_data.get("chapter_title")
        try:
            dtd_version = float(self.params.get("dtd_version"))
        except ValueError:
            raise ValueError("Invalid DTD version: expected a numeric value.")

        if dtd_version >= 1.3 and bool(chapter_title):
            yield build_response(
                title="part-title",
                parent=self.reference_data,
                item="element-citation",
                sub_item="part-title",
                is_valid=False,
                validation_type="exist",
                expected="<part-title>",
                obtained="<chapter-title>",
                advice="Replace <chapter-title> with <part-title> to meet the required standard.",
                data=self.reference_data,
                error_level=self.params.get("title_tag_by_dtd_version_error_level"),
            )

    def validate(self):
        yield from self.validate_year()
        yield from self.validate_source()
        yield from self.validate_publication_type()
        yield from self.validate_article_title()
        yield from self.validate_authors()
        yield from self.validate_comment_is_required_or_not()
        yield from self.validate_mixed_citation_sub_tags()
        yield from self.validate_mixed_citation()
        yield from self.validate_title_tag_by_dtd_version()


class ReferencesValidation:
    def __init__(self, xml_tree, params):
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        xml_references = XMLReferences(self.xml_tree)

        for reference_data in xml_references.items:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()

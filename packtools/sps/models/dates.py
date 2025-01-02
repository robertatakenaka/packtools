class Date:
    """Represents and processes a single date from an XML node.
    
    This class handles the extraction and structuring of date information from XML nodes,
    supporting year, month, day and season data.
    
    Attributes:
        node: XML node containing date information
        year: Year value extracted from node
        season: Season value extracted from node
        month: Month value extracted from node 
        day: Day value extracted from node

    Example:
        date_node = article.find('.//pub-date')
        date = Date(date_node)
        date_dict = date.data
    """

    def __init__(self, node):
        """Initialize a Date instance with an XML node.
        
        Args:
            node: XML node containing date elements (year, month, day, season)
        """
        self.node = node
        self.year = node.findtext("year")
        self.season = node.findtext("season")
        self.month = node.findtext("month")
        self.day = node.findtext("day")

    @property
    def data(self):
        """Get date information as a dictionary.
        
        Returns a dictionary containing available date components (year, month, season, day).
        Only components that exist in the source XML are included.
        
        Returns:
            dict: Date information with available components
            
        Example:
            {'year': '2024', 'month': '01', 'day': '15'}
        """
        _date = {}
        for name in ("year", "month", "season", "day"):
            value = self.node.findtext(name)
            if value:
                _date[name] = value
        return _date


class FulltextDates:
    """Processes and provides access to all date-related data from articles and sub-articles.

    This class handles extraction and organization of dates from SPS XML documents,
    maintaining hierarchy and relationships between different date types.

    Attributes:
        fulltext_node: Root XML node for date extraction
        parent_data: Metadata about the parent article/sub-article
        context_node: XML node containing date information (article-meta or front-stub)
    """

    def __init__(self, fulltext_node):
        """Initialize a FulltextDates instance.
        
        Args:
            fulltext_node: XML node (article or sub-article) to process dates from
        """
        self.fulltext_node = fulltext_node
        self.parent_data = FulltextNode(fulltext_node).data
        if self.fulltext_node.tag == "article":
            self.context_node = self.fulltext_node.find(".//article-meta")
        else:
            self.context_node = self.fulltext_node.find("front-stub")

    @property
    def data(self):
        """Get all date information in a hierarchical structure.

        Returns a dictionary containing all date information maintaining the document's
        hierarchical structure, including parent metadata and related documents.

        Returns:
            dict: Complete hierarchical date information
            
        Example:
            {
                'parent': {...},
                'pub': {...},
                'article_date': {...},
                'collection_date': {...},
                'history_dates': [...],
                'translations_data': {...},
                'subdocs_data': {...}
            }
        """
        data = {}
        data["parent"] = self.parent_data
        data["pub"] = self.epub_date
        data["article_date"] = self.article_date
        data["collection_date"] = self.collection_date
        data["history_dates"] = self.history_dates_list
        data.update(self.history_dates_dict)
        data["translations_data"] = {
            k: v.data
            for k, v in self.translations.items()
        }
        data["subdocs_data"] = {
            k: v.data
            for k, v in self.subdocs.items()
        }
        return data

    @property
    def items(self):
        """Get date information in a flattened structure.
        
        Yields date information for the main document and all related documents
        (translations and subdocs) in a flat structure, simplifying data processing.
        
        Yields:
            dict: Flattened date information for each document part
            
        Example:
            for item in dates.items:
                print(f"Document ID: {item['parent']['parent_id']}")
                print(f"Pub date: {item['pub']}")
        """
        data = {}
        data["parent"] = self.parent_data
        data["pub"] = self.epub_date
        data["article_date"] = self.article_date
        data["collection_date"] = self.collection_date
        data["history_dates"] = self.history_dates_list
        data.update(self.history_dates_dict)
        yield data

        for k, item in self.translations.items():
            yield from item.items
        for k, item in self.subdocs.items():
            yield from item.items

    @property
    def epub_date(self):
        """Get electronic publication date.
        
        Extracts and processes the electronic publication date, handling both current
        (date-type='pub') and legacy (pub-type='epub') attributes.
        
        Returns:
            dict: Publication date information with type and parent data, or None if not found
            
        Example:
            {'year': '2024', 'month': '01', 'type': 'pub', 'parent': {...}}
        """
        try:
            date_node = self.context_node.xpath(".//pub-date[@date-type='pub']")[0]
        except IndexError:
            # handle legacy attribute pub-type
            try:
                date_node = self.context_node.xpath(".//pub-date[@pub-type='epub']")[0]
            except IndexError:
                return None
        data = Date(date_node).data
        data["type"] = "pub"
        data["parent"] = self.parent_data
        return data

    @property
    def article_date(self):
        """Get complete article publication date.
        
        Returns the complete publication date (including day) of the article on the website.
        Currently returns the same as epub_date.
        
        Returns:
            dict: Article publication date information
        """
        return self.epub_date

    @property
    def collection_date(self):
        """Get collection publication date.
        
        Extracts the collection publication date, handling both current 
        (date-type='collection') and legacy (pub-type='epub-ppub') attributes.
        
        Returns:
            dict: Collection date information with type and parent data, or None if not found
            
        Example:
            {'year': '2024', 'month': '01', 'type': 'collection', 'parent': {...}}
        """
        try:
            date_node = self.context_node.xpath(".//pub-date[@date-type='collection']")[0]
        except IndexError:
            # handle legacy attribute pub-type
            try:
                date_node = self.context_node.xpath(".//pub-date[@pub-type='epub-ppub']")[0]
            except IndexError:
                return None

        data = Date(date_node).data
        data["type"] = "collection"
        data["parent"] = self.parent_data
        return data

    @property
    def pub_dates(self):
        """Get all publication dates.
        
        Returns a list of all publication dates (epub and collection) available in the document.
        Handles legacy SPS versions (pre-1.8) for compatibility.
        
        Returns:
            list: List of publication dates (collection and/or epub)
            
        Notes:
            - AOP articles only have pub/epub date
            - Legacy XMLs might have only pub or only collection date
            - epub can represent article date (pub) or issue date (collection)
            - epub-ppub represents issue date (collection)
        """
        _dates = []
        if self.collection_date:
            _dates.append(self.collection_date)
        if self.epub_date:
            _dates.append(self.epub_date)
        return _dates

    @property
    def history_dates_list(self):
        """Get article history dates as a list.
        
        Extracts all history dates (received, accepted, etc.) from the document,
        adding type and parent information to each date.
        
        Returns:
            list: List of history dates with type and parent information
            
        Example:
            [
                {'year': '2023', 'month': '12', 'type': 'received', 'parent': {...}},
                {'year': '2024', 'month': '01', 'type': 'accepted', 'parent': {...}}
            ]
        """
        _dates = []
        for node in self.context_node.xpath(".//history//date"):
            type = node.get("date-type")
            _date = Date(node)
            data = _date.data
            data["parent"] = self.parent_data
            data["type"] = type
            _dates.append(data)
        return _dates

    @property
    def history_dates_dict(self):
        """Get article history dates as a dictionary.
        
        Converts the history dates list into a dictionary keyed by date type,
        providing easier access to specific history dates.
        
        Returns:
            dict: History dates indexed by date type
            
        Example:
            {
                'received': {'year': '2023', 'month': '12', ...},
                'accepted': {'year': '2024', 'month': '01', ...}
            }
        """
        _dates = {}
        for event_date in self.history_dates_list:
            _dates[event_date['type']] = event_date
        return _dates

    @property
    def translations(self):
        """Get article translations with their dates.
        
        Returns a dictionary of FulltextDates instances for each translation
        sub-article, indexed by translation ID.
        
        Returns:
            dict: Translation FulltextDates instances by ID
            
        Example:
            {'en': FulltextDates(...), 'es': FulltextDates(...)}
        """
        translations = {}
        for item in self.fulltext_node.xpath("./sub-article[@article-type='translation']"):
            translations[item.get("id")] = FulltextDates(item)
        return translations

    @property
    def subdocs(self):
        """Get supplementary documents with their dates.
        
        Returns a dictionary of FulltextDates instances for each non-translation
        sub-article, indexed by document ID.
        
        Returns:
            dict: Supplementary document FulltextDates instances by ID
            
        Example:
            {'suppl1': FulltextDates(...), 'suppl2': FulltextDates(...)}
        """
        subdocs = {}
        for item in self.fulltext_node.xpath("./sub-article[@article-type!='translation']"):
            subdocs[item.get("id")] = FulltextDates(item)
        return subdocs


class ArticleDates:
    """High-level interface to access article dates.
    
    Provides a convenient interface to access all date information from an article
    through delegation to FulltextDates.

    Attributes:
        xmltree: XML tree containing the article
        main_dates: FulltextDates instance for the main article
    """

    def __init__(self, xmltree):
        """Initialize an ArticleDates instance.
        
        Args:
            xmltree: XML tree containing the article to process
        """
        self.xmltree = xmltree
        self.main_dates = FulltextDates(xmltree.find("."))

    def __getattr__(self, name):
        """Delegate attribute access to main_dates.
        
        Provides access to FulltextDates attributes through ArticleDates.
        Raises AttributeError if the attribute doesn't exist.
        
        Args:
            name: Name of the attribute to access
            
        Returns:
            The requested attribute from main_dates
            
        Raises:
            AttributeError: If the attribute doesn't exist in ArticleDates or FulltextDates
        """
        if hasattr(self.main_dates, name):
            return getattr(self.main_dates, name)
        raise AttributeError(f"ArticleDates.{name} or FulltextDates.{name} does not exist")
    
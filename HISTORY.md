# History


## 2.6.12 (2021-03-25)

* Workaround the presence of `--` in a XML comment. Inherent problem of SGML languages (#254)
* Fix HTMLGenerator to transform `graphic` in `table` (#248)
* Fix HTMLGenerator to transform `inline-graphic` in `xref` (#250)


## 2.6.11 (2021-03-11)

* Generate HTML for abstracts, one for file, for Google Scholar Indexing.

## 2.6.10 (2020-12-07)

* Fix HTMLGenerator to show all the abstracts in each translated article page.

## 2.6.9 (2020-12-04)

* Generate modals to all images, even without id attribute.


## 2.6.8 (2020-11-30)

* Show collection date in the bibliographic strip for all documents types, except Ahead of Prints


## 2.6.7 (2020-10-20)

* Fix thumbnail in modal where elements are grouped in tabs.
* Generate modals to figs located in front, back and sub-article.


## 2.6.6 (2020-09-23)

* Check if there is thumbnail graphic alternative xlink:href before using it in HTMLGenerator.


## 2.6.5 (2020-08-31)

* Use of thumbnail graphic alternative to build HTML in HTMLGenerator.


## 2.6.4 (2020-06-16)

* WEB optimiser minor fix to not to externalize an error of one dependent library.


## 2.6.3 (2020-05-07)

* Changes XML reading in WEB optimiser to not to load DTD
* Preserves XML DOCTYPE after XML reading in WEB optimiser


## 2.6.2 (2020-04-13)

* Fixes XML WEB optimiser stop execution in case linked image file format are not supported
* Adds debug logs


## 2.6.1 (2020-04-08)

* SPS Package WEB optimiser code refactoring
* Adds option to stop execution if an error occurs during WEB package optimisation


## 2.6.0 (2020-02-18)

* Drop support for Python version 3.4.
* Ajustments to follow the Crossref DOI Display guidelines [https://www.crossref.org/display-guidelines/]
* Tool to optimise images for WEB in SPS Packages
* Initial support for SciELO PS version 1.10.


## 2.5.6 (2019-10-29)

* Fixes link to retracted articles in the HTML.
* Fixes the *how to cite* of documents that have collaborative authors.
* Adds Python 3.7 to the test matrix.
* Removes the dependency of `python-slugify`.


## 2.5.5 (2019-09-16)

* Adds highlight to a document retraction
  [https://github.com/scieloorg/packtools/pull/205].
* Adds support to partial retractions and minor improvements to labels
  [https://github.com/scieloorg/opac/issues/1406#issuecomment-524839144].


## 2.5.4 (2019-08-26)

* Shows DOIs for translations when available
  [https://github.com/scieloorg/opac/issues/1391],
  [https://github.com/scieloorg/packtools/pull/202].
* Shows history dates for sub-articles. 


## 2.5.3 (2019-08-14)

* Fixes the rendering of visual abstracts.
  [https://github.com/scieloorg/packtools/pull/200].


## 2.5.2 (2019-07-19)

* Minor fixes to the generated HTML.


## 2.5.1 (2019-05-22)

* Minor fixes to the generated HTML.


## 2.5 (2019-05-16)

* Adds the capability to run a webserver that provides a web-based interface
  for stylechecker and htmlgenerator.
* README.rst and HISTORY.rst were converted to Markdown.
* Change validation rules for `<pub-date>` on sps-1.8.
* Minor fixes to the generated HTML.


## 2.4.3 (2019-04-17)

* Minor fixes to the generated HTML
  [https://github.com/scieloorg/opac/issues/1276].


## 2.4.2 (2019-03-29)

* Add support to SciELO PS 1.9.
* Minor fixes to the generated HTML
  [https://github.com/scieloorg/packtools/pull/184].


## 2.4.1 (2019-03-20)

* Minor fixes and adjusts to the generated HTML
  [https://github.com/scieloorg/packtools/issues/168],
  [https://github.com/scieloorg/packtools/issues/169].


## 2.4 (2019-01-16)

* Makes possible to have plugable catalogs of validation schemas and xslts.
* Minor fixes and adjusts to the generated HTML.


## 2.3.8 (2018-12-03)

* Fixes a bug that would cause authors names to be ommited in the HTML version
  [https://github.com/scieloorg/packtools/issues/159]


## 2.3.7 (2018-07-17)

* Fixes a bug that would break the html generator
  [https://github.com/scieloorg/packtools/issues/157]


## 2.3.6 (2018-06-20)

* Fixes a bug on the distribution os xsl data files.


## 2.3.5 (2018-03-22)

* Fixes a bug that would cause affs to be mandatory for corrections and
  retractions.


## 2.3.4 (2018-03-21)

* Fixes support for SciELO PS 1.8.


## 2.3.3 (2018-03-15)

* Fixes support for SciELO PS 1.8 adding validations to affs and ref-lists.


## 2.3.2 (2018-03-14)

* Makes the validation of the response element more flexible.
* Adds more values to ``//product/@product-type``.
* Adds more values to ``//date/@date-type``.
* Adds SciELO BR specific rules.


## 2.3.1 (2018-03-05)

* Fixes a bug that would cause error messages on all sps-1.8 documents.


## 2.3 (2018-03-02)

* Initial support for SciELO PS 1.8.


## 2.2 (2018-02-02)

* Updates the HTMLGenerator to support the build of the most recent version of
  the articles in HTML.


## 2.1 (2017-09-28)

* Initial support for SciELO PS 1.7.
* Adds support to JATS 1.1. 
* Removes Python 3.3 and adds lxml 3.8 and 4.0 to the test matrix.


## 2.0.3 (2017-06-02)

* Fixes a bug that would cause ``etree.XMLParser`` to raise TypeError on
  some old versions of lxml.


## 2.0.2 (2017-05-16)

* Reduces the size of the test matrix so tests run on a reasonable amount of 
  time (the full matrix was taking almost 1 hour to run). Now we are testing
  against minor versions of lxml  3.4, 3.5 and 3.6 , except for 3.7.x 
  series where we also test patch versions.
* Fixes bug that would cause wheel distributions to handle dependencies
  incorrectly.


## 2.0.1 (2017-04-26)

* Fixes bugs and regressions.


## 2.0 (2017-04-25)

* [Backwards incompatible] Major changes on ``packtools.domain.XMLValidator``
  initializer and ``.parse`` classmethod. The param ``extra_schematron`` is 
  now deprecated. Use ``sch_schemas`` and ``extra_sch_schemas`` instead, since 
  both params accept an arbitrary number of schematron schemas.
* Validation logic was abstracted and moved to Validator objects
  (``packtools.domain.PyValidator``, ``packtools.domain.DTDValidator``, and 
  ``packtools.domain.SchematronValidator``).
* The stylechecker utility exits 0 on success, and >0 if an error occurs
  [https://github.com/scieloorg/packtools/issues/118].
* The values in attribute ``@country`` are checked against ISO3166 alpha-2 
  list.
* Fixes a bug that would cause element's text to be printed out on error 
  messages instead of the element's name
  [https://github.com/scieloorg/packtools/issues/123].
* [Backwards incompatible] Major changes to the data structure returned by 
  ``packtools.stylechecker.summarize`` and, as consequence, to the 
  JSON-encoded data structure produced by the stylechecker command-line tool
  [https://github.com/scieloorg/packtools/issues/75].
* The parsing of schematron schemas was accelerated by preventing the
  collection of the IDs in an auxiliary hash table
  [https://github.com/scieloorg/packtools/issues/109].


## 1.5 (2017-04-03)

* Initial support for SciELO PS 1.6.


## 1.4.2 (2017-03-22)

* This release is purely bureaucratic, because Pypi does not allow a package
  to be fixed and resubmitted with the same filename.


## 1.4.1 (2017-03-22)

* Fixes syntax error on HISTORY.rst that caused style problems on Pypi.


## 1.4 (2017-03-22)

* XML catalog to resolve system ids of type URL
  [https://github.com/scieloorg/packtools/issues/110].
* Remove the use license restrictions from the Brazil instance
  [https://github.com/scieloorg/packtools/issues/112].
* Make built-in schematron schemas available through the prefix `@`:
  @scielo-br, @sps-1.1, @sps-1.2, @sps-1.3, @sps-1.4, @sps-1.5.
* Better exception and log messages.


## 1.3.3 (2017-02-16)

* Fixes a bug that would cause invalid product types to be accepted on 
  ``article/front/article-meta/product/@product-type``.
* Fixes a bug that would cause invalid invalid values to be accepted on 
  ``article/front/article-meta/aff/institution/@content-type``.
* Clean up unused attributes from classes from the ``packtools.style_error`` 
  module. 
* Log messages are now omitted from the stderr by default. 
* Fixes a bug that would cause tests to fail on Python 3.6
  [https://github.com/scieloorg/packtools/issues/107].


## 1.3.2 (2016-11-22)

* Bugfix release
  [https://github.com/scieloorg/packtools/issues/101].


## 1.3.1 (2016-10-03)

* Bugfix release 
  [https://github.com/scieloorg/packtools/commit/36a0277e].


## 1.3 (2016-09-30)

* Added functions ``stylechecker.summarize`` and ``stylechecker.annotate``.
* Added zip-file validation capabilities.
* Initial support for SciELO PS 1.5.


## 1.2 (2016-04-04)

* Fixes a bug that would cause ``country`` elements to be mandatory on 
  sub-articles of type ``transation``. 
* HTMLGenerator().generate() method now handling undefined 
  ``article/@xml:lang`` attribute.


## 1.1 (2016-03-11)

* Initial support for SciELO PS 1.4.


## 1.0 (2016-02-23)

* Better debug information with ``stylechecker sysinfo`` option.
* Added scripts to handle registration of local xml catalog in the super catalog.
* New domain specific exceptions.
* The module ``packtools.xray`` was removed.
* Added support for automatic generation of HTML documents through 
  ``HTMLGenerator``.
* Backwards incompatible change in ``XMLValidator`` init method signature.


## 0.8.1 (2015-09-03)

* Fixe some issues that would cause invalid sps-1.3 XMLs to be considered valid.


## 0.8.0 (2015-08-31)

* Minor refactoring to make possible for the XMLValidator to handle deprecated 
  versions of SciELO PS.
* Added basic support to SciELO PS 1.3.


## 0.7.6 (2015-07-08)

* Fixed bug that would cause empty mandatory elements to be valid.


## 0.7.5 (2015-07-03)

* Added feature to run the validation against an external schematron schema 
  [#55].
* stylechecker's ``loglevel`` option accepts upper, lower or mixed case strings.
* stylechecker utility can read from stdin, so it can be a filter in unix 
  pipelines.
* Added ``raw`` option to stylechecker. 
* Fixed bug that would raise UnicodeDecodeError in the presence 
  of any non-ascii character in the path to the file (Python 2 on Windows only).


## 0.7.4 (2015-06-19)

* Fixed bug that would cause page counts to be reported as error when 
  pagination is identified with elocation-id [#51].
* Added support for creative commons IGO licenses (sps-1.2 only). 
* Fixed bug that would cause funding-group validation to raise false positives.


## 0.7.3 (2015-05-18)

* Validating the minimum set of elements required for references of type 
  journal [http://git.io/vUSp6].
* Added validation of //aff/country/@country attributes for XMLs under 
  sps-1.2 spec.


## 0.7.2 (2015-04-30)

* Fixes a bug in which the occurrence of empty award-id, 
  fn[@fn-type="financial-disclosure"] or ack could lead stylechecker to crash.


## 0.7.1 (2015-04-29)

* Fixes a bug that report *page-count* as invalid when fpage or lpage values 
  are non-digit.
* Fixes a bug that mark as invalid XMLs containing use-licenses with 
  https scheme or missing trailing slashes.
* Changes the funding-group validation algorithm. 
* Checking for funding-statement when fn[fn-type="financial-disclosure"] is 
  present.


## 0.7 (2015-03-13)

* Added SciELO PS 1.2 support.
* Added the apparent sourceline of the element raising validation errors 
  (stylechecker).
* Added the option *nocolors* to prevent stylechecker output from being 
  colorized by ANSI escape sequences.
* stylechecker now prints log messages to stdout. The option *loglevel* 
  should be used to define the log level. Options are: DEBUG, INFO, WARNING, 
  ERROR or CRITICAL.
* SciELO PS 1.2 schematron uses EXSLT querybinding.
* Better error handling while analyzing multiple XML files with stylechecker.


## 0.6.4 (2015-02-03)

* Fixes a bug that causes malfunctioning on stylechecker
  while expanding wildcards on windows.
* Major semantic changes at *assetsdir* options. Now it is always turned ON,
  and the option is used to set the lookup basedir. By default,
  the XML basedir is used.


## 0.6.3 (2015-02-02)

* stylechecker CLI utility overhaul:
    * The basic output is now presented as JSON structure. 
    * The option *assetsdir* lookups, in the given dir, for each asset referenced in
      XML. The *annotated* option now writes the output to a file. The
      utility now takes more than one XML a time.
    * *pygments*, if installed, will be used to display pretty JSON outputs.


## 0.6.2 (2015-01-23)

* Added method ``XMLValidator.lookup_assets``.
* Added property ``XMLValidator.assets``. 
* Fixed minor issue that would cause //element-citation[@publication-type="report"] 
  to be reported as invalid.
* Fixed minor issue that would erroneously identify an element-citation element 
  as not being child of element ref.


## 0.6.1 (2014-11-28)

* Minor fix to implement changes from SciELO PS 1.1.1.


## 0.6 (2014-10-28)

* Python 3 support.
* Project-wide code refactoring.
* ``packtools.__version__`` attribute to get the package version.
* Distinction between classes of error with the attribute ``StyleError.level``.


## 0.5 (2014-09-29)

* Basic implementation of XML style rules according to SciELO PS version 1.1.
* ``stylechecker`` and ``packbuilder`` console utilities.
* Major performance improvements on ``XMLValidator`` instantiation, when used
  with long-running processes (9.5x).


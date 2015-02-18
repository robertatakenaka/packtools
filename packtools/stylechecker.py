#coding: utf-8
from __future__ import print_function
import os
import argparse
import sys
import pkg_resources
import json
import glob
import logging

from lxml import etree
# import pygments if here
try:
    import pygments     # NOQA
    from pygments.lexers import get_lexer_for_mimetype
    from pygments.formatters import TerminalFormatter
except ImportError:
    pygments = False    # NOQA

import packtools


logger = logging.getLogger(__file__)


class XMLError(Exception):
    """ Represents errors that would block XMLValidator instance from
    being created.
    """

def prettify(jsonobj):
    """ Prettify JSON output.

    On windows, bypass pygments colorization.

    Function copied from Circus process manager:
    https://github.com/circus-tent/circus/blob/master/circus/circusctl.py
    """

    json_str = json.dumps(jsonobj, indent=2, sort_keys=True)
    if pygments and not sys.platform.startswith('win'):
        try:
            lexer = get_lexer_for_mimetype("application/json")
            return pygments.highlight(json_str, lexer, TerminalFormatter())
        except:
            pass

    return json_str


def get_xmlvalidator(xmlpath, no_network):
    try:
        parsed_xml = packtools.XML(xmlpath, no_network=no_network)
    except IOError:
        raise XMLError('Error reading %s. Make sure it is a valid file-path or URL.' % xmlpath)
    except etree.XMLSyntaxError as e:
        raise XMLError('Error reading %s. Syntax error: %s' % (xmlpath, e))

    try:
        xml = packtools.XMLValidator(parsed_xml)
    except ValueError as e:
        raise XMLError('Error reading %s. %s.' % (xmlpath, e))

    return xml


def summarize(validator, assets_basedir=None, verbose=False):

    def _make_err_message(err):
        """ An error message is comprised of the message itself and the
        element sourceline.
        """
        err_msg = {'message': err.message}

        try:
            err_element = err.get_apparent_element(validator.lxml)
        except ValueError:
            logger.info('Could not locate the element name in: %s' % err.message)
            err_element = None

        if verbose:
            if err_element is not None:
                err_msg['apparent_line'] = err_element.sourceline
                err_msg['apparent_snippet'] = etree.tostring(err_element, encoding='unicode')
            else:
                err_msg['apparent_line'] = None
                err_msg['apparent_snippet'] = None

        return err_msg


    dtd_is_valid, dtd_errors = validator.validate()
    sps_is_valid, sps_errors = validator.validate_style()

    summary = {
        'dtd_errors': [_make_err_message(err) for err in dtd_errors],
        'sps_errors': [_make_err_message(err) for err in sps_errors],
    }

    if assets_basedir:
        summary['assets'] = validator.lookup_assets(assets_basedir)

    return summary


def flatten(paths):
    for path in paths:
        ylock = True
        if not path.startswith(('http:', 'https:')):
            # try to expand wildchars and get the absolute path
            for fpath in glob.iglob(path):
                yield os.path.abspath(fpath)
                ylock = False

        # args must not be suppressed, even the invalid
        if ylock == True:
            yield path


@packtools.utils.config_xml_catalog
def main():

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='stylechecker cli utility')
    parser.add_argument('--annotated', action='store_true',
                        help='reproduces the XML with notes at elements that have errors')
    parser.add_argument('--nonetwork', action='store_true',
                        help='prevents the retrieval of the DTD through the network')
    parser.add_argument('--assetsdir', default=None,
                        help='lookup, at the given directory, for each asset referenced by the XML. current working directory will be used by default.')
    parser.add_argument('XML', nargs='+',
                        help='filesystem path or URL to the XML')
    parser.add_argument('--version', action='version', version=packtools_version)
    parser.add_argument('--verbose', action='store_true',
                        help='add the apparent source line and snippet to the summary')
    args = parser.parse_args()

    print('Please wait, this may take a while...')

    summary_list = []
    for xml in flatten(args.XML):
        try:
            xml_validator = get_xmlvalidator(xml, args.nonetwork)
        except XMLError as e:
            sys.exit(e)

        if args.annotated:
            err_xml = xml_validator.annotate_errors()

            fname, fext = xml.rsplit('.', 1)
            out_fname = '.'.join([fname, 'annotated', fext])

            with open(out_fname, 'wb') as fp:
                fp.write(etree.tostring(err_xml, pretty_print=True,
                            encoding='utf-8', xml_declaration=True))

            print('Annotated XML file:', out_fname)

        else:
            try:
                # remote XML will not lookup for assets
                if xml.startswith(('http:', 'https:')):
                    assets_basedir = None
                else:
                    assets_basedir = args.assetsdir or os.path.dirname(xml)

                summary = summarize(xml_validator, assets_basedir=assets_basedir, verbose=args.verbose)
            except TypeError as e:
                sys.exit('Error validating %s. %s.' % (xml_validator, e))

            summary['_xml'] = xml
            summary['is_valid'] = bool(xml_validator.validate()[0] and xml_validator.validate_style()[0])

            summary_list.append(summary)

    if summary_list:
        print(prettify(summary_list))


if __name__ == '__main__':
    main()


import requests
import json

from .constants import ORCID_PUBLIC_BASE_URL
from .utils import dictmapper, MappingRule as to

from .exceptions import NotFoundException

# setting logger
import logging
logger = logging.getLogger("#orcid#")
logging.basicConfig(filename='orcid-log.log', level=logging.INFO)


BASE_HEADERS = {'Accept':'application/orcid+json'}

BIO_PATH = ['orcid-profile','orcid-bio']
PERSONAL_DETAILS_PATH = BIO_PATH + ['personal-details']

def _parse_keywords(d):
    # XXX yes, splitting on commas is bad- but a bug in ORCID
    # (https://github.com/ORCID/ORCID-Parent/issues/27) makes this the  best
    # way. will fix when they do
    if d is not None:
        #return d.get('keyword',[{}])[0].get('value','').split(',')
        return [val['value'] for val in d['keyword']]
    return []

WebsiteBase = dictmapper('WebsiteBase', {
    'name':['url-name','value'],
    'url':['url', 'value']
})

class Website(WebsiteBase):
    def __unicode__(self):
        return self.url

    def __repr__(self):
        return "<%s %s [%s]>" % (type(self).__name__, self.name, self.url)

def _parse_researcher_urls(l):
    if l is not None:
        return [Website(d) for d in l]
    return []

CitationBase = dictmapper('CitationBase', {
    'text':['citation'],
    'type':['work-citation-type']
})

class Citation(CitationBase):
    def __unicode__(self):
        return self.text

    def __repr__(self):
        return '<%s [type: %s]>' % (type(self).__name__, self.type)

ExternalIDBase = dictmapper('ExternalIDBase', {
    'id':['work-external-identifier-id','value'],
    'type':['work-external-identifier-type']
})

class ExternalID(ExternalIDBase):
    def __unicode__(self):
        return unicode(self.id)

    def __repr__(self):
        return '<%s %s:%s>' % (type(self).__name__, self.type, str(self.id))

PublicationBase = dictmapper('PublicationBase',{
    'title':['work-title','title','value'],
    'subtitle':['work-title','subtitle','value'],
    'url':['url','value'],
    'citation': to(['work-citation'], lambda d: Citation(d) if d is not None else None),
    'external_ids':to(['work-external-identifiers','work-external-identifier'],
                      lambda l: map(ExternalID, l) if l is not None else None),
    'publicationyear': ['publication-date', 'year', 'value'],
})

class Publication(PublicationBase):
    def __repr__(self):
        return '<%s "%s">' % (type(self).__name__, self.title)

WORKS_PATH = ['orcid-profile', 'orcid-activities','orcid-works',]

def _parse_publications(l):
    if l is not None:
        #logger.debug(json.dumps(l, sort_keys=True, indent=4, separators=(',', ': ')))
        return [Publication(d) for d in l]
    return []

Works = dictmapper('Works', {
    'publications':to(WORKS_PATH + ['orcid-work'], _parse_publications),
})

AuthorBase = dictmapper('AuthorBase', {
    'orcid':['orcid-profile','orcid-identifier','path'],
    'family_name':PERSONAL_DETAILS_PATH + ['family-name','value'],
    'given_name':PERSONAL_DETAILS_PATH + ['given-names','value'],
    'biography':BIO_PATH + ['biography',],
    'keywords':to(BIO_PATH + ['keywords'], _parse_keywords),
    #'keywords':to(BIO_PATH + ['keywords', 'keyword'], _parse_keywords),
    'researcher_urls':to(BIO_PATH + ['researcher-urls','researcher-url'],
                         _parse_researcher_urls),
})

class Author(AuthorBase):
    _loaded_works = None

    def _load_works(self):
        resp = requests.get(ORCID_PUBLIC_BASE_URL + self.orcid
                            + '/orcid-works', headers = BASE_HEADERS)
        logger.debug(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))
        self._loaded_works = Works(resp.json())

    @property
    def publications(self):
        if self._loaded_works is None:
            self._load_works()
        return self._loaded_works.publications

    def __repr__(self):
        return "<%s %s %s, ORCID %s>" % (type(self).__name__, self.given_name,
                                         self.family_name, self.orcid)

Citation = dictmapper('Citation', {
    'citation':['citation'],
    'citation_type':['work-citation-type']
})

def write_logs(resp):
    logger.debug(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))

def get(orcid_id):
    """
    Get an author based on an ORCID identifier.
    """
    resp = requests.get(ORCID_PUBLIC_BASE_URL + unicode(orcid_id),
                        headers=BASE_HEADERS)
    write_logs(resp)
    json_body = resp.json()
    return Author(json_body)

# def get_with_json(orcid_id):
#     """
#     Get an author based on an ORCID identifier and json
#     """
#     resp = requests.get(ORCID_PUBLIC_BASE_URL + unicode(orcid_id),
#                         headers=BASE_HEADERS)
#     json_body = resp.json()
#     write_logs(resp)
#     return Author(json_body), json_body

def search(query):
    resp = requests.get(ORCID_PUBLIC_BASE_URL + 'search/orcid-bio',
                        params={'q':unicode(query)}, headers=BASE_HEADERS)
    json_body = resp.json()
    return (Author(res) for res in json_body.get('orcid-search-results', {})\
            .get('orcid-search-result'))

### About

A simple wrapper around the orcid.org API. Enhanced clone of this rep - https://github.com/scholrly/orcid-python. Ready to run examples can be found in the [examples](examples) folder. Current version is adapted to work with "services-to-wordcloud" implementation.

### Install

** NOTE ** pyorcid installation that is desriped below is already shiped with the "services-to-wordcloud". Install only dependencies of it (see the section *Dependencies*).

Install at once with pip
```
pip install git+https://github.com/vdmitriyev/pyorcid.git
```

Manual installation (or usage):
* Download from the [GitHub](https://github.com/vdmitriyev/pyorcid/archive/master.zip) latest version
* Unzip archive
* Install dependencies (see the section *Dependencies*)
* Naviage to the example folder, pick up and execute example


### Dependencies

* requests>=1.0.4
* lucene-querybuilder>=0.1.6
* bibtexparser

Install dependencies with pip
```
pip install -r requirements.txt
```

### Command Line Examples

Here's a quick snippet to get info on `John Wilbanks`_. ::

    >>> import orcid
    >>> #retrieve john's profile from his ORCID
    >>> john = orcid.get('0000-0002-4510-0385')
    >>> print john.family_name
    wilbanks

What if you'd like to see an author's works or areas of interest? ::

    >>> print john.keywords
    []
    >>> print john.publications
    []

Hm, let's try another author. ::

    >>> alfonso = orcid.get('0000-0001-8855-5569')
    >>> print alfonso.keywords
    [u'computer science', u' bioinformatics', u' computational biology']
    >>> print alfonso.publications[0]
    <Publication "A note about norbert wiener and his contribution to harmonic analysis and tauberian theorems">


Maybe you'd like to read about Mr. Wiener's contributions? ::

    >>> print alfonso.publications[0].url
    http://www.scopus.com/inward/record.url?eid=2-s2.0-67650513866&partnerID=MN8TOARS

### Searching


If you'd rather search for authors, try ORCID's search functionality ::

    >>> #do a simple author search for john
    >>> authors = orcid.search('john wilbanks')
    >>> print next(authors).family_name
    wilbanks

You can also accomplish more complex queries using `Q` objects and fields ::

    >>> from orcid import Q
    >>> authors = orcid.search(Q('given-name','john') & Q('family-name', 'wilbanks'))
    >>> print next(authors).family_name
    wilbanks


### Credits

Cloned from the repository https://github.com/scholrly/orcid-python lead by [Matt Luongo](https://github.com/mhluongo) from [Scholrly](https://github.com/scholrly/)

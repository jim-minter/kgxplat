#!/usr/bin/python

import bottle
import lxml.html
import requests


def get_rows(source):
    r = requests.get("http://www.opentraintimes.com/location/%s/" %
                     source.upper())
    x = lxml.html.fromstring(r.text)

    for row in x.findall(".//tbody/tr"):
        yield ["".join(td.itertext()).strip() for td in row.findall("td")]


@bottle.route('/<source:re:[A-Za-z]{3}>/<dest:re:[A-Za-z ,]+>')
def root(source, dest):
    dest = [dest.lower() for dest in dest.split(",")]
    bottle.response.content_type = "text/plain"
    rows = ["%s: %-10s (%s)" % (row[5], row[4], row[3])
            for row in get_rows(source)
            if row[4].lower() in dest]

    return "\n".join(rows) + "\n"


@bottle.route('/')
def root():
    bottle.redirect("/KGX/Cambridge,Ely,Kings Lynn")


if __name__ == "__main__":
    bottle.run(host="0.0.0.0")

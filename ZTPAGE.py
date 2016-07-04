# coding: utf-8

from urllib2 import urlopen
import urllib2
import bs4 as BeautifulSoup


class ZTPage:
    def __init__(self, url):
        self.url = url
        self.update()

    def update(self):
        self.update_content()
        self.parse_type()
        self.parse_infos()
        self.parse_links()

    def update_content(self):
        req = urllib2.Request(self.url, headers={'User-Agent': "Magic Browser"})
        html = urlopen(req).read()
        soup = BeautifulSoup.BeautifulSoup(html, "html5lib")
        self.content = soup.find('div', class_="maincont")

    def parse_type(self):
        if "series" in self.url:
            self.type = "Show"
        if "films" in self.url:
            self.type = "Movie"

    def parse_links(self):
        liste = {}
        host = 'error'
        html = self.content.find('div', class_="contentl").find_all(["span", "a"])
        for elem in html:
            if ('span' == elem.name) and (unicode(elem.string) != 'None'):
                host = elem.string
                liste[host] = {}
            if elem.name == 'a':
                elem.string = elem.string.replace("Episode", '').replace('Final', '').strip()
                episode_number = str(elem.string.encode('utf-8'))
                liste[host][episode_number] = elem.attrs['href']
        self.links = liste

    def parse_infos(self):
        # Retreive Title
        title = self.content.find('div', class_="titrearticles").h1.string
        if self.type == "Show":
            title = title.split("-")
            self.title = title[0].strip()
            # Retreive Season for TV Shows
            self.season = int(title[1].replace("Saison", "").replace('[Complete]', '').strip())
        if self.type == "Movie":
            self.title = title.strip()
        # Retreive Language, Format, Codec ...
        info = self.content.find('div', class_="corps").div.span.span.b.strong.string
        first_part = info.split('|')[0]
        second_part = info.split('|')[1]
        self.language = first_part.split(' ')[1].strip()
        self.currentEpisode = first_part.split(' ')[0].strip()
        self.currentEpisode = self.currentEpisode.replace('[', '')
        self.currentEpisode = int(self.currentEpisode.split('/')[0])
        # Pb encodage ...
        quality = second_part.replace("Qualit", '').strip()
        quality = quality[1:]
        # ...
        self.quality = quality.strip()

    def get_available_hosts(self):
        return self.links.keys()

    def get_tvshow_link(self, host, episodenumber):
        alllinks = self.links[host]
        link = alllinks[episodenumber]
        return link

    def print_report(self):
        print self.url
        print self.title
        print self.season
        print self.quality
        print self.language
        print self.currentEpisode
        print self.links

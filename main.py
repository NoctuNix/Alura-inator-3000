credentials = {
    'username': 'username@email.com',
    'password': 'Password123'
}

baseUrls = [
    'https://cursos.alura.com.br/course/curso-1',
    'https://cursos.alura.com.br/course/curso-2',
    'https://cursos.alura.com.br/course/curso-3',
    'https://cursos.alura.com.br/course/curso-4',
    'https://cursos.alura.com.br/course/curso-...',
    'https://cursos.alura.com.br/course/curso-N'
]

import os, requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

session = requests.Session()
session.post("https://cursos.alura.com.br/signin", data=credentials)

def parseHTML (url):
    r = session.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def filterCourseSection (tag):
    return tag.has_attr('class') and len(tag['class']) and tag['class'][0] == 'courseSection-listItem'

def getSections (url):
    soup = parseHTML(url)
    sections = soup.find_all(filterCourseSection)
    return sections

def getDivChild (section, name):
    for ch in section.children:
        if ch.name != 'div':
            continue
        for children in ch.children:
            if children.name == name:
                return children

def getSectionNameAndURL (section):
    url = ''
    name = ''

    child = getDivChild(section, 'a')
    url = f"https://cursos.alura.com.br{child['href']}"

    for children in child.children:
        if children.name != "div" or not len(children['class']):
            continue
        if children['class'][0] == 'courseSectionList-sectionTitle':
            name = children.contents[0].replace('\n','').strip()

    return [name, url]

def downloadVid (url, path, number):
    r = session.get(f"https://cursos.alura.com.br{url}/video")

    if r.status_code >= 400 and r.status_code < 600:
        return

    json = r.json()
    link = json[0]['link']

    o = urlparse(link)
    query = o.query
    videoId = o.path.split("/")[3].split("-")[0]
    vid = requests.get(f"https://video.alura.com.br/alura/{videoId}-hd.mp4?{query}", stream=True)

    vid.raise_for_status()

    with open(f"./{path}/{number}.mp4", "wb") as file:
        for block in vid.iter_content(1024):
            file.write(block)

for baseUrl in baseUrls:
    baseName = baseUrl.split("/")[-1]

    print(f"========================\n{baseName}\n")

    sections = getSections(baseUrl)

    allSections = []
    for section in sections:
        pair = getSectionNameAndURL(section)
        allSections.append(pair)

    try:
        os.mkdir(f"./{baseName}")
    except OSError as e:
        if e.args[0] == 183:
            pass

    def sanitize (str):
        chars = [
            "\\", "/", "*", ":",
            "?", '"', "<", ">", "|"
        ]
        for char in chars:
            str = str.replace(char, "-")
        return str

    for i in range(len(allSections)):
        sanitizedName = sanitize(allSections[i][0])
        name = f"{i +1}- {sanitizedName}"
        url = allSections[i][1]

        print(name, url)

        try:
            os.mkdir(f"./{baseName}/{name}")
        except OSError as e:
            if e.args[0] == 183:
                pass

        r = session.get(url)
        redirectUrl = r.url

        r = session.get(redirectUrl)
        matches = re.findall(r'href="(/course/[\w-]+/task/[0-9]+)"', r.text, re.U|re.I)

        for i in range(len(matches)):
            print(f"{i +1}: {matches[i]}")
            downloadVid(matches[i], f"{baseName}/{name}", i +1)

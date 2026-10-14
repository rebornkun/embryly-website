"""Build the Embryly collection without rewriting the rest of the website."""
from pathlib import Path
import ast, csv, html, json, math, re, struct, sys
import xml.etree.ElementTree as ET

def build(root):
    root = Path(root)
    data = root / 'content' / 'blog'
    topics = json.loads((data / 'topics.json').read_text())
    sources = json.loads((data / 'sources.json').read_text())
    descriptions = json.loads((data / 'descriptions.json').read_text())
    config = json.loads((root / 'blog_config.json').read_text())
    origin = config['production_origin'].rstrip('/')
    if not origin.startswith('https://'):
        raise ValueError('Production origin must use https')
    app_url = config.get('app_store_url')
    if app_url and not app_url.startswith('https://apps.apple.com/'):
        raise ValueError('Use a verified Apple App Store URL')
    # Reuse the established navigation and footer without executing the old build.
    tree = ast.parse((root / 'build.py').read_text())
    definitions = [n for n in tree.body if
        (isinstance(n, ast.FunctionDef) and n.name in ('header','footer')) or
        (isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='APPLE' for t in n.targets))]
    shared = {}
    exec(compile(ast.Module(body=definitions,type_ignores=[]),'site shell','exec'),shared)
    header, footer = shared['header'], shared['footer']
    esc = html.escape
    checked = config['checked_date']
    by_slug = {t['slug']:t for t in topics}
    ledger = []

    def source_url(key):
        return sources[key]['url']

    def inline(text):
        text = re.sub(r'\[([^\]]+)\]\(source:([a-z]+)\)',
                      lambda m:f'[{m[1]}]({source_url(m[2])})',text)
        text = esc(text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                      lambda m:f'<a href="{esc(html.unescape(m[2]),quote=True)}">{m[1]}</a>',text)
        return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)

    def markdown(text):
        blocks=[]
        for part in text.strip().split('\n\n'):
            if part.startswith('## '):
                title=part[3:].strip()
                anchor=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
                blocks.append(f'<h2 id="{anchor}">{inline(title)}</h2>')
            else: blocks.append('<p>'+inline(part.replace('\n',' '))+'</p>')
        return blocks

    def cta(topic=None):
        benefit = ('Scan foods and barcodes for clearer pregnancy food guidance.' if
                   not topic or topic['category']!='Meal ideas' else
                   'Find meal inspiration matched to your saved preferences and pregnancy week.')
        badge=shared['APPLE']+'<span><small>Download on the</small><strong>App Store</strong></span>'
        action = (f'<a class="journal-store-badge" href="{esc(app_url,quote=True)}" aria-label="Download Embryly on the App Store">{badge}</a>' if app_url else
                  f'<button class="journal-store-badge" disabled aria-label="Download Embryly on the App Store, coming soon" aria-describedby="app-soon">{badge}</button><span id="app-soon" class="coming-soon">Coming soon on iPhone</span>')
        return f'<aside class="journal-cta" aria-label="Embryly app"><img class="journal-app-icon" src="../assets/embryly-app-icon.png" width="56" height="56" alt="Embryly app icon"><div><strong>A little food clarity.</strong><p>{benefit}</p></div><div class="cta-action">{action}</div></aside>'

    def card(t):
        slug=t['slug']
        return f'<a class="journal-card" data-category="{esc(t["category"],quote=True)}" data-search="{esc((t["title"]+" "+descriptions[slug]).lower(),quote=True)}" href="{slug}.html"><div class="journal-card-image"><img src="../assets/blog/{slug}.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="{esc(t["alt"],quote=True)}"></div><span class="meta">{esc(t["category"])}</span><h2>{esc(t["title"])}</h2><p>{esc(descriptions[slug])}</p><span class="journal-read">Read the guide <span aria-hidden="true">↗</span></span></a>'

    def page(path,title,description,content,image=None,schema=None):
        url=origin+'/'+path
        image=image or 'assets/blog/sushi-while-pregnant.jpg'
        robot='index,follow' if config['indexable'] else 'noindex,follow'
        schema_tag='' if not schema else '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>'
        document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#faf7f2"><title>{esc(title)} | Embryly</title><meta name="description" content="{esc(description,quote=True)}"><meta name="robots" content="{robot}"><link rel="canonical" href="{url}"><meta property="og:type" content="{'article' if schema else 'website'}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{origin}/{image}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css?v=20260926-portraits"><link rel="stylesheet" href="../assets/blog.css?v=20261014">{schema_tag}<script defer src="../assets/site.js?v=20260926-portraits"></script><script defer src="../assets/blog.js?v=20261014"></script></head><body>{header('../')}<main id="main">{content}</main>{footer('../')}</body></html>'''
        (root/path).write_text(document)

    for t in topics:
        slug=t['slug']
        raw=(data/'articles'/f'{slug}.md').read_text()
        count=len(re.findall(r'\b[\w’]+\b',re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',raw)))
        blocks=markdown(raw)
        used=list(dict.fromkeys(re.findall(r'\]\(source:([a-z]+)\)',raw)))
        toc=''.join(f'<a href="#{re.sub(r"[^a-z0-9]+","-",h.lower()).strip("-")}">{esc(h)}</a>' for h in re.findall(r'^## (.+)$',raw,re.M))
        refs=''.join(f'<li><a href="{esc(source_url(k),quote=True)}">{esc(sources[k]["title"])}</a></li>' for k in used)
        related=''.join(card(by_slug[s]) for s in t['related'])
        image=f'assets/blog/{slug}.jpg'
        post={'@type':'BlogPosting','headline':t['title'],'description':descriptions[slug],
              'author':{'@type':'Organization','name':'Embryly Editorial Team'},
              'publisher':{'@type':'Organization','name':'Embryly'},'inLanguage':'en-US',
              'mainEntityOfPage':origin+f'/blog/{slug}.html','image':origin+'/'+image,
              'dateModified':config['date_modified'],'wordCount':count,'articleSection':t['category']}
        if config.get('date_published'):post['datePublished']=config['date_published']
        schema={'@context':'https://schema.org','@graph':[post,{'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Home','item':origin+'/index.html'},
            {'@type':'ListItem','position':2,'name':'Journal','item':origin+'/blog/index.html'},
            {'@type':'ListItem','position':3,'name':t['title'],'item':origin+f'/blog/{slug}.html'}]}]}
        from datetime import date
        editorial=date.fromisoformat(t['editorial_date']).strftime('%B %-d, %Y') if t.get('editorial_date') else None
        date_line=f'Editorial date: {editorial} · ' if editorial else ''
        publication_line=f'Published {date.fromisoformat(config["date_published"]).strftime("%B %-d, %Y")} · ' if config.get('date_published') else ''
        body=f'''<article class="journal-article"><header class="journal-article-heading"><a class="text-link" href="index.html">← The Embryly journal</a><p class="meta">{esc(t['category'])} · {math.ceil(count/200)} min read</p><h1>{esc(t['title'])}</h1><p class="journal-deck">{esc(descriptions[slug])}</p><p class="journal-byline">Embryly Editorial Team<br>{date_line}{publication_line}Sources checked October 14, 2026</p></header><div class="journal-body"><div class="journal-answer">{blocks[0]}</div>{cta(t)}<figure class="journal-cover"><img src="../{image}" width="1536" height="1024" alt="{esc(t['alt'],quote=True)}" fetchpriority="high" decoding="async"></figure><nav class="journal-toc" aria-label="In this article"><strong>In this article</strong>{toc}</nav>{''.join(blocks[1:])}<aside class="journal-note">General educational guidance based on US sources. Your care team can advise on individual circumstances. Artwork is illustrative.</aside><section class="journal-sources" aria-labelledby="sources-title"><h2 id="sources-title">Sources</h2><ul>{refs}</ul></section>{cta(t).replace('id="app-soon"','id="app-soon-end"').replace('aria-describedby="app-soon"','aria-describedby="app-soon-end"')}<section class="journal-related" aria-labelledby="related-title"><h2 id="related-title">A little more reading</h2><div class="journal-grid">{related}</div></section></div></article>'''
        page(f'blog/{slug}.html',t['title'],descriptions[slug],body,image,schema)
        ledger.append({**t,'description':descriptions[slug],'word_count':count,'sources_used':used,'checked_date':checked,'status':'local preview','measured_search_volume':None,'published_date':config.get('date_published')})

    categories=list(dict.fromkeys(t['category'] for t in topics))
    filters='<button data-filter="All" aria-pressed="true">All</button>'+''.join(f'<button data-filter="{esc(c,quote=True)}" aria-pressed="false">{esc(c)}</button>' for c in categories)
    content=f'''<section class="journal-intro"><span class="eyebrow">THE EMBRYLY JOURNAL</span><h1>Food questions.<br><em>A little more clarity.</em></h1><p>Practical answers for the shop, the kitchen and the moment you wonder, “Can I eat this?”</p></section><section class="journal-library" aria-label="Article library"><label class="journal-search"><span>Find a food or question</span><input type="search" id="journal-search" placeholder="Try sushi, cheese or coffee" autocomplete="off"></label><div class="journal-filters" aria-label="Filter articles">{filters}</div><p class="journal-count" role="status" aria-live="polite">30 guides to explore</p><div class="journal-grid" id="journal-grid">{''.join(card(t) for t in topics)}</div><p id="journal-empty" hidden>No matching guides yet. Try another food or choose All.</p><section class="journal-foundations"><h2>Start with the bigger picture</h2><a href="pregnancy-food-safety.html">A calmer guide to pregnancy food safety ↗</a><a href="pregnancy-meal-planning.html">A flexible approach to pregnancy meal planning ↗</a></section></section>'''
    page('blog/index.html','Pregnancy Food Safety Guides and Meal Ideas','Explore 30 practical pregnancy food guides, from sushi and cheese to seasonal food questions and everyday meal ideas.',content)
    (data/'editorial-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False))
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    sitemap=root/'sitemap.xml'
    tree=ET.parse(sitemap)
    for item in list(tree.getroot()):
        loc=item.find(f'{{{ns}}}loc')
        if loc is not None and any(loc.text==origin+f'/blog/{t["slug"]}.html' for t in topics):tree.getroot().remove(item)
    for t in topics:
        entry=ET.SubElement(tree.getroot(),f'{{{ns}}}url')
        ET.SubElement(entry,f'{{{ns}}}loc').text=origin+f'/blog/{t["slug"]}.html'
        ET.SubElement(entry,f'{{{ns}}}lastmod').text=config['date_modified']
    tree.write(sitemap,encoding='utf-8',xml_declaration=True)
    # Keep shared website metadata and the original introductory guides consistent.
    icon_links='<link rel="icon" href="{prefix}assets/favicon-32.png" type="image/png" sizes="32x32"><link rel="icon" href="{prefix}assets/favicon-16.png" type="image/png" sizes="16x16"><link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png" sizes="180x180">'
    for document in [*root.glob('*.html'),*root.joinpath('blog').glob('*.html')]:
        text=document.read_text()
        prefix='../' if document.parent.name=='blog' else ''
        text=re.sub(r'<link\b[^>]*\brel="(?:icon|apple-touch-icon)"[^>]*>','',text)
        text=text.replace('</head>',icon_links.format(prefix=prefix)+'</head>')
        text=text.replace('https://embryly-website.vercel.app',origin)
        text=re.sub(r'<meta name="robots" content="[^"]+">',f'<meta name="robots" content="{"index,follow" if config["indexable"] else "noindex,follow"}">',text)
        if document.parent.name=='blog':
            if 'assets/blog.css?' not in text:text=text.replace('</head>','<link rel="stylesheet" href="../assets/blog.css?v=20261014"></head>')
            if 'assets/blog-launch.css?' not in text:text=text.replace('</head>','<link rel="stylesheet" href="../assets/blog-launch.css?v=20261014"></head>')
            text=re.sub(r'<p><a class="text-link" href="../index.html#download">Explore Embryly ↗</a><br>.*?</p>',cta(),text)
        if document==root/'index.html' and config.get('google_site_verification'):
            text=re.sub(r'<meta name="google-site-verification"[^>]*>','',text)
            text=text.replace('</head>',f'<meta name="google-site-verification" content="{esc(config["google_site_verification"],quote=True)}"></head>')
        document.write_text(re.sub(r'(?m)^[ \t]+$', '', text))
    (root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n' if config['indexable'] else 'User-agent: *\nDisallow: /\n')
    print(f'Built {len(topics)} articles; {sum(x["word_count"] for x in ledger)} words; indexable={config["indexable"]}')

if __name__=='__main__':build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent)

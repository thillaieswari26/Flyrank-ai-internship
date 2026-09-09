import json, re, time
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin, urldefrag, urlparse
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError, field_validator

BASE='https://books.toscrape.com/'
UA='ThillaiEswari-PoliteScraper/1.0 (+https://github.com/thillaieswari26/flyrank-week5-polite-scraper)'
ROOT=Path(__file__).resolve().parents[1]; CACHE=ROOT/'cache'; OUT=ROOT/'output'
class Book(BaseModel):
    title:str; product_url:str; price_text:str; availability_text:str; rating_text:str
    description:str|None; source_page:str; fetched_at:str; price_gbp:float
    @field_validator('price_gbp')
    @classmethod
    def positive(cls,v):
        if v<0: raise ValueError('negative price')
        return v
def canon(u):
    u,_=urldefrag(urljoin(BASE,u)); p=urlparse(u); path=re.sub('/+','/',p.path)
    return p._replace(path=path.rstrip('/') or '/').geturl()
def get(u,cache,report):
    if cache and cache.exists(): report['cache_hits']+=1; return cache.read_text(encoding='utf8')
    for attempt in range(2):
        try:
            time.sleep(.5 if report['real_requests'] else 0)
            report['real_requests']+=1; r=requests.get(u,headers={'User-Agent':UA},timeout=15)
            report['pages_fetched']+=1
            if r.status_code==200:
                if cache: cache.parent.mkdir(parents=True,exist_ok=True); cache.write_text(r.text,encoding='utf8')
                return r.text
            if 500<=r.status_code<600 and attempt==0: continue
            raise RuntimeError(f'HTTP {r.status_code}')
        except requests.Timeout:
            if attempt==0: continue
            raise RuntimeError('timeout after one retry')
    raise RuntimeError('request failed')
def main():
    CACHE.mkdir(exist_ok=True); (CACHE/'details').mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    R={'start_time':datetime.now(timezone.utc).isoformat(),'pages_fetched':0,'real_requests':0,'cache_hits':0,'catalogue_pages':0,'discovered':0,'unique_urls':0,'valid_records':0,'invalid_records':0,'failed_pages':[]}
    try: R['robots_status']=requests.get(urljoin(BASE,'robots.txt'),headers={'User-Agent':UA},timeout=15).status_code; R['real_requests']+=1; R['pages_fetched']+=1
    except Exception as e: R['robots_status']=str(e)
    html=get(BASE,CACHE/'catalogue-page-1.html',R); pages=[(BASE,html)]; cur=BASE
    for n in (2,3):
        soup=BeautifulSoup(html,'html.parser'); a=soup.select_one('li.next a')
        if not a: break
        cur=canon(urljoin(cur,a['href'])); html=get(cur,CACHE/f'catalogue-page-{n}.html',R); pages.append((cur,html))
    R['catalogue_pages']=len(pages); urls=[]; src={}
    for page,html in pages:
        for a in BeautifulSoup(html,'html.parser').select('article.product_pod h3 a'):
            u=canon(urljoin(page,a['href'])); urls.append(u); src[u]=page
    urls=list(dict.fromkeys(urls)); R['discovered']=len(urls); R['unique_urls']=len(urls)
    good=[]; errors=[]
    for i,u in enumerate(urls,1):
        try:
            s=BeautifulSoup(get(u,CACHE/'details'/f'{i:03}.html',R),'html.parser'); pm=s.select_one('div.product_main')
            title=pm.select_one('h1'); price=pm.select_one('p.price_color'); av=pm.select_one('p.instock'); rating=pm.select_one('p.star-rating')
            if not all((title,price,av,rating)): raise ValueError('required selector missing')
            d=s.select_one('#product_description + p')
            data={'title':title.get_text(' ',strip=True),'product_url':u,'price_text':price.get_text(' ',strip=True),'availability_text':av.get_text(' ',strip=True),'rating_text':next((x for x in rating.get('class',[]) if x!='star-rating'),rating.get_text(' ',strip=True)),'description':d.get_text(' ',strip=True) if d else None,'source_page':src[u],'fetched_at':datetime.now(timezone.utc).isoformat(),'price_gbp':float(re.search(r'[0-9]+(?:\.[0-9]+)?',price.get_text()).group())}
            good.append(Book.model_validate(data).model_dump())
        except Exception as e: errors.append({'product_url':u,'error':str(e)})
    try: get(BASE+'this-page-does-not-exist-hopefully/',None,R)
    except Exception as e: R['failed_pages'].append({'url':BASE+'this-page-does-not-exist-hopefully/','error':str(e),'reason':'deliberately broken test URL'})
    R['valid_records']=len(good); R['invalid_records']=len(errors)
    (OUT/'books.json').write_text(json.dumps(good,indent=2),encoding='utf8'); (OUT/'errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8'); (OUT/'run-report.json').write_text(json.dumps(R,indent=2),encoding='utf8')
    print('catalogue_pages=',R['catalogue_pages'],'unique_urls=',R['unique_urls'],'valid_records=',R['valid_records'])
if __name__=='__main__': main()

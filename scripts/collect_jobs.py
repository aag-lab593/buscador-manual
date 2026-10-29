#!/usr/bin/env python3
"""Public remote job feed collector. No credentials, no personal data."""
import json, re, urllib.request, urllib.error, datetime
from pathlib import Path
FAMILIES={
"operations":["operations","operations coordinator","operations specialist","coordinador de operaciones"],
"customer":["customer success","customer experience","customer support","client success"],
"people":["people operations","human resources","talent operations","people partner"],
"business":["business operations","business analyst","administrative manager"],
"executive":["executive assistant","executive operations","chief of staff"],
"implementation":["implementation","onboarding","project coordinator"],
"ai":["ai operations","ai implementation","automation"],
"hospitality":["hospitality","hotel operations","property operations","guest experience"]}
SOURCES={
"Remotive":"https://remotive.com/api/remote-jobs?limit=500",
"Jobicy":"https://jobicy.com/api/v2/remote-jobs?count=50",
"Himalayas":"https://himalayas.app/jobs/api/search?limit=100",
"Remote OK":"https://remoteok.com/api",
"Arbeitnow":"https://www.arbeitnow.com/api/job-board-api"}
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"CareerOfficeManualSearch/1.0 (public feed; GitHub Pages)","Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=20) as resp:return json.load(resp)
def parse(name,data):
 if name=="Remotive":rows=data.get("jobs",[])
 elif name=="Jobicy":rows=data.get("jobs",[])
 elif name=="Himalayas":rows=data.get("jobs",data.get("results",[]))
 elif name=="Remote OK":rows=data if isinstance(data,list) else []
 else:rows=data.get("data",[])
 for x in rows:
  if name=="Arbeitnow" and not x.get("remote"):continue
  title=x.get("title") or x.get("position") or x.get("jobTitle") or ""
  company=x.get("company_name") or x.get("company") or x.get("companyName") or ""
  if isinstance(company,dict):company=company.get("name","")
  location=x.get("candidate_required_location") or x.get("location") or x.get("jobGeo") or x.get("geo") or ""
  if isinstance(location,dict):location=location.get("name","")
  url=x.get("url") or x.get("jobUrl") or x.get("applicationLink") or ""
  if not isinstance(url,str) or not url.startswith("https://") or not title:continue
  families=[key for key,terms in FAMILIES.items() if any(t in title.lower() for t in terms)]
  if not families:continue
  yield dict(title=title,company=str(company),location=str(location),url=url,source=name,families=families,salary=str(x.get("salary") or ""),posted=str(x.get("pubDate") or x.get("publication_date") or x.get("date") or ""))
def main():
 results=[];stats=[];seen=set()
 for name,url in SOURCES.items():
  try:
   data=fetch(url);jobs=list(parse(name,data));stats.append(dict(source=name,status="ok",matches=len(jobs)))
   for job in jobs:
    key=job["url"].split("?")[0].rstrip("/")
    if key not in seen:seen.add(key);results.append(job)
  except Exception as exc:stats.append(dict(source=name,status="error",message=str(exc)[:160],matches=0))
 payload={"updated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"jobs":results,"sources":stats,"scope":"Public remote listings; Ecuador eligibility unverified"}
 out=Path("data/jobs.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"jobs":len(results),"sources":stats}))
if __name__=="__main__":main()

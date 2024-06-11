import json
import csv
from datetime import datetime

def years_between(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return abs((end_date - start_date).days) // 365

csv_file = 'resume.csv'
csv_obj = open(csv_file, 'w')
csv_writer = csv.writer(csv_obj)
header = ["id", "location", "experience"]


# Retrieve JSON data from the file
with open("resume_data.json", "r") as file:
    data = json.load(file)

# get all languages
langages_header = []
for item in data:
    if item.get('resumes', []):
        for l in item.get('resumes', [])[0].get("languages"):
            lang = l.get("language").strip().lower()
            lang = lang.replace('francais', 'français')
            if lang != "" and lang not in langages_header:
                langages_header.append(lang)


# get all skills
skills_header = []
for item in data:
    if item.get('resumes', []):
        featuredSkills = item.get("resumes")[0].get('skills', [])[0].get("featuredSkills")
        if isinstance(featuredSkills, list):
            for skill in featuredSkills:
                if skill.get("skill").strip().lower() not in skills_header:
                    skills_header.append(skill.get("skill").strip().lower())


header = header + langages_header + skills_header
csv_writer.writerow(header)



for item in data:
    row = [0] * len(header)
    id = item.get('user').get('id')
    row[header.index('id')] = id

    if item.get('resumes', []):
        location = item.get('resumes', [])[0].get("perInfs").get('location').strip().lower()
        row[header.index('location')] = location
        for l in item.get('resumes', [])[0].get("languages"):
            lang = l.get("language").strip().lower()
            lang = lang.replace('francais', 'français')
            if lang != "":
                row[header.index(lang)] = 1

        featuredSkills = item.get("resumes")[0].get('skills', [])[0].get("featuredSkills")
        if isinstance(featuredSkills, list):
            for skill in featuredSkills:
                row[header.index(skill.get("skill").strip().lower())] = skill.get("rating")

        experience = 0
        for w in item.get('resumes', [])[0].get("WorkExps"):
            experience += years_between(w.get("StartDate"), w.get("EndDate"))
        row[header.index("experience")] = experience
    csv_writer.writerow(row)

csv_obj.close()
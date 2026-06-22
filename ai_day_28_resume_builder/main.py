import re
from datetime import datetime

def bullet_points(role):
    bullets = {
        "software engineer":    ["Designed and developed scalable backend services using Python and REST APIs","Collaborated with cross-functional teams to deliver features on time","Improved application performance by 30% through code optimisation","Wrote unit and integration tests achieving 85% code coverage"],
        "data analyst":         ["Analysed large datasets to extract actionable business insights","Built interactive dashboards using Python and SQL","Automated reporting pipelines saving 10+ hours of manual work weekly","Presented findings to stakeholders in clear non-technical language"],
        "web developer":        ["Built responsive web applications using HTML CSS and JavaScript","Developed and consumed RESTful APIs for frontend-backend integration","Optimised website performance achieving 95+ Lighthouse scores","Implemented version control workflows using Git and GitHub"],
        "data scientist":       ["Developed machine learning models to predict customer behaviour","Performed feature engineering and model evaluation using Scikit-learn","Built data pipelines for cleaning and transforming large datasets","Communicated model results through visualisations and reports"],
        "devops engineer":      ["Managed CI/CD pipelines using GitHub Actions and Jenkins","Containerised applications using Docker and orchestrated with Kubernetes","Monitored system performance and reduced downtime by 40%","Automated infrastructure provisioning using Terraform"],
    }
    role_lower = role.lower()
    for key, points in bullets.items():
        if any(w in role_lower for w in key.split()):
            return points
    return ["Delivered high-quality work consistently meeting project deadlines","Collaborated effectively with team members and stakeholders","Identified and resolved issues proactively improving processes","Contributed to documentation and knowledge sharing initiatives"]

def generate_resume(info):
    lines = []
    lines.append("=" * 65)
    lines.append(f"  {info['name'].upper()}")
    lines.append(f"  {info['email']}  |  {info['phone']}  |  {info['location']}")
    if info.get("github"):
        lines.append(f"  GitHub: {info['github']}")
    lines.append("=" * 65)
    lines.append("")
    lines.append("PROFESSIONAL SUMMARY")
    lines.append("-" * 40)
    summary = f"{info['name']} is a motivated {info['target_role']} with {info['experience']} years of experience in {info['field']}. Passionate about building impactful solutions and continuously learning new technologies."
    lines.append(summary)
    lines.append("")
    lines.append("TECHNICAL SKILLS")
    lines.append("-" * 40)
    for cat, skills in info["skills"].items():
        lines.append(f"  {cat}: {', '.join(skills)}")
    lines.append("")
    lines.append("EXPERIENCE")
    lines.append("-" * 40)
    for job in info["jobs"]:
        lines.append(f"  {job['role']} | {job['company']} | {job['period']}")
        for bp in bullet_points(job["role"]):
            lines.append(f"    • {bp}")
        lines.append("")
    lines.append("EDUCATION")
    lines.append("-" * 40)
    for edu in info["education"]:
        lines.append(f"  {edu['degree']} | {edu['institution']} | {edu['year']}")
    lines.append("")
    lines.append("=" * 65)
    return "\n".join(lines)

def main():
    print("=== AI Resume Builder ===")
    print("Answer the questions and get a professional resume generated.\n")
    info = {}
    info["name"]        = input("Full name: ").strip()
    info["email"]       = input("Email: ").strip()
    info["phone"]       = input("Phone: ").strip()
    info["location"]    = input("Location (city, country): ").strip()
    info["github"]      = input("GitHub URL (optional): ").strip()
    info["target_role"] = input("Target role (e.g. Software Engineer): ").strip()
    info["field"]       = input("Your field (e.g. software development, data science): ").strip()
    try: info["experience"] = int(input("Years of experience: "))
    except: info["experience"] = 0
    print("\nSkills (press Enter to skip a category):")
    info["skills"] = {}
    cats = ["Languages", "Frameworks", "Databases", "Tools"]
    for cat in cats:
        s = input(f"  {cat} (comma separated): ").strip()
        if s: info["skills"][cat] = [x.strip() for x in s.split(",")]
    print("\nWork experience (press Enter with no company to finish):")
    info["jobs"] = []
    while True:
        company = input("  Company name (or Enter to finish): ").strip()
        if not company: break
        role   = input("  Your role: ").strip()
        period = input("  Period (e.g. Jan 2023 - Present): ").strip()
        info["jobs"].append({"company": company, "role": role, "period": period})
    print("\nEducation (press Enter with no institution to finish):")
    info["education"] = []
    while True:
        inst = input("  Institution (or Enter to finish): ").strip()
        if not inst: break
        degree = input("  Degree: ").strip()
        year   = input("  Year: ").strip()
        info["education"].append({"institution": inst, "degree": degree, "year": year})
    resume = generate_resume(info)
    print(f"\n{resume}")
    filename = f"{info['name'].lower().replace(' ','_')}_resume.txt"
    with open(filename, "w") as f:
        f.write(resume)
    print(f"\nResume saved to {filename}")

if __name__ == "__main__":
    main()

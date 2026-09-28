import json
from pathlib import Path

from config import qdrant_client, COLLECTION_NAME
from services.resume_analysis import analyze_resume
from services.role_recommendation import generate_other_roles
from services.roadmap import generate_roadmap
from services.interview_questions import get_interview_questions
from setup_vector_db import create_db


# -----------------------------
# VECTOR DB VALIDATION
# -----------------------------

print("=" * 60)
print("  RAG AI Resume Analyzer")
print("=" * 60)

print("\n[Step 1/2] Checking vector database...")

if not qdrant_client.collection_exists(COLLECTION_NAME):
    print("\n  Vector database not found. Setting up now (this only runs once)...")
    result = create_db()
    print(f"\n  {result}")

collection_info = qdrant_client.get_collection(COLLECTION_NAME)
vector_count = collection_info.points_count

print(f"  Vector DB ready — {vector_count} knowledge chunks loaded.")


# -----------------------------
# ROLE SELECTION (INTERACTIVE)
# -----------------------------

print("\n[Step 2/2] Role Selection")

# Load roles from data/ folder
roles_path = Path(__file__).parent.parent / "data" / "available_roles.json"

with open(roles_path, "r") as fh:
    available_roles = json.load(fh)

sorted_roles = sorted(available_roles["roles"])

print("\n  Available Roles:")
print("  " + "-" * 40)
for i, role in enumerate(sorted_roles, start=1):
    print(f"  {i:>2}. {role.title()}")
print("  " + "-" * 40)

role_input = None

while True:
    print("\n  You can enter:")
    print("    - A number (e.g. 3) to pick from the list above")
    print("    - The role name directly (e.g. data scientist)")

    user_input = input("\n  Your choice: ").strip().lower()

    # Check if user entered a number
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(sorted_roles):
            role_input = sorted_roles[index]
            print(f"\n  Selected role: {role_input.title()}")
            break
        else:
            print(f"\n  Invalid number. Please enter a number between 1 and {len(sorted_roles)}.")
    # Check if user entered a role name
    elif user_input in available_roles["roles"]:
        role_input = user_input
        print(f"\n  Selected role: {role_input.title()}")
        break
    else:
        print(f"\n  '{user_input}' is not a valid role or number.")
        print("  Please try again.")


# -----------------------------
# RESUME + JD + MATCH ANALYSIS
# -----------------------------

print("\n" + "=" * 60)
print("  Analyzing your resume... (this may take a moment)")
print("=" * 60)

result = analyze_resume(role_input)

resume_extract = result["resume_extract"]

match_data = json.loads(
    result["match_answer"]
)


print("\nMatch Percentage:")
print(match_data["match_percent"])

print("\nMissing Skills:")
for skill in match_data["missing_skills"]:
    print("-", skill)

print("\nAnalysis:")
print(match_data["short_analysis"])


# -----------------------------
# OTHER ROLES
# -----------------------------

other_roles_data = generate_other_roles(
    resume_extract,
    role_input
)

print("\nOther Roles:")

for role in other_roles_data["roles"]:
    print("-", role)


# -----------------------------
# ROADMAP
# -----------------------------

roadmap_data = generate_roadmap(
    match_data["missing_skills"]
)

print("\nLearning Path:")

for item in roadmap_data["learning_path"]:
    print("-", item)

print("\nStudy Resources:")

for resource in roadmap_data["study_resources"]:
    print("-", resource)

print("\nRecommended Projects:")

for project in roadmap_data["recommended_projects"]:
    print("-", project)

print("\nRoadmap:")

for step in roadmap_data["roadmap"]:
    print("-", step)


# interview ques feature 

interview_questions = get_interview_questions(
    role_input,
    top_k=10
)

print("\nInterview Questions:")
print(interview_questions)

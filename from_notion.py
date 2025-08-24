from notion_client import Client
import pandas as pd

# Replace with your integration token and database ID
NOTION_TOKEN = notion_token
DATABASE_ID = database_id

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

def get_candidates():
    # Query the database
    results = notion.databases.query(database_id=DATABASE_ID).get("results", [])

    candidates = []
    for page in results:
        props = page["properties"]

        # First name (title)
        title_list = props.get("First name", {}).get("title", [])
        first_name = title_list[0].get("plain_text", "") if title_list else ""

        # Last name (rich_text)
        rich_last = props.get("Last name", {}).get("rich_text", [])
        last_name = rich_last[0].get("plain_text", "") if rich_last else ""

        # 2nd Preference Team (rich_text)
        rich_pref = props.get("2nd Preference Team", {}).get("rich_text", [])
        second_pref = rich_pref[0].get("plain_text", "") if rich_pref else ""

        # Degree and Year (select)
        degree = props.get("Degree/Major", {}).get("select", {}).get("name", "")
        year = props.get("Year", {}).get("select", {}).get("name", "")

        # Resume (files)
        resume_files = props.get("Resume", {}).get("files", [])
        resume = resume_files[0].get("name", "") if resume_files else ""

        # LinkedIn (url)
        linkedin = props.get("LinkedIn", {}).get("url", "")

        # Interview Transcript (files)
        transcript_files = props.get("Interview Transcript", {}).get("files", [])
        transcript = transcript_files[0].get("name", "") if transcript_files else ""

        # Statuses (status)
        initial_status = props.get("Initial Filtration Status", {}).get("status", {}).get("name", "")
        interview_status = props.get("Interview Status", {}).get("status", {}).get("name", "")

        # Exec Comments (rich_text)
        comments_rich = props.get("Exec Comments", {}).get("rich_text", [])
        exec_comments = comments_rich[0].get("plain_text", "") if comments_rich else ""

        candidates.append({
            "first_name": first_name,
            "last_name": last_name,
            "2nd Preference Team": second_pref,
            "Degree/Major": degree,
            "Year": year,
            "Resume": resume,
            "LinkedIn": linkedin,
            "Interview Transcript": transcript,
            "Initial Filtration Status": initial_status,
            "Interview Status": interview_status,
            "Exec Comments": exec_comments,
        })

    return candidates


# Example usage
if __name__ == "__main__":
    data = get_candidates()
    df = pd.DataFrame(data)

    # Add "No" column
    df.index = df.index + 1
    df.reset_index(inplace=True)
    df.rename(columns={"index": "No"}, inplace=True)

    # Save all applicants
    df.to_csv("applicants.csv", index=False)
    print("✅ Saved as applicants.csv")

    # === FILTER BY Initial Filtration Status ===
    accepted_init = df[df["Initial Filtration Status"] == "Accepted"]
    rejected_init = df[df["Initial Filtration Status"] == "Rejected"]

    accepted_init.to_csv("accepted_initial_filtration.csv", index=False)
    print("✅ Saved as accepted_initial_filtration.csv")

    rejected_init.to_csv("rejected_initial_filtration.csv", index=False)
    print("❌ Saved as rejected_initial_filtration.csv")

    # === FILTER BY Interview Status ===
    accepted_interview = df[df["Interview Status"] == "Accepted"]
    rejected_interview = df[df["Interview Status"] == "Rejected"]

    accepted_interview.to_csv("accepted_interview.csv", index=False)
    print("✅ Saved as accepted_interview.csv")

    rejected_interview.to_csv("rejected_interview.csv", index=False)
    print("❌ Saved as rejected_interview.csv")

    # Optional: print summaries
    print("\n📋 Summary:")
    print(f"Total applicants: {len(df)}")
    print(f"Initial Accepted: {len(accepted_init)}")
    print(f"Initial Rejected: {len(rejected_init)}")
    print(f"Interview Accepted: {len(accepted_interview)}")
    print(f"Interview Rejected: {len(rejected_interview)}")

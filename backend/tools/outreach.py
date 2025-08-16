
def simulate_networking_outreach(name: str = "Hiring Manager", to_email: str = "", role: str = "", company: str = "", platform: str = "Email") -> str:
    intro = f"Hi {name},"
    body = (
        f" I admire {company or 'your team'}'s work and I'm exploring opportunities as "
        f"{role or 'a contributor in data-driven product development'}. "
        "Would you be open to a brief chat about the team’s priorities and how I might add value?"
    )
    closing = "\n\nBest regards,\nShahnaz"
    draft = f"{intro}{body}{closing}"
    status = "✅ Simulated send (no real email dispatched)."
    if to_email:
        status += f" Recipient: {to_email}."
    return f"Drafted outreach via {platform}:{' (simulated send)' if to_email else ''}\n\n{draft}\n\nStatus: {status}"

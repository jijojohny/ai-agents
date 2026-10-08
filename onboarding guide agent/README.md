# Onboarding Guide Agent

Drafts **Day 1 / Week 1 / Month 1** onboarding outlines with checklists and role owners. Optional JSON (`OnboardingGuideReply`). Multi-provider LLM.

```bash
cd "onboarding guide agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Role, company context, tools..."
```

Env: `ONBOARDING_GUIDE_AGENT_PROVIDER`, `ONBOARDING_GUIDE_AGENT_MODEL`. Does not invent company policies.
